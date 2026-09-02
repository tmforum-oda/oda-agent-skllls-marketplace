---
name: feedback-propose-matrix-correction
description: Turns ${CLAUDE_PLUGIN_ROOT}/knowledge/index/matrix-discrepancies.md's logged use-case/matrix disagreements into specific, submittable correction proposals for the next IG1228 revision -- e.g. which TMFCxxx rows should be added or removed for a given TMFSxxx use case. Use this to act on a logged discrepancy rather than just read about it.
---

# Propose Matrix Correction — Skill Instructions

## What this skill produces

A specific, submittable correction for one (or every) disagreement in
`${CLAUDE_PLUGIN_ROOT}/knowledge/index/matrix-discrepancies.md` — "IG1228 chapter 2's TMFS009
row should add TMFC001/002/005/008" — not a restatement of the
discrepancy table.

## Step 1 — Read the disagreement, not just the id

`${CLAUDE_PLUGIN_ROOT}/knowledge/index/matrix-discrepancies.md`'s table has two columns per use
case: **own-only** (components the document's own References section
names but the matrix doesn't credit) and **matrix-only** (components the
matrix credits but the document's own References section doesn't name).
These need opposite corrections:

- **Own-only** → propose *adding* those `TMFCxxx` ids to the use case's
  row in IG1228 chapter 2's matrix table.
- **Matrix-only** → this is more ambiguous, and the correction proposal
  should say so: it could mean the matrix should be trusted and the
  document's own References section is what's incomplete (the more
  common pattern per the file's own analysis), or it could mean the
  matrix genuinely over-credits the use case and should drop the row.
  Don't default to "the document is right, fix the matrix" without
  checking which is actually more plausible for this specific case.

## Step 2 — Ground the proposal in the actual source text

For an own-only correction, quote the specific line from the use case's
own References section (`${CLAUDE_PLUGIN_ROOT}/knowledge/use-cases/{ID}/{ID}.md`) that names
the component the matrix is missing — a correction proposal needs a
citable source, not just "the discrepancy file says so." For a
matrix-only correction, check whether the component appears anywhere
else in the document's body (per the same body-text-vs-frontmatter gap
`generate-test-cases-from-usecase` documents) before concluding the
matrix is simply wrong — a component named in body prose but missed by
`docx2md.py`'s References-section-only extraction isn't a matrix error at
all, it's a frontmatter extraction gap, and the correction should say
that distinction explicitly rather than blaming the matrix.

`matrix-discrepancies.md` itself is hand-maintained and isn't rebuilt by
any refresh script the way `components.json`/`apis.json` are — it
reflects the corpus as of whenever it was last regenerated, not
necessarily its current state. Reading the live use case document for
this step also catches document-side drift: if its own References
section no longer contains the id the table logged as own-only, that id
has since been removed from the document itself, and the table entry is
stale — say so explicitly rather than drafting a correction to add an id
the document no longer even claims. This check only covers the
document's side, not the matrix's — `usecase-component-matrix.json` is
extracted from IG1228 separately and isn't re-derived by this skill, so
a matrix-side change since the table was built wouldn't be caught here.

## Step 3 — Flag both-direction cases as needing human judgment, not an automatic pick

A use case with entries in *both* the own-only and matrix-only columns
(disagreement in both directions) doesn't have an obvious "correct"
answer — don't pick one side and propose only that half. State both
findings and say explicitly that a human reviewer needs to decide, rather
than resolving the ambiguity unilaterally.

## Output format

One correction entry per use case, each with: the use case id, the
specific `TMFCxxx` id(s) involved, which direction (add-to-matrix /
remove-from-matrix / needs-human-review), and the citable source text
backing the proposal. Group by direction so a reviewer can process all
the "add to matrix" proposals together, separately from the "needs
review" ones.

## What this skill does NOT do

- Does not submit anything to TM Forum or edit `${CLAUDE_PLUGIN_ROOT}/knowledge/index/usecase-component-matrix.json` directly — this drafts a proposal for a human working-group member to take forward, it doesn't act as if the correction were already accepted.
- Does not resolve a both-direction disagreement by picking the side that seems more likely — Step 3's flag is required output for those cases, not an optional caveat.
- Does not propose a correction without a citable source line — "the discrepancy file logs it" is not itself a citable source for a correction proposal; the source is the use case document's own text.
