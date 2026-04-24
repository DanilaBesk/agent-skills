run_id: sample-run-001
research_objective: Compare local-first AI coding tool memory patterns across documentation and implementation examples.
current_stage: normalization
stage_status: active
current_wave: w02
planned_waves: adaptive
subagents_per_wave: adaptive
recommended_next_batch_size: 2
recommended_total_discovery_target: 12
estimated_remaining_discovery_files: 3
latest_review_file_id: r-w01-a99
target_discovery_file_range: 10-300
minimum_discovery_file_floor: 10
subresearch_dir: evidence-subresearch/
final_report_path: evidence-research-final-report.md
subresearch_files_total: 3
discovery_files_total: 1
unique_sources_total: 2
normalization_pass_count: 1
normalized_file_count: 1
pending_normalization_count: 1
promoted_file_count: 1
full_corpus_coverage_status: in_progress
next_action: run the next discovery batch from prompt backlog items p-r01-01 and p-r01-02
updated_at: 2026-04-24T14:00:00+03:00

## Working Assumptions

- local-first repos and docs are enough to demonstrate the workflow shape in this sample

## Collection Strategy

- multi_hour_mode: allowed
- breadth_bias: official docs first, then implementation examples
- collection_stop_rule: reviewer confirms enough thematic coverage or explicit exhaustion
- expansion_rule: use reviewer prompts before increasing batch width
- reviewer_loop: after_every_research_batch
- theme_drift_policy: slight_bounded_only

## Source Ledger

Append-only by subagents for new source rows. Reconciliation is orchestrator-owned.

| source_key | title | url_or_path | source_family | first_seen_in_file_id | first_seen_wave | reuse_status | last_checked_at | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| src-example-1 | Local Memory Design Note | https://example.com/local-memory | web-doc | d-w01-a01-memory-design | w01 | new | 2026-04-24T10:10:00+03:00 | primary concept note |
| src-example-2 | OSS Implementation Note | https://example.com/oss-impl | repo-doc | d-w01-a01-memory-design | w01 | new | 2026-04-24T10:14:00+03:00 | concrete implementation surface |
<!-- append-source-ledger-rows-here -->

## Subresearch Index

Append-only by subagents for new file rows. Status corrections are orchestrator-owned.

| file_id | file_class | path | stage | wave | agent_id | role | topic_slice | source_keys | reviewed_sources_count | novelty | state_append_status | normalization_status | final_report_status | promoted_sections | short_summary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| d-w01-a01-memory-design | discovery | evidence-subresearch/discovery-w01-a01-memory-design.md | breadth_collection | w01 | a01 | breadth-scout | local memory design patterns | src-example-1,src-example-2 | 2 | high | appended | normalized | promoted | 4 | mapped the core design pattern |
| r-w01-a99 | review | evidence-subresearch/review-w01-a99.md | iteration_review | w01 | a99 | iteration-reviewer | review first discovery batch |  | 0 | medium | appended | pending | duplicate_noted | 2 | generated next discovery prompts |
| n-b01-memory-cluster | normalization | evidence-subresearch/normalization-b01-memory-cluster.md | normalization | w02 | a21 | batch-normalizer | normalize the first memory cluster |  | 0 | medium | appended | normalized | promoted | 4 | normalized the first thematic batch |
<!-- append-subresearch-index-rows-here -->

## Iteration Review Log

| review_file_id | reviewed_file_ids | reviewer_agent_id | review_scope | recommended_next_batch_size | recommended_total_discovery_target | estimated_remaining_discovery_files | continue_or_shift | theme_drift_note | prompt_ids | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r-w01-a99 | d-w01-a01-memory-design | a99 | initial memory-pattern batch | 2 | 12 | 3 | continue_discovery | tight_to_core | p-r01-01,p-r01-02,p-r01-03 | more evidence needed around conflict handling and write paths |
<!-- append-iteration-review-log-rows-here -->

## Prompt Backlog

| prompt_id | parent_review_file_id | objective | why_now | suggested_source_directions | drift_bound | priority | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| p-r01-01 | r-w01-a99 | find conflict-resolution behavior in local memory tools | reviewer found weak evidence on collisions | official docs, issue threads | tight_to_core | high | new |
| p-r01-02 | r-w01-a99 | inspect write-path safeguards in open-source implementations | implementation depth is still thin | repo docs, source comments | tight_to_core | high | new |
| p-r01-03 | r-w01-a99 | collect one adjacent but bounded example from another local-first tool | improve comparison quality | product docs, architecture notes | slight_bounded_drift | medium | new |
<!-- append-prompt-backlog-rows-here -->

## Normalization Queue

| batch_id | theme | input_file_ids | output_file_id | status | promoted_sections | notes |
| --- | --- | --- | --- | --- | --- | --- |
| b-01-memory | local memory design cluster | d-w01-a01-memory-design | n-b01-memory-cluster | completed | 4 | first normalized batch |
<!-- append-normalization-queue-rows-here -->

## Final Synthesis Checklist

| item | status | notes |
| --- | --- | --- |
| latest reviewer accepted current discovery target or explicit exhaustion | pending | discovery still in progress |
| all indexed files have normalization status | pending | review file still pending |
| all indexed files have final report status | pending | review file not yet promoted |
| contradictions retained in final report | pending | waiting for more evidence |
| major assumptions disclosed | pass | listed in state and report |
