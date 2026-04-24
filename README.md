# Agent Skills

Personal skill development repository for Codex and agent workflows.

## Layout

- `skills/` contains installable skill folders.
- `scripts/sync-skill.sh` copies one skill from this repository into the global `~/.agents/skills/` directory.

## Included Skills

- `evidence-first-research-orchestrator`: long-running evidence-first research workflow with adaptive subagent batches, reviewer-guided prompt loops, large discovery corpora, and iterative normalization into one final report.

## Common Commands

```bash
./scripts/sync-skill.sh evidence-first-research-orchestrator
```

This updates `~/.agents/skills/evidence-first-research-orchestrator` from the repository copy.

```bash
python3 skills/evidence-first-research-orchestrator/scripts/validate_research_run.py \
  --state skills/evidence-first-research-orchestrator/examples/sample-run/evidence-research-state.md
```

```bash
python3 skills/evidence-first-research-orchestrator/scripts/update_state.py \
  --state skills/evidence-first-research-orchestrator/examples/sample-run/evidence-research-state.md \
  --section source_ledger \
  --row '| src-example-3 | Conflict Handling Note | https://example.com/conflict-note | web-doc | d-w02-a02-conflict-handling | w02 | new | 2026-04-24T15:00:00+03:00 | helper dry-run example |' \
  --dry-run
```
