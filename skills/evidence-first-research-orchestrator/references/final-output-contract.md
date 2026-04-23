# Final Output Contract

The final output has one canonical synthesis file:

- `evidence-research-final-report.md`

But that file is only valid when it is backed by:

- `evidence-research-state.md`
- the indexed files in `evidence-subresearch/`

## Canonical Rule

The final report must be a self-sufficient research document, not a recap of the run.
Readers should be able to understand the question, search method, source coverage, thematic findings, contradictions, and bottom-line synthesis without opening every subresearch file.

The final report is expected to emerge from iterative normalization of a large corpus, not from a one-shot summarization pass.

The discovery corpus should also be shaped by repeated independent reviewer loops rather than by a fixed precommitted plan.

## Required Final Report Sections

1. `Research Question And Working Assumptions`
2. `Wave Strategy, Corpus Scale, And Source Coverage`
3. `Terminology And Boundary Rules`
4. `Normalized Findings By Theme`
5. `Contradictions, Tensions, And Hard Disagreements`
6. `Cross-Source Synthesis`
7. `What Remains Open`
8. `Conclusion`
9. `Appendices`

## Coverage Rule

The final report may compress repeated or duplicate material, but it must not skip indexed files silently.

Before the run is done:

1. every row in the state-file `Subresearch Index` must have a non-pending `normalization_status`;
2. every row must also have a non-pending `final_report_status`;
3. allowed `final_report_status` values are:
   - `promoted`
   - `promoted_as_contradiction`
   - `duplicate_noted`
   - `empty_with_reason`
4. the state file must make it possible to see how every indexed file was handled.

## Iterative Normalization Rule

The final report should be built in repeated normalization passes:

1. discovery files are grouped into thematic batches;
2. each batch is normalized and promoted into the report;
3. contradictions and duplicates stay visible during promotion;
4. after all indexed discovery files are covered, one final whole-document harmonization pass aligns terminology and structure without dropping meaning.

The reviewer loop may continue to challenge the synthesis direction, but it should no longer generate broad topic drift once the run is in late normalization.

## Depth Rule

Normalizing the report does not allow dropping meaning.

The final report must preserve:

- materially different viewpoints;
- source-backed contradictions;
- important implementation-versus-theory distinctions;
- unresolved gaps that still matter;
- the semantic distinctions discovered in subresearch files.

## Appendix Rule

The report appendix should include, in compact form:

- source-family coverage;
- subresearch file coverage;
- major contradictory clusters;
- any assumptions that materially shaped the search.

Do not push the core argument into appendices.
Appendices are compression surfaces, not the main truth surface.

The exact one-to-one file coverage map may stay in the state file, but the final report should still explain how the corpus was reduced and promoted.

## Cleanup Rule

Do not delete the state file or the subresearch folder by default.
This workflow assumes retained evidence, not report-only cleanup.
