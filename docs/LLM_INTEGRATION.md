# Optional model integration (ATLAS v0.3)

ATLAS ships without a model or paid API. The connector supports a user-provided
OpenAI-compatible HTTPS `chat/completions` endpoint.

Set three **private local environment variables**:
- `ATLAS_MODEL_ENDPOINT`: complete HTTPS inference endpoint URL
- `ATLAS_MODEL_NAME`: model identifier required by the provider
- `ATLAS_MODEL_API_KEY`: secret provided by that provider

Never commit tokens, add them to issues, or send them through chat.
**No model has been selected or contacted**. Verify provider pricing, privacy,
terms and quotas before explicitly enabling inference.

`atlas.llm_experiment.evaluate(context="")` runs three arithmetic evaluation
cases. To produce a meaningful with-vs-without-memory study, hold the model
identifier, decoding parameters and test set constant, run multiple trials,
and pass verified context only in the memory arm. This module is an adapter,
not evidence of measurable improvement.

## Boundaries
- CI tests mock the model and never make requests.
- No credentials are required for CI.
- No automatic model calls, external writes, or periodic runs.
- HTTPS is required; the basic URL filter is not a full SSRF defense.
- Use a trusted, explicitly approved provider endpoint only.
- Network inference should ultimately run from a dedicated hardened service.
