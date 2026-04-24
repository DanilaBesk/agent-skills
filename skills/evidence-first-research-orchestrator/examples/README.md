# Examples

This folder contains a compact sample run for the `evidence-first-research-orchestrator` skill.

## Included Example

- `sample-run/` shows:
  - a realistic `evidence-research-state.md`
  - a discovery subresearch file
  - a reviewer subresearch file
  - a normalization subresearch file
  - a minimal final report

## Useful Commands

```bash
python3 ../scripts/validate_research_run.py --state sample-run/evidence-research-state.md
```

```bash
python3 ../scripts/update_state.py \
  --state sample-run/evidence-research-state.md \
  --section source_ledger \
  --row '| src-example-3 | Conflict Handling Note | https://example.com/conflict-note | web-doc | d-w02-a02-conflict-handling | w02 | new | 2026-04-24T15:00:00+03:00 | helper dry-run example |' \
  --dry-run
```
