import logging
import re
import shutil
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import config
from core.logging_utils import log_event
from PIL import Image
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels

try:
    import pymupdf
except ModuleNotFoundError:
    import fitz as pymupdf

logger = logging.getLogger(__name__)

_CAPTION_START = re.compile(
    r"^\s*((fig(?:ure)?\.?\s*\d+[\w.\-]*)|(table\s*\d+[\w.\-]*)|(图\s*\d+[\w.\-]*)|(表\s*\d+[\w.\-]*))",
    re.IGNORECASE,
)


@dataclass
class FigureRecord:
    id: str
    source: str
    page: int
    kind: str
    image_path: str
    caption: str
    context: str
    width: int
    height: int


class ClipFigureIndex:
    """CLIP-backed image/page index for figure-aware paper QA."""

    def __init__(self, collection_key: str, qdrant_client: QdrantClient):
        self.collection_key = config.normalize_collection_name(collection_key)
        self.collection_name = config.get_figure_collection_name(self.collection_key)
        self.figure_dir = Path(config.get_figure_dir(self.collection_key))
        self.client = qdrant_client
        self._model = None
        self._vector_size = None

    def _load_model(self):
        if self._model is not None:
            return self._model
        from sentence_transformers import SentenceTransformer

        kwargs = {}
        if config.CLIP_DEVICE:
            kwargs["device"] = config.CLIP_DEVICE
        self._model = SentenceTransformer(config.CLIP_MODEL, **kwargs)
        log_event(logger, "multimodal.clip_model_loaded", model=config.CLIP_MODEL, collection=self.collection_key)
        return self._model

    def _embed_text(self, text: str) -> list[float]:
        model = self._load_model()
        vector = model.encode([text], convert_to_numpy=True, normalize_embeddings=True)[0]
        return vector.astype("float32").tolist()

    def _embed_images(self, image_paths: Iterable[str]) -> list[list[float]]:
        paths = list(image_paths)
        if not paths:
            return []
        model = self._load_model()
        images = []
        for image_path in paths:
            with Image.open(image_path) as image:
                images.append(image.convert("RGB").copy())
        vectors = model.encode(
            images,
            batch_size=config.CLIP_BATCH_SIZE,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )
        return [vector.astype("float32").tolist() for vector in vectors]

    def _get_vector_size(self) -> int:
        if self._vector_size is None:
            self._vector_size = len(self._embed_text("figure"))
        return self._vector_size

    def _ensure_collection(self) -> None:
        if self.client.collection_exists(self.collection_name):
            return
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=qmodels.VectorParams(size=self._get_vector_size(), distance=qmodels.Distance.COSINE),
        )
        log_event(
            logger,
            "multimodal.figure_collection_created",
            collection=self.collection_key,
            vector_collection=self.collection_name,
            vector_size=self._vector_size,
        )

    @staticmethod
    def _caption_candidates(page_text: str) -> str:
        lines = [line.strip() for line in page_text.splitlines() if line.strip()]
        captions = []
        for index, line in enumerate(lines):
            if _CAPTION_START.search(line):
                window = [line]
                for next_line in lines[index + 1 : index + 3]:
                    if _CAPTION_START.search(next_line):
                        break
                    window.append(next_line)
                captions.append(" ".join(window))
        return "\n".join(captions[:8])

    @staticmethod
    def _trim(text: str, max_chars: int) -> str:
        text = re.sub(r"\s+", " ", (text or "")).strip()
        if len(text) <= max_chars:
            return text
        return text[:max_chars].rstrip() + "..."

    @staticmethod
    def _query_terms(text: str) -> set[str]:
        terms = {term for term in re.findall(r"[a-zA-Z0-9]+", (text or "").lower()) if len(term) >= 2}
        chinese = re.findall(r"[\u4e00-\u9fff]{2,}", text or "")
        for item in chinese:
            terms.update(item[index : index + 2] for index in range(max(len(item) - 1, 0)))
        return terms

    @classmethod
    def _caption_boost(cls, query: str, caption: str, context: str) -> float:
        query_terms = cls._query_terms(query)
        if not query_terms:
            return 0.0
        target_terms = cls._query_terms(f"{caption} {context[:500]}")
        overlap = len(query_terms & target_terms)
        return min(0.12, overlap * 0.02)

    def _record_id(self, source: str, kind: str, page: int, index: int) -> str:
        raw = f"{self.collection_key}:{source}:{kind}:{page}:{index}"
        return str(uuid.uuid5(uuid.NAMESPACE_URL, raw))

    def _save_page_screenshot(self, page, output_path: Path) -> tuple[int, int]:
        zoom = config.FIGURE_PAGE_RENDER_DPI / 72
        pixmap = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), alpha=False)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        pixmap.save(str(output_path))
        return pixmap.width, pixmap.height

    def _save_embedded_image(self, doc, xref: int, output_path: Path) -> tuple[int, int] | None:
        try:
            extracted = doc.extract_image(xref)
            image_bytes = extracted.get("image")
            if not image_bytes:
                return None
            output_path.parent.mkdir(parents=True, exist_ok=True)
            temp_path = output_path.with_suffix(f".{extracted.get('ext', 'png')}")
            temp_path.write_bytes(image_bytes)
            with Image.open(temp_path) as image:
                image = image.convert("RGB")
                width, height = image.size
                if width < config.FIGURE_MIN_WIDTH or height < config.FIGURE_MIN_HEIGHT:
                    temp_path.unlink(missing_ok=True)
                    return None
                image.save(output_path)
            if temp_path != output_path:
                temp_path.unlink(missing_ok=True)
            return width, height
        except Exception as exc:
            log_event(logger, "multimodal.embedded_image_extract_failed", collection=self.collection_key, xref=xref, error=str(exc))
            return None

    def extract_pdf_figures(self, pdf_path: str | Path) -> list[FigureRecord]:
        pdf_path = Path(pdf_path)
        source = pdf_path.name
        source_stem = pdf_path.stem
        doc = pymupdf.open(pdf_path)
        output_dir = self.figure_dir / source_stem
        output_dir.mkdir(parents=True, exist_ok=True)
        records: list[FigureRecord] = []
        seen_xrefs: set[int] = set()
        max_pages = min(doc.page_count, config.FIGURE_MAX_PAGES_PER_DOC)

        for page_index in range(max_pages):
            page = doc[page_index]
            page_number = page_index + 1
            page_text = page.get_text("text")
            caption = self._caption_candidates(page_text)
            context = self._trim(page_text, config.FIGURE_CONTEXT_CHARS)

            if config.FIGURE_INDEX_PAGE_SCREENSHOTS:
                image_path = output_dir / f"page_{page_number:03d}.png"
                width, height = self._save_page_screenshot(page, image_path)
                records.append(
                    FigureRecord(
                        id=self._record_id(source, "page", page_number, 0),
                        source=source,
                        page=page_number,
                        kind="page",
                        image_path=str(image_path),
                        caption=caption,
                        context=context,
                        width=width,
                        height=height,
                    )
                )

            if config.FIGURE_INDEX_EMBEDDED_IMAGES:
                for image_index, image_info in enumerate(page.get_images(full=True), start=1):
                    xref = int(image_info[0])
                    if xref in seen_xrefs:
                        continue
                    embedded_width = int(image_info[2] or 0)
                    embedded_height = int(image_info[3] or 0)
                    embedded_pixels = embedded_width * embedded_height
                    if (
                        embedded_width < config.FIGURE_MIN_WIDTH
                        or embedded_height < config.FIGURE_MIN_HEIGHT
                        or embedded_pixels > config.FIGURE_MAX_IMAGE_PIXELS
                    ):
                        log_event(
                            logger,
                            "multimodal.embedded_image_skipped",
                            collection=self.collection_key,
                            source=source,
                            page=page_number,
                            xref=xref,
                            width=embedded_width,
                            height=embedded_height,
                            pixels=embedded_pixels,
                        )
                        seen_xrefs.add(xref)
                        continue
                    seen_xrefs.add(xref)
                    image_path = output_dir / f"image_p{page_number:03d}_{image_index:02d}.png"
                    size = self._save_embedded_image(doc, xref, image_path)
                    if size is None:
                        continue
                    width, height = size
                    records.append(
                        FigureRecord(
                            id=self._record_id(source, "image", page_number, image_index),
                            source=source,
                            page=page_number,
                            kind="image",
                            image_path=str(image_path),
                            caption=caption,
                            context=context,
                            width=width,
                            height=height,
                        )
                    )

        return records

    def index_pdf(self, pdf_path: str | Path) -> dict:
        if not config.MULTIMODAL_ENABLED:
            return {"enabled": False, "indexed": 0, "collection": self.collection_name}

        records = self.extract_pdf_figures(pdf_path)
        if not records:
            return {"enabled": True, "indexed": 0, "collection": self.collection_name}

        self._ensure_collection()
        vectors = self._embed_images(record.image_path for record in records)
        points = []
        for record, vector in zip(records, vectors):
            points.append(
                qmodels.PointStruct(
                    id=record.id,
                    vector=vector,
                    payload={
                        "source": record.source,
                        "page": record.page,
                        "kind": record.kind,
                        "image_path": record.image_path,
                        "caption": record.caption,
                        "context": record.context,
                        "width": record.width,
                        "height": record.height,
                    },
                )
            )
        self.client.upsert(collection_name=self.collection_name, points=points)
        log_event(
            logger,
            "multimodal.figures_indexed",
            collection=self.collection_key,
            vector_collection=self.collection_name,
            file=Path(pdf_path).name,
            indexed=len(points),
        )
        return {"enabled": True, "indexed": len(points), "collection": self.collection_name}

    def search(self, query: str, limit: int = 5) -> list[dict]:
        if not config.MULTIMODAL_ENABLED:
            return []
        if not self.client.collection_exists(self.collection_name):
            return []
        vector = self._embed_text(query)
        try:
            candidate_limit = max(limit, min(limit * 8, 50))
            response = self.client.query_points(
                collection_name=self.collection_name,
                query=vector,
                limit=candidate_limit,
                with_payload=True,
            )
            points = response.points
        except AttributeError:
            points = self.client.search(
                collection_name=self.collection_name,
                query_vector=vector,
                limit=max(limit, min(limit * 8, 50)),
                with_payload=True,
            )
        results = []
        for point in points:
            payload = point.payload or {}
            image_path = payload.get("image_path", "")
            image_url = ""
            if image_path:
                try:
                    rel_path = Path(image_path).resolve().relative_to(Path(config.FIGURE_ROOT_DIR).resolve())
                    image_url = f"/figures/files/{rel_path.as_posix()}"
                except ValueError:
                    image_url = ""
            clip_score = float(getattr(point, "score", 0.0) or 0.0)
            boost = self._caption_boost(query, payload.get("caption", ""), payload.get("context", ""))
            results.append(
                {
                    "score": clip_score + boost,
                    "clip_score": clip_score,
                    "caption_boost": boost,
                    "source": payload.get("source", ""),
                    "page": payload.get("page", ""),
                    "kind": payload.get("kind", ""),
                    "image_path": image_path,
                    "image_url": image_url,
                    "caption": payload.get("caption", ""),
                    "context": payload.get("context", ""),
                    "width": payload.get("width", 0),
                    "height": payload.get("height", 0),
                }
            )
        results.sort(key=lambda item: item["score"], reverse=True)
        results = results[:limit]
        log_event(
            logger,
            "multimodal.figures_searched",
            collection=self.collection_key,
            vector_collection=self.collection_name,
            query=query,
            limit=limit,
            result_count=len(results),
        )
        return results

    def search_to_text(self, query: str, limit: int = 5) -> str:
        results = self.search(query=query, limit=limit)
        if not results:
            return "NO_RELEVANT_FIGURES"
        blocks = []
        for item in results:
            blocks.append(
                "Figure Result\n"
                f"File Name: {item['source']}\n"
                f"Page: {item['page']}\n"
                f"Kind: {item['kind']}\n"
                f"Hybrid Score: {item['score']:.4f}\n"
                f"CLIP Score: {item['clip_score']:.4f}\n"
                f"Caption Boost: {item['caption_boost']:.4f}\n"
                f"Image Path: {item['image_path']}\n"
                f"Image URL: {item['image_url'] or 'n/a'}\n"
                f"Caption: {item['caption'] or 'n/a'}\n"
                f"Nearby Page Text: {item['context'] or 'n/a'}"
            )
        return "\n\n".join(blocks)

    def clear(self) -> None:
        if self.client.collection_exists(self.collection_name):
            self.client.delete_collection(self.collection_name)
        if self.figure_dir.exists():
            shutil.rmtree(self.figure_dir)
            self.figure_dir.mkdir(parents=True, exist_ok=True)
        log_event(logger, "multimodal.figures_cleared", collection=self.collection_key, vector_collection=self.collection_name)
