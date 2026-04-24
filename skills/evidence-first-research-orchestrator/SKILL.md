---
name: evidence-first-research-orchestrator
description: Use when a task requires wide evidence-first research across web sources, documents, repositories, and other auditable artifacts with delegation-first breadth collection, late normalization, and one deep final synthesis document
---

# Evidence-First Research Orchestrator

## Purpose

Use this skill for research that must gather a very large and diverse source base before deep synthesis.

This is a breadth-first research system:

- early waves maximize source discovery and angle diversity;
- the orchestrator delegates first-pass collection to subagents;
- the state file prevents duplicate source work;
- late waves normalize every subresearch file without omission;
- the final wave produces one large normalized research document.

This skill is intentionally long-running. Multi-hour runs are acceptable if that is what it takes to build a strong corpus.

Do not use this skill for quick fact lookup, one-off browsing, or small questions that do not justify a large wave-based corpus build.

## Runtime Surfaces

This skill uses only three run-time artifact surfaces:

- `evidence-research-state.md`
- `evidence-subresearch/`
- `evidence-research-final-report.md`

Do not create separate claim registries, wave logs, gap logs, audit CSVs, or sidecar verification files by default.
The state file carries run state plus the source and file index.
The subresearch folder carries one markdown file per subagent run.
The final report is the only canonical synthesis document.

## Mandatory Operating Stance

1. The main orchestrator delegates before doing first-pass collection itself.
2. Discovery is adaptive and iteration-based, not fixed in advance:
   - the orchestrator decides how many research subagents to launch in the current batch;
   - after every research batch, launch one independent `iteration-reviewer`;
   - the reviewer reads the latest research files, asks hard questions, and returns `3-5` prompts for the next batch unless it explicitly recommends shifting toward normalization;
   - the orchestrator must re-decide the next batch width and direction after every reviewer pass.
3. The reviewer sets the approximate discovery scale for the topic inside a `10-300` range.
4. Complex or ambiguous topics should bias toward the high end of that range instead of stopping early.
5. Slight bounded drift is allowed when it sharpens the original question, but the reviewer must keep the next prompts anchored to the core theme.
6. Early waves optimize for unique sources and distinct angles, not polished reasoning.
7. Every subagent writes exactly one file inside `evidence-subresearch/`.
8. After writing its file, the subagent must update `evidence-research-state.md` directly with:
   - one index entry for its file;
   - source-ledger rows for the sources it reviewed.
9. Subagents may append only their own new rows in the state file; the orchestrator owns reconciliation, counters, and status correction.
10. Once the reviewer-orchestrator loop decides the discovery corpus is large enough, the orchestrator switches to iterative normalization waves and must process all indexed files without exception.
11. The final report is written only after every indexed discovery file has both a normalization outcome and a final-report outcome in the state file.
12. If the user question is workable but underspecified, record assumptions in the state file and continue. Do not pause for clarification unless proceeding would be unsafe.

## Read Order

Read these files before running the workflow:

- `references/control-plane.md`
- `references/role-taxonomy.md`
- `references/subagent-input-contract.md`
- `references/subagent-return-contract.md`
- `references/final-output-contract.md`
- `templates/artifact-templates.md`

Then use these operational aids when available:

- `examples/sample-run/` for a concrete discovery -> review -> normalization example
- `scripts/update_state.py` for append-only state updates
- `scripts/validate_research_run.py` before reviewer pass, before normalization handoff, and before closure

## Execution Loop

1. Bootstrap:
   - create `evidence-research-state.md`;
   - create `evidence-subresearch/`;
   - set the research objective, working assumptions, provisional discovery range, initial batch hypothesis, and source-duplication rules.
2. Breadth collection:
   - keep spawning disjoint research packets;
   - prioritize unexplored source families, jurisdictions, implementation surfaces, time slices, or counter-positions;
   - accept source-rich files, reject summary-only files;
   - require each subagent to append its own file index row and source rows into the state file.
3. Iteration review:
   - launch one independent reviewer on the latest batch of research files;
   - require the reviewer to surface open questions, weak points, and contradictions from the latest files;
   - require the reviewer to write `3-5` prompts for the next research batch unless it explicitly recommends moving toward normalization or stopping for exhaustion;
   - require the reviewer to recommend the next batch width and an updated approximate total discovery count inside `10-300`.
4. Coverage expansion:
   - use the reviewer prompts to decide the next research batch rather than repeating the previous pattern blindly;
   - continue collection while waves still add novel sources, novel contradictions, or novel analytical angles;
   - prefer additional discovery waves until the reviewer-driven corpus target is reached or a documented exhaustion boundary is accepted;
   - use the state file to steer the next packets away from already covered material.
5. Normalization:
   - group related indexed files into batches by theme;
   - run repeated normalization passes across those batches;
   - iteratively promote those batches into the final report instead of attempting one giant one-shot merge;
   - mark every indexed file in the state file as normalized, duplicated, contradictory, or empty-with-reason;
   - do not leave any file unreviewed.
6. Final synthesis:
   - write one deep report that preserves the meanings and tensions from the underlying files;
   - complete one final whole-document normalization pass over the complete report after all batches have already been integrated.

## Hard Invariants

1. No first-pass collection by the main orchestrator before delegated packets are launched.
2. No duplicate-source blindness: every accepted source must be recorded in the state file.
3. No summary-only subagent files.
4. No subagent completion without a direct state-file append for its own file and sources.
5. No discovery batch without a subsequent independent reviewer pass.
6. No next discovery batch without reviewer prompts or an explicit reviewer recommendation to shift stages.
7. No fixed batch width reused blindly across iterations.
8. No synthesis before breadth collection is materially complete.
9. No final synthesis while any indexed discovery file still lacks a normalization outcome.
10. No contradiction smoothing into fake consensus.
11. No loss of semantic detail just because the final document is cleaner.
12. No asking the user for extra clarification when reasonable written assumptions can keep the run moving.
13. No leaving critical findings only inside subresearch files; the final report must absorb them.
14. No closing the run without a full-file coverage pass recorded in the state file.

## Deliverables

This skill is complete only when it leaves:

- `evidence-research-state.md` with live run state, source ledger, subresearch index, and normalization coverage;
- `evidence-subresearch/` with one file per subagent run and a reviewer-shaped discovery corpus that stays inside `10-300` and should bias upward on complex topics;
- `evidence-research-final-report.md` as the deep normalized research document;
- explicit preservation of contradictions, unresolved questions, and boundary notes inside the final report instead of leaving them only in subresearch files.
