"""A deterministic benchmark; no model credentials or external services needed."""
import json
from datetime import datetime, timezone
from pathlib import Path
from .evaluator import arithmetic, check_answer

CASES = (
    {"id": "M001", "expression": "7 * (3 + 5)", "candidate": 56},
    {"id": "M002", "expression": "81 / 9 + 4", "candidate": 13},
    {"id": "M003", "expression": "2 ** 6 - 1", "candidate": 63},
    {"id": "M004", "expression": "12 * 4 - 3", "candidate": 46},
)


def run_benchmark(cases=CASES):
    results = []
    for case in cases:
        expected = arithmetic(case["expression"])
        passed = check_answer(case["expression"], case["candidate"])
        results.append({"id": case["id"], "expression": case["expression"],
                        "candidate": case["candidate"], "expected": expected,
                        "passed": passed})
    return {"schema_version": 1, "experiment": "EXP-001-smoke-test",
            "evaluated_at": datetime.now(timezone.utc).isoformat(),
            "correct": sum(int(r["passed"]) for r in results),
            "total": len(results), "results": results}


def save_report(path: str, report: dict):
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    result = run_benchmark()
    print(json.dumps(result, indent=2))
