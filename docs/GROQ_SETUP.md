# ATLAS v0.4 — Optional GroqCloud research profile

The code includes a GroqCloud endpoint profile, but **no model calls have been made**.
The user must review the provider's current free-plan limits and terms, open a
free account, and provide a key via a private environment variable. Do not paste
keys into chat, issues, pull requests or source code.

- Provider: https://console.groq.com/
- Model: `openai/gpt-oss-20b`
- Endpoint: `https://api.groq.com/openai/v1/chat/completions`
- Conservative experiment ceiling: 20 requests (not a cost guarantee).
- Current provider limits: https://console.groq.com/docs/rate-limits

Set `ATLAS_MODEL_ENDPOINT`, `ATLAS_MODEL_NAME`, and `ATLAS_MODEL_API_KEY`
privately. Do not set or commit these in GitHub Actions: CI uses mocks only.

Call `run_paired(ask_model)` from a trusted environment after approval.
Both groups share the same tasks, model and inference settings; only reference
context changes. A true memory-learning study still requires verified
task-specific memory, order randomization, multiple seeds and larger held-out
benchmarks. No automation or paid tier is enabled.
