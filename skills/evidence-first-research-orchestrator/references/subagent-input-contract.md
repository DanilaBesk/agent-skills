# Subagent Input Contract

One packet equals one role, one bounded objective, and one output file.

## Required Fields

- `run_id`
- `stage`
- `wave_id`
- `agent_id`
- `role`
- `objective`
- `file_class`
- `topic_slice`
- `output_path`
- `state_file_path`
- `state_update_scope`
- `reviewed_file_ids`
- `prompt_output_target`
- `theme_drift_limit`
- `source_priority_order`
- `source_keys_to_avoid`
- `assigned_file_ids`
- `acceptance_criteria`
- `stop_conditions`
- `prohibited_moves`

## Packaging Rules

1. Every packet must point the worker to the shared state file.
2. Every packet must produce exactly one markdown file in `evidence-subresearch/`.
3. Every packet must require a direct append to the shared state file after the output file is written.
4. Collection packets should target unexplored angles and avoid already-saturated source keys from the state file.
5. After every research batch, an `iteration-reviewer` packet must receive the latest `reviewed_file_ids`.
6. Reviewer packets must ask for `3-5` next prompts unless the worker is explicitly evaluating whether to shift stages.
7. Reviewer packets must include a `theme_drift_limit` that allows slight bounded drift but not topic abandonment.
8. Normalization packets must receive a disjoint file set through `assigned_file_ids`.
9. Final-synthesis packets must name which files or themes they are challenging or reconstructing.
10. Packets should be specific enough that another worker would not duplicate the same search path by accident.
11. Do not ask a subagent to write the whole report unless the packet is explicitly for `final-synthesizer` and the state file shows normalization is complete.
12. Every packet should name the expected file-id pattern so the worker does not invent incompatible naming.

## Template

```text
Run: <run-id>
Stage: <stage-name>
Wave: <wave-id>
Agent: <agent-id>
Role: <role-name>
Objective: <one bounded objective>
File class: <discovery|review|normalization|synthesis|critique>
Topic slice: <one narrow angle or one assigned file batch>
Output path: evidence-subresearch/<file-name>.md
Expected file id pattern: <for example `d-w07-a03-standards-gap`>
State file path: evidence-research-state.md
State update scope:
- append one Subresearch Index row
- append reviewed Source Ledger rows
- append review-log and prompt-backlog rows when this is a review packet
- do not rewrite counters or other file rows

Reviewed file IDs:
- <latest file ids for a reviewer or `none` for fresh collection>

Prompt output target:
- <`3-5` for reviewer packets, otherwise `n/a`>

Theme drift limit:
- <how far the worker may deviate while staying anchored to the core topic>

Source priority order:
1. <preferred source family>
2. <secondary source family>

Source keys to avoid:
- <source-key already covered>

Assigned file IDs:
- <file-id or `none` for fresh collection>

Acceptance criteria:
- <what makes this file usable>
- include at least one concrete datapoint, quote fragment, or exact source-grounded note per material finding when the source permits it

Stop conditions:
- <when the worker must return with partial or blocked status>

Prohibited moves:
- no final recommendation
- no source-free summary
- no duplicate-heavy browsing without explicit reason
- no editing other agents' files
```
