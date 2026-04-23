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
