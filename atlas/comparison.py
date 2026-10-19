"""Controlled toy comparison of verified rule retrieval against no memory.

Important: This measures the toy rule-retrieval mechanism, NOT LLM learning.
"""
import json
from .memory import VerifiedMemory

TRAIN = (
    ("T1", "addition", "compute_sum"),
    ("T2", "multiplication", "compute_product"),
    ("T3", "subtraction", "compute_difference"),
)
HOLDOUT = (
    ("H1", "addition", 7, 11, 18),
    ("H2", "addition", -3, 8, 5),
    ("H3", "multiplication", 6, 9, 54),
    ("H4", "multiplication", -4, 5, -20),
    ("H5", "subtraction", 20, 3, 17),
    ("H6", "subtraction", 8, 15, -7),
)


def attempt(operation, a, b, rule):
    """Fallback is deliberately weak and identical in both arms."""
    if rule == "compute_sum" and operation == "addition":
        return a + b
    if rule == "compute_product" and operation == "multiplication":
        return a * b
    if rule == "compute_difference" and operation == "subtraction":
        return a - b
    return 0


def compare(memory=None):
    owns_memory = memory is None
    if owns_memory:
        memory = VerifiedMemory()
    try:
        for identifier, operation, rule in TRAIN:
            # Only explicitly validated rules are admitted.
            if memory.retrieve(operation) is None:
                memory.add_verified(identifier, operation, rule)
        samples = []
        for identifier, operation, a, b, answer in HOLDOUT:
            baseline = attempt(operation, a, b, None)
            enriched = attempt(operation, a, b, memory.retrieve(operation))
            samples.append({
                "id": identifier, "baseline_correct": baseline == answer,
                "memory_correct": enriched == answer,
            })
        return {
            "experiment": "EXP-002-rule-retrieval-demo",
            "disclaimer": "Toy rule lookup only; not evidence of an AI learning",
            "train_ids": [x[0] for x in TRAIN],
            "holdout_ids": [x[0] for x in HOLDOUT],
            "baseline_correct": sum(x["baseline_correct"] for x in samples),
            "memory_correct": sum(x["memory_correct"] for x in samples),
            "total": len(samples), "samples": samples,
        }
    finally:
        if owns_memory:
            memory.close()


if __name__ == "__main__":
    print(json.dumps(compare(), indent=2))
