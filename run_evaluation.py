"""Run a small illustrative local evaluation; this is NOT an official benchmark run."""
import csv
import json
import time
from pathlib import Path

from src.graph import build_graph

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "sample_questions.json"
OUTPUT_PATH = ROOT / "results" / "benchmark_results.csv"


def normalize(text: str) -> str:
    return " ".join(text.lower().strip().split())


def main() -> None:
    examples = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    graph = build_graph()
    rows = []

    for item in examples:
        start = time.perf_counter()
        result = graph.invoke({"question": item["question"]})
        latency_ms = round((time.perf_counter() - start) * 1000, 2)
        expected = item.get("expected_contains", "").strip()
        answer = result.get("final_answer", "")
        passed = bool(expected) and normalize(expected) in normalize(answer)
        rows.append({
            "id": item["id"],
            "category": item["category"],
            "route": result.get("route", ""),
            "model_used": result.get("model_used", "unknown"),
            "latency_ms": latency_ms,
            "illustrative_check_passed": passed,
            "input_tokens": result.get("input_tokens", ""),
            "output_tokens": result.get("output_tokens", ""),
            "note": "Illustrative local sample; not an official benchmark score",
        })

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    pass_rate = sum(row["illustrative_check_passed"] for row in rows) / len(rows) if rows else 0
    print(f"Examples evaluated: {len(rows)}")
    print(f"Illustrative exact-substring check pass rate: {pass_rate:.1%}")
    print("This is not an official MMLU/GPQA/HumanEval/SWE-bench/TruthfulQA result.")
    print(f"Saved CSV: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
