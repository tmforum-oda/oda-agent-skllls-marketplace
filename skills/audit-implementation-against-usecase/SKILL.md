---
name: audit-implementation-against-usecase
description: Given a TMFSxxx use-case id and an existing implementation (codebase, API contract, or integration config), checks whether the implementation actually follows the use case's described flow and calls the right real APIs, flagging drift from spec. Use this to audit an existing system against ODA, not to design a new one.
---

# Audit Implementation Against Use Case — Skill Instructions

## What this skill answers

"Does our existing system actually do what TMFSxxx says it should?" The
reverse of `validate-design-against-oda`, which checks a *proposed*
design before it's built — this skill checks something that already
exists, against a use case it claims to implement.

## Step 1 — Check maturity first

Run `check-usecase-maturity` against the id. An audit against an
Alpha/Beta use case should report drift with that context — the spec
itself may still be moving, so not every difference is necessarily the
implementation's fault.

## Step 2 — Establish what the use case actually requires

Read `knowledge/use-cases/{ID}/{ID}.md` for the expected flow — the
`# Description` section, and whatever the document calls its
sequence-diagram content. Heading text and nesting for this varies across
the corpus (sometimes a top-level `# Sequence diagrams`, sometimes nested
under `# Diagrams` → `## Sequence diagrams`, sometimes singular, sometimes
different casing) — look for it by what it actually contains, not an
exact heading match, and check the diagram images themselves, not just
surrounding prose — the real step order and actors usually live in the
images. One use case in the corpus, `TMFS019B`, genuinely has no
sequence-diagram content at all (it's structured around information
modeling, not a process flow) — if a search for it comes up empty, say so
plainly and base the audit on the `# Description` section and frontmatter
links instead, rather than inventing flow content that isn't there.

**Build the component checklist as the union of two sources, not
frontmatter alone** — this is the same reconciliation
`generate-test-cases-from-usecase` already does, and skipping it produces
real, measured gaps: read the use case's own frontmatter
`links.components`, and also look up the id in
`knowledge/index/usecase-component-matrix.json`'s `use_cases` object
(IG1228 chapter 2's own forward index for this id). Per
`knowledge/index/matrix-discrepancies.md`'s corpus-wide check, these two
sources disagree for 14 of 24 use cases — sometimes barely (one component
either way), sometimes almost entirely: `TMFS020`'s own frontmatter names
`TMFC033`/`TMFC039`/`TMFC050`/`TMFC036`, while the matrix credits it with
`TMFC001`/`TMFC020`/`TMFC023`/`TMFC028`/`TMFC035`/`TMFC039` — only one id
in common. Auditing TMFS020 against frontmatter alone would check the
wrong four components almost entirely. Take the union, note which
component came from which source (matrix-discrepancies.md's own
`matrix-only`/`own-only` framing works fine here), and carry that
provenance into Step 4's findings. `links.apis` has no matrix-side
equivalent to union against — IG1228 chapter 2 is a use-case↔**component**
table only — so the API half of the checklist stays frontmatter-only,
same asymmetry `assess-change-impact`/`spec/spec.md` §5.4 already document
for the reverse direction.

This is the checklist the implementation gets audited against — build it
before looking at the implementation, not while reading it, so the audit
isn't unconsciously shaped by what the implementation already does.

## Step 3 — Compare against the implementation

For each API the use case links, check whether the implementation
actually calls it — and specifically, whether it calls operations that
exist in the cached schema. **Don't assume the exact cached version from
the use case's own frontmatter** — a use case's `links.apis` entry only
carries `id` and `name` (the generation, like "v4", is at most embedded
loosely in the `name` string, e.g. `"Party Management v4"` — there's no
structured version field to read), so look the id up in
`knowledge/index/apis.json` to get its real cached `version`/`path`
(`knowledge/apis/{TMFxxx}/{TMFxxx}_v{version}.json`) rather than guessing
the filename. A call to an operation or path that isn't in the cached
schema is itself a finding — either the implementation is calling
something invalid, or it's using a newer/older API version than what's
cached here (check `knowledge/index/apis.json` for other cached versions
of the same id before concluding it's wrong).

For each component the use case links, check whether the implementation
has an equivalent piece of functionality — this is necessarily a looser
match than the API check (implementations don't literally instantiate
ODA components), so report it as "functionally maps to X" or "no
equivalent found for X," not as a strict pass/fail.

## Step 4 — Report drift, don't silently normalize it

Every difference between the use case's described flow and the
implementation is a finding, whichever direction it points:

- Implementation calls an API the use case doesn't link — flag as either
  an undocumented extension or a sign the use case's own document is
  incomplete. For a **component**, Step 2's matrix union already covers
  the common case (the matrix credits it even though the document
  doesn't); this bullet is really about the narrower cases Step 2 can't
  catch — an **API** (no matrix data to check at all), or a component
  named only in the use case's own body prose rather than its References
  section (frontmatter extraction only reads the References section, so
  a component mentioned only in the flowing text — like TMFS020's own
  `TMFC001`/`002`/`023` in its body — won't be in `links.components`
  *or* the matrix). Don't assume the implementation is wrong before
  checking whether the document's own body text already justifies it.
- Use case links an API/component the implementation doesn't touch —
  flag as a genuine gap, not something to explain away.
- Sequence order differs from what the diagrams show — flag it; don't
  assume the implementation's order is fine just because it's simpler.

## Output format

A findings list, not a pass/fail verdict — each finding states what the
use case expects, what the implementation actually does, and which
direction the drift points. Close with the maturity caveat from Step 1
restated, since it changes how seriously each finding should be taken.

## What this skill does NOT do

- Does not modify the implementation — this is a read-only audit to inform a human decision, same posture as `assess-change-impact`.
- Does not treat every difference as a bug — a use case that's Alpha/Beta may legitimately be behind what a shipped implementation already does; Step 1's maturity check exists specifically so this isn't lost.
- Does not fabricate a use case's expected behavior beyond what Step 2 actually establishes — an audit finding must trace back to specific frontmatter links or specific sequence-diagram content, not a general impression of what the use case is "about."
- Does not build the component checklist from frontmatter alone — Step 2's matrix union is required, not an optional cross-check, since matrix-only disagreement is the more common case corpus-wide, not the rarer one.
- Does not invent flow content for a use case with no sequence-diagram section — `TMFS019B` is a real, confirmed example; say so and audit against whatever the document does contain instead.
