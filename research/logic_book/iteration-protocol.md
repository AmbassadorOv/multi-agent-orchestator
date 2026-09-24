# Logic Book Iteration Protocol

## Objective
Incrementally improve a provenance-first knowledge base for the *Book of Logic* (ספר ההגיון), with Wikipedia/MediaWiki used as contextual and bibliographic evidence, not as an authority that silently replaces the primary text.

## Every iteration
1. Select a bounded unresolved frontier: one chapter, term cluster, relation, or suspected drift.
2. Extract primary-text evidence available to the project.
3. Query MediaWiki MCP for structure: page metadata, revisions, history, backlinks, categories and diffs.
4. Query Wikipedia MCP for content, sections and links.
5. If wikipedia-crosscheck is configured, obtain an independent extraction.
6. Normalize each extraction into provenance records. Never merge sources into a single undifferentiated answer.
7. Compare claims, definitions, chapter placement, names and relations.
8. Run drift tests: terminology drift; chapter/node drift; definition drift; relation-direction drift; count/order drift; source/version drift.
9. When drift is detected, trace backward to the earliest decision node supported by evidence.
10. Re-open the source material at that node and test the parent assumptions before changing downstream records.
11. Create a candidate correction only when evidence supports it.
12. Preserve the old state and record why it changed.
13. Expand the ontology only from newly supported evidence; never invent numeric logical weights.
14. Stop when the iteration reaches its bounded budget. Leave a machine-readable checkpoint for the next iteration.

## Drift localization rule
A drift is not merely model disagreement. It is a reproducible mismatch between independently sourced evidence, an established project invariant, or a previously provenance-backed record.

When drift occurs, test in this order:
source/version -> term identity -> chapter placement -> local relation -> cross-chapter relation -> derived classification.

Do not jump directly to a global reclassification.

## Output
Each iteration must produce: extraction records; provenance records; drift report; candidate corrections; unresolved questions; next frontier; iteration timestamp/id.

## Safety invariants
- No secret is committed.
- No source is silently overwritten by another source.
- No exact logical weight is invented.
- No global ordering is inferred merely from chapter order.
- Revisions are append-only at the evidence/decision level.
