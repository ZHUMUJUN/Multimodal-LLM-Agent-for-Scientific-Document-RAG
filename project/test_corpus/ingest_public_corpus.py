import argparse
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

import fitz
from services.platform_service import PlatformService


DEFAULT_COLLECTION = "public_light_pollution_corpus"
MARKDOWN_CACHE_DIR = Path(__file__).resolve().parent / "markdown_cache"
VALIDATED_FILES = [
    "05_cbd_artificial_light_at_night_biodiversity.pdf",
    "06_cambridge_turtle_conservation_light_glow.pdf",
    "08_artificial_light_at_night_global_disruptor_arxiv.pdf",
    "09_world_atlas_artificial_night_sky_brightness_arxiv.pdf",
    "10_natural_night_sky_brightness_gaia_arxiv.pdf",
    "11_anthropogenic_photons_light_pollution_arxiv.pdf",
    "12_space_objects_artificial_night_sky_brightness_arxiv.pdf",
    "13_dancing_sky_paranal_observations_arxiv.pdf",
]


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Ingest the validated public PDF corpus into a collection.")
    parser.add_argument("--collection", default=DEFAULT_COLLECTION, help="Target collection name.")
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Clear the target collection before ingesting the corpus.",
    )
    return parser


def pdf_to_markdown_text(pdf_path: Path, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf_path)
    lines = [f"# {pdf_path.stem}", ""]
    try:
        for page_number, page in enumerate(doc, start=1):
            text = page.get_text("text").strip()
            if not text:
                continue
            lines.append(f"## Page {page_number}")
            lines.append("")
            lines.append(text)
            lines.append("")
    finally:
        doc.close()

    output_path = output_dir / f"{pdf_path.stem}.md"
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


def build_markdown_cache(pdf_paths: list[Path]) -> list[Path]:
    converted_paths: list[Path] = []
    for pdf_path in pdf_paths:
        converted_paths.append(pdf_to_markdown_text(pdf_path, MARKDOWN_CACHE_DIR))
    return converted_paths


def main() -> None:
    args = build_argument_parser().parse_args()
    pdf_dir = Path(__file__).resolve().parent / "pdfs"
    document_paths = [pdf_dir / name for name in VALIDATED_FILES]
    missing = [str(path) for path in document_paths if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing validated corpus files: {missing}")

    service = PlatformService()

    if args.clear:
        service.clear_collection(args.collection)

    markdown_paths = build_markdown_cache(document_paths)
    result = service.add_documents(args.collection, [str(path) for path in markdown_paths])

    print(f"collection={result['collection']}")
    print(f"added={result['added']}")
    print(f"skipped={result['skipped']}")
    print("documents:")
    for name in result["documents"]:
        print(f"- {name}")


if __name__ == "__main__":
    main()
