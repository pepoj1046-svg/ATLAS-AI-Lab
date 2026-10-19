"""Explicitly-triggered bounded Groq experiment (eight model requests max).

Never writes credentials to stdout, files, or databases. Inference exceptions
are sanitized by atlas.model; no untrusted generated code is run.
"""
import json
import os
from .model import ask_model
from .paired_study import run_paired


def main():
    if os.environ.get("ATLAS_MODEL_ENDPOINT") != "https://api.groq.com/openai/v1/chat/completions":
        raise SystemExit("Only the approved fixed Groq endpoint is allowed")
    if os.environ.get("ATLAS_MODEL_NAME") != "openai/gpt-oss-20b":
        raise SystemExit("Unexpected model configuration")
    if not os.environ.get("ATLAS_MODEL_API_KEY"):
        raise SystemExit("Missing API key; no experiment started")
    results = run_paired(ask_model, max_requests=8)
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
