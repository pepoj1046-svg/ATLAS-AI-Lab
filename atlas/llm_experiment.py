"""Optional live evaluation. Requires a user-configured model; never run in CI."""
import json
from .model import ask_model
from .evaluator import arithmetic, check_answer

# All prompts are evaluation-only; no training samples in this file.
CASES = (("E1", "17 + 24"), ("E2", "8 * 13"), ("E3", "50 - 19"))


def evaluate(context=""):
    results = []
    for case_id, expression in CASES:
        answer = ask_model(f"Compute {expression}. Return only a number.", context=context)
        try:
            is_correct = check_answer(expression, float(answer.strip()))
        except (ValueError, OverflowError):
            is_correct = False
        results.append({"id": case_id, "correct": is_correct})
    return {"context_enabled": bool(context), "correct": sum(r["correct"] for r in results),
            "total": len(results), "results": results}


if __name__ == "__main__":
    raise SystemExit("Live inference is opt-in. Import evaluate() only after configuring an approved provider.")
