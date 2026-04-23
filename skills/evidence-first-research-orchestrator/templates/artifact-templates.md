# Artifact Templates

Use these templates when creating or refreshing run artifacts.
Keep the structure stable so the orchestrator can track coverage without extra sidecars.

## `evidence-research-state.md`

```md
run_id:
research_objective:
current_stage:
stage_status:
current_wave:
planned_waves:
subagents_per_wave:
recommended_next_batch_size:
recommended_total_discovery_target:
estimated_remaining_discovery_files:
latest_review_file_id:
target_discovery_file_range: 10-300
minimum_discovery_file_floor: 10
subresearch_dir: evidence-subresearch/
final_report_path: evidence-research-final-report.md
subresearch_files_total:
discovery_files_total:
unique_sources_total:
normalization_pass_count:
normalized_file_count:
pending_normalization_count:
promoted_file_count:
full_corpus_coverage_status:
next_action:
updated_at:

## Working Assumptions

-

## Collection Strategy

- multi_hour_mode: allowed
- breadth_bias:
- collection_stop_rule:
- expansion_rule:
- reviewer_loop: after_every_research_batch
- theme_drift_policy: slight_bounded_only

## Source Ledger

Append-only by subagents for new source rows. Reconciliation is orchestrator-owned.

| source_key | title | url_or_path | source_family | first_seen_in_file_id | first_seen_wave | reuse_status | last_checked_at | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Subresearch Index

Append-only by subagents for new file rows. Status corrections are orchestrator-owned.

| file_id | file_class | path | stage | wave | agent_id | role | topic_slice | source_keys | reviewed_sources_count | novelty | state_append_status | normalization_status | final_report_status | promoted_sections | short_summary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Iteration Review Log

| review_file_id | reviewed_file_ids | reviewer_agent_id | review_scope | recommended_next_batch_size | recommended_total_discovery_target | estimated_remaining_discovery_files | continue_or_shift | theme_drift_note | prompt_ids | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Prompt Backlog

| prompt_id | parent_review_file_id | objective | why_now | suggested_source_directions | drift_bound | priority | status |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Normalization Queue

| batch_id | theme | input_file_ids | output_file_id | status | promoted_sections | notes |
| --- | --- | --- | --- | --- | --- | --- |

## Final Synthesis Checklist

| item | status | notes |
| --- | --- | --- |
| latest reviewer accepted current discovery target or explicit exhaustion | pending | |
| all indexed files have normalization status | pending | |
| all indexed files have final report status | pending | |
| contradictions retained in final report | pending | |
| major assumptions disclosed | pending | |
```

## `evidence-subresearch/<file-name>.md`

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

-

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

-

## Open Leads

-

## Handoff

- suggested_neighbors:
- normalization_cluster:
- recommended_next_step:

## Review Questions

- n/a

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

## `evidence-research-final-report.md`

```md
# <research title>

## 1. Research Question And Working Assumptions

## 2. Iteration Strategy, Corpus Scale, And Source Coverage

## 3. Terminology And Boundary Rules

## 4. Normalized Findings By Theme

## 5. Contradictions, Tensions, And Hard Disagreements

## 6. Cross-Source Synthesis

## 7. What Remains Open

## 8. Conclusion

## 9. Appendices

### Appendix A. Source-Family Coverage

### Appendix B. Subresearch File Coverage, Review Loop, And Promotion Logic

### Appendix C. Major Contradiction Clusters

### Appendix D. Assumptions That Shaped The Search
```
