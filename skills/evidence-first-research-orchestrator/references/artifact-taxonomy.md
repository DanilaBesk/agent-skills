# Artifact Taxonomy

This workflow keeps the artifact model intentionally small.

| Artifact | Purpose | Owner | Retained |
| --- | --- | --- | --- |
| `evidence-research-state.md` | Shared run state plus the source ledger, subresearch index, iteration-review log, prompt backlog, normalization queue, corpus target tracking, and final coverage tracker | main orchestrator, with append-only subagent updates | yes |
| `evidence-subresearch/` | Folder of one markdown file per subagent run across discovery, iteration review, contradiction checks, normalization batches, and synthesis challenge passes; serious runs choose their scale adaptively inside `10-300` and should bias upward on complex topics | subagents, indexed in the shared state file | yes |
| `evidence-research-final-report.md` | Canonical deep normalized research document built after full-file normalization coverage | main orchestrator | yes |

## Default Rule

Do not create separate retained artifacts for:

- claim registries
- source registries
- evidence registries
- wave logs
- contradiction logs
- verification checklists
- gap logs
- comparative matrices
- graph exports

If a run truly needs one of those structures, embed the needed material either inside the state file or inside the final report appendix instead of creating a new retained sidecar by default.

## Retention Rule

Keep all three artifacts unless the user explicitly asks for cleanup.

Do not delete the state file or subresearch folder after the final report is finished.
They are part of the evidence trail.
