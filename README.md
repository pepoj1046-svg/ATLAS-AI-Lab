# ATLAS AI Lab

Open-source, supervised AI research laboratory focused on **verifiable experiments** and evidence-backed memory. Apache-2.0 licensed.

## Status: v0.1 (bootstrap)
This is an intentionally small baseline, **not** an autonomous agent or trained AI. No Supabase integration, paid inference, or unrestricted code execution is enabled.

### Local verification
Requires Python 3.11+; no third-party packages or API keys.

```bash
python -m unittest discover -s tests -v
python -m atlas.experiment
```

The smoke benchmark evaluates four candidate answers, three correct and one deliberately incorrect. It is a test of the evaluator, not evidence of agent learning.

## Roadmap
1. Verified experiment records and persistence.
2. Baseline and memory-enabled agent adapters.
3. Controlled held-out benchmarks to measure actual improvement.
4. Optional standalone Supabase project and dashboard.

See [architecture and safety notes](docs/ARCHITECTURE.md).

## Safety and governance
Experiment actions stay supervised. Do not commit secrets. No spending, external service deployment or changes to unrelated repositories without explicit authorization.
