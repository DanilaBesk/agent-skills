# Repository Instructions

## Purpose

This repository is the source workspace for custom agent skills.

## Conventions

- Put each skill in `skills/<skill-name>/`.
- Each skill must have a `SKILL.md` file at its root.
- Keep reusable examples or templates inside the skill folder.
- Prefer changing the repository copy first, then sync into `~/.agents/skills/`.
- Do not edit generated or copied global skill folders directly when a repository source exists.

## Verification

- Run `git diff --check` before committing.
- After changing markdown links, run a link checker if one is added to this repository.
- For `evidence-first-research-orchestrator`, prefer using its skill-local scripts instead of ad hoc state editing:

```bash
python3 skills/evidence-first-research-orchestrator/scripts/validate_research_run.py --state <path-to-state>
python3 skills/evidence-first-research-orchestrator/scripts/update_state.py --state <path-to-state> --section <section> --row '<markdown-table-row>'
```

- After syncing a skill, compare repo and global copies with:

```bash
diff -qr skills/<skill-name> ~/.agents/skills/<skill-name>
```
