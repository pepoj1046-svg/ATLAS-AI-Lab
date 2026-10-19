"""Fair paired experiment harness: identical tasks, model and parameters.

It does not contact a provider unless an explicit caller supplies ask().
Real-world improvements are not claimed by this harness.
"""
from dataclasses import dataclass
from .evaluator import check_answer

TASKS = (
    ("P1", "13 + 29"),
    ("P2", "72 - 38"),
    ("P3", "9 * 17"),
    ("P4", "144 / 12"),
)
VERIFIED_CONTEXT = "Use ordinary arithmetic. Return a single number; do not include any explanation."

@dataclass(frozen=True)
class Trial:
    case_id: str
    arm: str
    correct: bool

def run_paired(ask, cases=TASKS, memory_context=VERIFIED_CONTEXT, max_requests=20):
    if len(cases) * 2 > max_requests:
        raise ValueError("Experiment exceeds its request ceiling")
    trials = []
    for case_id, expression in cases:
        for arm, context in (("baseline", ""), ("memory", memory_context)):
            raw = ask(f"Compute {expression}. Reply with only a number.", context)
            try:
                correct = check_answer(expression, float(raw.strip()))
            except (ValueError, OverflowError, TypeError, AttributeError):
                correct = False
            trials.append(Trial(case_id, arm, correct))
    return {
        "requests": len(trials),
        "total_per_arm": len(cases),
        "baseline_correct": sum(x.correct for x in trials if x.arm == "baseline"),
        "memory_correct": sum(x.correct for x in trials if x.arm == "memory"),
        "trials": [x.__dict__ for x in trials],
        "limitations": "Prompts differ by context; repeat with randomized arm order and independent held-out tasks before claiming improvement.",
    }
