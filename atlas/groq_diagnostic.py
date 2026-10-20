"""Single-request opt-in API check. No secrets or model replies are logged."""
import os
from .model import ask_model, ModelUnavailable

def main():
    if os.environ.get("ATLAS_MODEL_ENDPOINT") != "https://api.groq.com/openai/v1/chat/completions":
        raise SystemExit("Unexpected endpoint")
    if os.environ.get("ATLAS_MODEL_NAME") != "openai/gpt-oss-20b":
        raise SystemExit("Unexpected model")
    if not os.environ.get("ATLAS_MODEL_API_KEY"):
        raise SystemExit("Missing GROQ_API_KEY repository secret")
    try:
        result = ask_model("Return exactly the digit 4 as a plain number.")
    except ModelUnavailable as exc:
        # Message deliberately excludes response bodies, request headers, keys and URLs.
        raise SystemExit(str(exc)) from None
    if result.strip() == "4":
        print("GROQ_DIAGNOSTIC_OK: authenticated inference returned expected answer.")
    else:
        print("GROQ_DIAGNOSTIC_REACHABLE: inference worked, response differed from expected.")
if __name__ == "__main__":
    main()
