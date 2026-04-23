# Control Plane Contract

This file defines the minimal deterministic surface of the skill.

## Runtime Model

The workflow has three persistent surfaces:

- `evidence-research-state.md`
- `evidence-subresearch/`
- `evidence-research-final-report.md`

Everything else should stay inside the chat transcript or inside a subagent file that already lives in `evidence-subresearch/`.

## Naming And ID Rules

Keep IDs and file names deterministic enough that subagents can coordinate without asking.

- `file_id`:
  - discovery files: `d-w<wave>-a<agent>-<slug>`
  - review files: `r-w<wave>-a<agent>`
  - normalization files: `n-b<batch>-<slug>`
  - synthesis or critique files: `s-w<wave>-<slug>`
- `prompt_id`: `p-r<review-wave>-<nn>`
- `source_key`: short stable slug from source family plus site or document identity
- `batch_id`: `b-<nn>-<slug>`

Prefer sortable names for on-disk files:

- `discovery-w<wave>-a<agent>-<slug>.md`
- `review-w<wave>-a<agent>.md`
- `normalization-b<batch>-<slug>.md`
- `synthesis-w<wave>-<slug>.md`

## Stage Model

Use these stages:

- `bootstrap`
- `breadth_collection`
- `iteration_review`
- `coverage_expansion`
- `normalization`
- `final_synthesis`
- `done`
- `blocked`

Treat stage progression as corpus progression:

- `breadth_collection` builds the large discovery corpus;
- `iteration_review` critiques the latest batch and generates the next bounded prompts;
- `coverage_expansion` pushes that corpus toward the target range;
- `normalization` iteratively reduces the indexed corpus into coherent thematic synthesis;
- `final_synthesis` performs the last full harmonization pass over an already-normalized corpus.

Use these stage statuses:

- `active`
- `awaiting_returns`
- `review`
- `repeat_required`
- `passed`
- `done`
- `blocked`

## Delegation Doctrine

The orchestrator owns:

- objective control;
- packet assembly;
- source-deduplication discipline;
- state-file integrity;
- batch selection for normalization;
- final report integrity.

Subagents own:

- first-pass source discovery;
- angle expansion;
- contradiction hunting;
- implementation/example scouting;
- latest-batch review and next-prompt generation;
- batch normalization;
- synthesis challenge.

The orchestrator must not perform first-pass collection before delegated packets are launched for the current wave unless subagent tooling is unavailable.

## Wave Rules

1. Use iteration-based collection, not one long serial run.
2. In each research iteration, the orchestrator chooses the number of research subagents instead of reusing a fixed width blindly.
3. A research batch often lands in the `1-5` subagent range, but that width must be re-evaluated after every reviewer pass.
4. After every research batch, run exactly one independent `iteration-reviewer`.
5. The reviewer must:
   - read the latest research files;
   - identify weak spots, contradictions, and underexplored directions;
   - return `3-5` prompts for the next research batch unless it explicitly recommends stage shift or exhaustion;
   - recommend the next batch width;
   - recommend an updated approximate total discovery target.
6. The approximate total discovery target must stay inside `10-300`.
7. Complex topics should bias upward rather than stopping early.
8. Bias the first waves toward source diversity:
   - new source families;
   - new institutions;
   - new implementations;
   - new contradictory positions;
   - new time slices where relevant.
9. Keep collecting while reviewer-guided iterations still add meaningful novelty.
10. Do not move to normalization early just because the topic feels understandable.
11. Use the state-file source ledger to avoid obvious duplicate browsing.
12. Time is elastic. Multi-hour runs are acceptable if the corpus is still improving.

## Latest Batch Rule

`latest research batch` means the discovery-oriented files added since the most recent accepted review file.

If there is no prior accepted review file, the latest batch is the full current discovery set.
The orchestrator should pass those exact `reviewed_file_ids` into the reviewer packet instead of making the reviewer guess.

## Required State File

Use `evidence-research-state.md` with these top-level fields:

- `run_id`
- `research_objective`
- `current_stage`
- `stage_status`
- `current_wave`
- `planned_waves`
- `subagents_per_wave`
- `recommended_next_batch_size`
- `recommended_total_discovery_target`
- `estimated_remaining_discovery_files`
- `latest_review_file_id`
- `subresearch_dir`
- `final_report_path`
- `target_discovery_file_range`
- `minimum_discovery_file_floor`
- `subresearch_files_total`
- `discovery_files_total`
- `unique_sources_total`
- `normalization_pass_count`
- `normalized_file_count`
- `pending_normalization_count`
- `promoted_file_count`
- `full_corpus_coverage_status`
- `next_action`
- `updated_at`

And these required sections:

- `Working Assumptions`
- `Collection Strategy`
- `Source Ledger`
- `Subresearch Index`
- `Iteration Review Log`
- `Prompt Backlog`
- `Normalization Queue`
- `Final Synthesis Checklist`

The state file is both the control artifact and the anti-duplication index.
Do not split those responsibilities into separate registries.

## Direct State Update Protocol

Subagents update the shared state file directly, but only in a narrow append-only way.

1. A subagent writes its own subresearch file first.
2. The subagent rereads the latest state file.
3. The subagent appends:
   - one new `Subresearch Index` row for its file;
   - the needed `Source Ledger` rows for the sources it reviewed.
4. The subagent must not rewrite:
   - counters;
   - totals;
   - normalization statuses for other files;
   - final-report statuses for other files.
5. Reviewer subagents may also append:
   - one `Iteration Review Log` row for their review file;
   - `3-5` `Prompt Backlog` rows for the next research batch.
6. The orchestrator reconciles duplicate sources, updates counters, accepts or rejects prompts, and corrects statuses after each iteration review.
7. If a subagent sees that its `file_id` already exists, it must not append a second row for that file.
8. If a stale-state conflict happens, the subagent should reread the state file and retry the append instead of editing arbitrary existing rows.

## Allowed State Values

Use stable values so different subagents do not invent competing vocabularies.

- `state_append_status`:
  - `pending`
  - `appended`
  - `conflict_retry`
  - `blocked`
- `Prompt Backlog.status`:
  - `new`
  - `claimed`
  - `completed`
  - `merged`
  - `dropped`
- `continue_or_shift`:
  - `continue_discovery`
  - `shift_to_normalization`
  - `shift_to_final_synthesis`
  - `stop_for_exhaustion`
- `priority`:
  - `high`
  - `medium`
  - `low`
- `theme_drift_note` should say either:
  - `tight_to_core`
  - `slight_bounded_drift`
  - `drift_not_allowed`

## Source Ledger Rule

The `Source Ledger` in the state file must record every accepted source that was checked in subresearch files, including duplicates and dead ends when they matter.

At minimum each source row must preserve:

- `source_key`
- `title`
- `url_or_path`
- `source_family`
- `first_seen_in_file_id`
- `first_seen_wave`
- `reuse_status`
- `last_checked_at`
- `notes`

Use `reuse_status` to mark `new`, `already_seen`, `superseded`, `duplicate`, or `needs_recheck`.

## Subresearch Index Rule

The `Subresearch Index` in the state file must record every subresearch file.

At minimum each row must preserve:

- `file_id`
- `file_class`
- `path`
- `stage`
- `wave`
- `agent_id`
- `role`
- `topic_slice`
- `source_keys`
- `reviewed_sources_count`
- `novelty`
- `state_append_status`
- `normalization_status`
- `final_report_status`
- `short_summary`

This index is the authoritative list of files that must be normalized and then covered by the final report.

Each discovery file row should be linkable and traceable without opening chat history.
The index is expected to grow large. A reviewer-shaped discovery corpus may land anywhere in `10-300`, but complex topics should bias upward instead of stopping early.

## Iteration Review Log Rule

The `Iteration Review Log` records the steering pass that happens after every research batch.

At minimum each row must preserve:

- `review_file_id`
- `reviewed_file_ids`
- `reviewer_agent_id`
- `review_scope`
- `recommended_next_batch_size`
- `recommended_total_discovery_target`
- `estimated_remaining_discovery_files`
- `continue_or_shift`
- `theme_drift_note`
- `prompt_ids`
- `notes`

The reviewer is allowed slight bounded drift only when it sharpens the original objective instead of replacing it.
The reviewer should explicitly mark whether each prompt stays `tight_to_core` or uses `slight_bounded_drift`.

## Prompt Backlog Rule

The `Prompt Backlog` stores the reviewer-generated prompts for the next research batches.

At minimum each row must preserve:

- `prompt_id`
- `parent_review_file_id`
- `objective`
- `why_now`
- `suggested_source_directions`
- `drift_bound`
- `priority`
- `status`

Reviewer-generated prompt sets should normally contain `3-5` prompts.
Fewer than `3` prompts is valid only when the reviewer explicitly recommends stage shift or exhaustion.

Prompts should be consumed in priority order, but the orchestrator may merge near-duplicate prompts into one stronger packet before the next batch launches.

## Research Batch Closure Rule

Do not send a batch to reviewer pass until the orchestrator has checked that:

- each file in the batch exists on disk;
- each file appended its own state rows or explicitly reported a conflict;
- duplicate-heavy or source-poor files were either rejected or marked with a reason;
- the batch is coherent enough for a reviewer to critique it.

## Normalization Rule

Normalization is exhaustive, iterative, and corpus-wide.

1. Build batches from the indexed discovery files by topic, claim family, geography, chronology, implementation surface, or contradiction cluster.
2. Run normalization over those batches in multiple passes rather than one giant merge.
3. Reviewer-style critique may continue during normalization, but discovery-style prompt drift should stay constrained by the already-built corpus.
4. After each batch pass, update the affected file rows and the final-report promotion notes.
5. Update every indexed discovery-file row with a `normalization_status`.
6. Allowed statuses are:
   - `pending`
   - `normalized`
   - `duplicate`
   - `contradiction_retained`
   - `empty_with_reason`
7. Do not start the last full synthesis pass while any indexed discovery file is still `pending`.
8. The preferred normalization rhythm is batch-by-batch promotion into the final report, followed by a final whole-document harmonization pass.

## Final Synthesis Rule

The final report becomes the canonical truth surface only after:

- collection breadth is sufficient for the topic;
- every indexed file has a normalization status;
- the discovery corpus either reached the target range or has an explicit exhaustion note;
- the latest accepted reviewer pass no longer demands further discovery work;
- the state file shows which files were promoted into the report.

Final report coverage does not require every file to get equal space, but every file must get an explicit outcome recorded in the state file.

## Orchestrator Responsibilities

The main orchestrator must:

- keep the run moving without unnecessary user clarification;
- package disjoint packets;
- reject source-free or duplicate-heavy subagent returns;
- update the state file after every accepted file;
- enforce the direct state-update protocol for every subagent file;
- spawn and validate one independent reviewer after every research batch;
- use reviewer prompts rather than inertia to choose the next batch;
- keep expanding collection while novelty remains high;
- ensure late-stage normalization covers all indexed files;
- produce one deep final report rather than a pile of partial syntheses.

If any of those conditions fail, the run is incomplete.
