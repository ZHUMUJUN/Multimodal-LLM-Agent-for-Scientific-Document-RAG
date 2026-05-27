import logging
import shutil
from pathlib import Path

import config
from core.logging_utils import log_event
from utils import pdfs_to_markdowns

logger = logging.getLogger(__name__)


class DocumentManager:

    def __init__(self, rag_system):
        self.rag_system = rag_system
        self.markdown_dir = Path(rag_system.markdown_dir)
        self.markdown_dir.mkdir(parents=True, exist_ok=True)

    def add_documents(self, document_paths, progress_callback=None):
        if not document_paths:
            return 0, 0

        document_paths = [document_paths] if isinstance(document_paths, str) else document_paths
        document_paths = [p for p in document_paths if p and Path(p).suffix.lower() in [".pdf", ".md"]]

        if not document_paths:
            return 0, 0

        added = 0
        skipped = 0

        for i, doc_path in enumerate(document_paths):
            file_name = Path(doc_path).name
            if progress_callback:
                progress_callback((i + 1) / len(document_paths), f"Processing {file_name}")

            doc_name = Path(doc_path).stem
            md_path = self.markdown_dir / f"{doc_name}.md"
            is_pdf = Path(doc_path).suffix.lower() == ".pdf"

            if md_path.exists():
                self._index_figures_if_available(doc_path)
                skipped += 1
                log_event(logger, "documents.skipped_existing", collection=self.rag_system.collection_key, file=file_name)
                continue

            try:
                if not is_pdf:
                    shutil.copy(doc_path, md_path)
                else:
                    pdfs_to_markdowns(str(doc_path), output_dir=str(self.markdown_dir), overwrite=False)
                    self._index_figures_if_available(doc_path)

                parent_chunks, child_chunks = self.rag_system.chunker.create_chunks_single(md_path)

                if not child_chunks:
                    skipped += 1
                    log_event(logger, "documents.skipped_empty", collection=self.rag_system.collection_key, file=file_name)
                    continue

                collection = self.rag_system.vector_db.get_collection(self.rag_system.collection_name)
                collection.add_documents(child_chunks)
                self.rag_system.parent_store.save_many(parent_chunks)

                added += 1
                log_event(
                    logger,
                    "documents.ingested",
                    collection=self.rag_system.collection_key,
                    file=file_name,
                    parent_chunks=len(parent_chunks),
                    child_chunks=len(child_chunks),
                )

            except Exception as exc:
                skipped += 1
                log_event(
                    logger,
                    "documents.ingest_failed",
                    collection=self.rag_system.collection_key,
                    file=file_name,
                    error=str(exc),
                )

        return added, skipped

    def _index_figures_if_available(self, doc_path) -> None:
        if not config.MULTIMODAL_ENABLED:
            return
        if Path(doc_path).suffix.lower() != ".pdf":
            return
        figure_index = getattr(self.rag_system, "figure_index", None)
        if figure_index is None:
            return
        try:
            result = figure_index.index_pdf(doc_path)
            log_event(
                logger,
                "documents.figures_indexed",
                collection=self.rag_system.collection_key,
                file=Path(doc_path).name,
                indexed=result.get("indexed", 0),
            )
        except Exception as exc:
            log_event(
                logger,
                "documents.figure_index_failed",
                collection=self.rag_system.collection_key,
                file=Path(doc_path).name,
                error=str(exc),
            )

    def get_markdown_files(self):
        if not self.markdown_dir.exists():
            return []
        return sorted([p.name.replace(".md", ".pdf") for p in self.markdown_dir.glob("*.md")])

    def clear_all(self):
        if self.markdown_dir.exists():
            shutil.rmtree(self.markdown_dir)
            self.markdown_dir.mkdir(parents=True, exist_ok=True)

        self.rag_system.parent_store.clear_store()
        self.rag_system.vector_db.delete_collection(self.rag_system.collection_name)
        self.rag_system.vector_db.create_collection(self.rag_system.collection_name)
        if getattr(self.rag_system, "figure_index", None) is not None:
            self.rag_system.figure_index.clear()
        log_event(logger, "documents.cleared", collection=self.rag_system.collection_key)
