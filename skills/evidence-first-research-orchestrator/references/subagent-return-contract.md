# Subagent Return Contract

Every delegated worker returns exactly one markdown file inside `evidence-subresearch/`.

## Required File Shape

```md
# Subresearch File <file-id>

run_id:
stage:
wave_id:
agent_id:
role:
file_class:
topic_slice:
reviewed_file_ids:
status:
state_append_status:
created_at:

## Summary

- <what was actually learned>

## Sources Reviewed

| source_key | title | url_or_path | source_family | authority | checked_at | novelty | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Findings

### F1
- claim_or_observation:
- why_it_matters:
- source_keys:
- key_excerpt_or_datapoint:
- confidence:
- limitations:

## Contradictions And Tensions

- <conflict or `none found`>

## Open Leads

- <next leads or `none`>

## Handoff

- suggested_neighbors:
- normalization_cluster:
- recommended_next_step:

## Review Questions

- <for review files or `n/a`>

## Next Research Prompts

| prompt_id | objective | why_now | suggested_source_directions | drift_bound | priority |
| --- | --- | --- | --- | --- | --- |

## Iteration Control

- recommended_next_batch_size:
- recommended_total_discovery_target:
- estimated_remaining_discovery_files:
- continue_or_shift:
- theme_drift_note:

## State File Update

- subresearch_index_row_appended:
- source_keys_appended:
- iteration_review_log_row_appended:
- prompt_backlog_rows_appended:
- retry_or_conflict_notes:
```

## Return Rules

1. `Sources Reviewed` is mandatory even when the worker found nothing useful.
2. The `novelty` field must say whether a source appears `new`, `already_seen`, `unclear`, or `rechecked_for_conflict`.
3. `Findings` may be short, but they must stay tied to `source_keys`.
4. Every material finding should include a short `key_excerpt_or_datapoint` when the source permits it.
5. Workers must preserve contradictions instead of smoothing them away.
6. Workers must list open leads rather than hiding them.
7. Workers may report `status: partial` or `status: blocked` when the source path failed.
8. Workers should report `state_append_status: appended` only after their own state-file rows were written.
9. For `file_class: review`, `Next Research Prompts` must contain `3-5` prompts unless `continue_or_shift` explicitly says `shift_to_normalization` or `stop_for_exhaustion`.
10. For `file_class: review`, the worker must stay near the core topic and may only use bounded drift that is justified in `theme_drift_note`.

## Orchestrator Rejection Rule

Reject the file if any of these is true:

- `Sources Reviewed` is missing;
- source identity is missing;
- the file is only a prose summary with no source table;
- findings do not reference source keys;
- material findings omit `key_excerpt_or_datapoint` without reason;
- contradictions were obviously flattened;
- the file lacks a `State File Update` section;
- a review file lacks `Review Questions`, `Next Research Prompts`, or `Iteration Control`;
- a review file returns fewer than `3` prompts without an explicit stage-shift or exhaustion reason;
- the worker ignored the assigned file set or topic slice;
- the file is trying to act as the final report instead of one bounded contribution.
