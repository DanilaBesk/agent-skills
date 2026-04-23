# Role Taxonomy

Use a small role set that maximizes source diversity early and disciplined synthesis late.

| Role | Objective | Best stage | Forbidden behavior | Required output |
| --- | --- | --- | --- | --- |
| `main orchestrator` | Own run control, packeting, state updates, batch selection, and final report integrity | all stages | doing the whole first-pass collection itself, skipping state updates, skipping file coverage | updated state file and final report |
| `breadth-scout` | Find new source clusters quickly from one bounded angle | breadth collection | polishing final conclusions, revisiting already saturated source clusters without reason | one subresearch file |
| `primary-source scout` | Pull authoritative or official sources for one angle | breadth collection or coverage expansion | replacing primary sources with weaker substitutes without saying so | one subresearch file |
| `counterevidence scout` | Hunt contradictions, edge cases, and serious disagreement | coverage expansion | collapsing conflict into consensus | one subresearch file |
| `implementation scout` | Gather real product, repository, standards, or operational examples | breadth collection or coverage expansion | treating implementation examples as universal proof | one subresearch file |
| `iteration-reviewer` | Read the latest research batch, identify the important questions, and propose the next `3-5` bounded prompts plus the next batch size | iteration review | drifting too far from the core topic, vague advice without prompts, re-running the same search path | one subresearch file |
| `batch-normalizer` | Normalize a bounded set of subresearch files into one coherent thematic pass | normalization | ignoring any assigned file, inventing claims not grounded in the files | one subresearch file |
| `final-synthesizer` | Reconstruct the final report from the normalized corpus | final synthesis | new browsing, dropping tensions, writing a shallow recap | one subresearch file or direct final-report edits when explicitly assigned |
| `synthesis-critic` | Attack weak synthesis, missing files, and hidden contradictions before closure | final synthesis | style-only review, generic praise, silent omission of coverage gaps | one subresearch file |

## Shared Rule

Every delegated role writes exactly one subresearch file and then appends its own state-file rows for that file and its reviewed sources.
`iteration-reviewer` also appends one review-log row and `3-5` prompt-backlog rows unless it explicitly recommends stage shift or exhaustion.
Only the orchestrator may reconcile or rewrite other rows.

## Routing Rules

1. Early waves should favor `breadth-scout`, `primary-source scout`, `implementation scout`, and `counterevidence scout`.
2. After every research batch, run one `iteration-reviewer` on the latest file set before choosing the next batch.
3. Do not overuse the same role in parallel if the packets hit the same source family or topic slice.
4. Normalization waves should use `batch-normalizer` on disjoint file sets.
5. Keep collection alive until the reviewer-orchestrator loop reaches the intended scale or the state file records real exhaustion.
6. Final synthesis should use `final-synthesizer` only after the state file shows zero pending normalization rows.
7. Use `synthesis-critic` before marking the run done.
