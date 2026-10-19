"""Approved zero-cost provider profile; does not make API requests."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ModelProfile:
    name: str
    endpoint: str
    model: str
    request_ceiling: int

GROQ_FREE = ModelProfile(
    name="GroqCloud free (opt-in)",
    endpoint="https://api.groq.com/openai/v1/chat/completions",
    model="openai/gpt-oss-20b",
    request_ceiling=20,
)

def chosen_profile():
    """A conservative per-experiment limit, not a provider billing guarantee."""
    return GROQ_FREE
