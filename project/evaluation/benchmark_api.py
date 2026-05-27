import argparse
import json
import statistics
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib import request


PROMPTS = [
    "列出当前集合有哪些文件。",
    "总结人工夜空亮度增加的主要驱动因素。",
    "哪篇文档把 artificial light at night 描述为 global disruptor？",
    "比较两篇文档对 LED 光谱变化的描述差异。",
    "哪些因素会影响自然夜空亮度？",
    "如果问题涉及跨文档关系，系统更适合走哪种检索模式？",
]


def _post(url: str, payload: dict) -> dict:
    started = time.perf_counter()
    req = request.Request(
        url=url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with request.urlopen(req, timeout=300) as response:
        body = json.loads(response.read().decode("utf-8"))
        return {
            "status": response.status,
            "latency_ms": round((time.perf_counter() - started) * 1000, 2),
            "answer_length": len((body.get("answer") or "")),
            "resolved_retrieval_mode": body.get("resolved_retrieval_mode"),
        }


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark the Agentic RAG /chat API.")
    parser.add_argument("--base-url", default="http://127.0.0.1:8001")
    parser.add_argument("--collection", default="default")
    parser.add_argument("--concurrency", type=int, default=5)
    parser.add_argument("--repeat", type=int, default=3)
    parser.add_argument("--output", default="project/evaluation/reports/api_benchmark.json")
    args = parser.parse_args()

    requests_payloads = [{"collection": args.collection, "message": prompt} for prompt in PROMPTS for _ in range(args.repeat)]
    url = f"{args.base_url.rstrip('/')}/chat"

    started = time.perf_counter()
    with ThreadPoolExecutor(max_workers=args.concurrency) as executor:
        results = list(executor.map(lambda payload: _post(url, payload), requests_payloads))
    total_seconds = time.perf_counter() - started

    latencies = [item["latency_ms"] for item in results]
    payload = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "base_url": args.base_url,
        "request_count": len(results),
        "concurrency": args.concurrency,
        "qps": round(len(results) / max(total_seconds, 1e-6), 2),
        "success_rate": round(sum(1 for item in results if item["status"] == 200) / max(len(results), 1), 4),
        "avg_latency_ms": round(statistics.mean(latencies), 2) if latencies else 0.0,
        "p95_latency_ms": round(sorted(latencies)[max(int(len(latencies) * 0.95) - 1, 0)], 2) if latencies else 0.0,
        "avg_answer_length": round(statistics.mean(item["answer_length"] for item in results), 2) if results else 0.0,
        "route_distribution": {
            mode: sum(1 for item in results if item.get("resolved_retrieval_mode") == mode)
            for mode in sorted({item.get("resolved_retrieval_mode") for item in results if item.get("resolved_retrieval_mode")})
        },
        "results": results,
    }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(output_path)


if __name__ == "__main__":
    main()
