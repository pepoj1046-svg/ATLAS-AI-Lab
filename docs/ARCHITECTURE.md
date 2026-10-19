# ATLAS v0.1 — architecture and guardrails

ATLAS is an **experimental**, supervised research laboratory. The first milestone is a deterministic evaluator and reproducible test suite, **not** a self-improving autonomous agent.

## Milestones
1. Bounded arithmetic evaluator and baseline tests.
2. Versioned, verified experiment records with provenance.
3. Baseline vs. memory-enabled agent evaluation on held-out cases.
4. Optional independent Supabase storage with RLS and explicit authorization.
5. Isolated execution of untrusted candidate programs in an approved sandbox.

## Safety and cost controls
- No paid services, external writes, secrets, or unattended agent operations without explicit approval.
- Never execute generated programs on a CI runner with repository tokens or secrets.
- Current arithmetic evaluator processes a tiny allowlisted AST; it is **not** a general Python sandbox.
- No network access needed for the baseline benchmark.
- GitHub Actions workflow uses standard ubuntu-latest, read-only token permissions, and five-minute timeout.
- The published source may be public; deployment keys, private data and experiment credentials must remain private.
- Supabase database is intentionally not connected or modified in v0.1.

## Experiment method
Keep training/memory cases disjoint from holdout evaluation. Use the same underlying model and budget for baseline and memory-enabled experiments. Store task IDs, seeds, model versions, scores, and failures. Avoid claiming learning from an improvement without repeatable controls.
