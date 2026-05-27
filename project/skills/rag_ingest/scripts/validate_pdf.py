from pathlib import Path
import sys


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: validate_pdf.py <path>")
        return 2
    path = Path(sys.argv[1])
    if not path.exists():
        print(f"missing: {path}")
        return 1
    if path.suffix.lower() != ".pdf":
        print(f"not_pdf: {path}")
        return 1
    with path.open("rb") as handle:
        header = handle.read(5)
    if header != b"%PDF-":
        print(f"invalid_pdf_header: {path}")
        return 1
    print(f"ok: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

