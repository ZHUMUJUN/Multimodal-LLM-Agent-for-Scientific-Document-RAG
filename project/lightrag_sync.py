import argparse
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

import config
from core.lightrag_client import LightRAGClient


def parse_args():
    parser = argparse.ArgumentParser(description="Sync an existing markdown collection into LightRAG.")
    parser.add_argument("--collection", default="public_light_pollution_corpus", help="Collection name under project/markdown_docs.")
    parser.add_argument("--clear-first", action="store_true", help="Clear existing LightRAG documents before syncing.")
    parser.add_argument("--batch-size", type=int, default=4, help="How many markdown docs to send per batch.")
    parser.add_argument("--wait-timeout", type=int, default=config.LIGHTRAG_TIMEOUT_SECONDS, help="Seconds to wait for indexing to become idle.")
    return parser.parse_args()


def main():
    args = parse_args()
    client = LightRAGClient()
    docs = client.load_markdown_collection(args.collection)
    if not docs:
        raise SystemExit(f"No markdown files found for collection: {args.collection}")

    if args.clear_first:
        print(client.clear_documents())
        client.wait_until_idle(timeout_seconds=args.wait_timeout)

    for start in range(0, len(docs), args.batch_size):
        batch = docs[start : start + args.batch_size]
        texts = [text for text, _source in batch]
        file_sources = [source for _text, source in batch]
        response = client.insert_texts(texts=texts, file_sources=file_sources)
        print(response)

    final_status = client.wait_until_idle(timeout_seconds=args.wait_timeout)
    print(final_status)


if __name__ == "__main__":
    main()
