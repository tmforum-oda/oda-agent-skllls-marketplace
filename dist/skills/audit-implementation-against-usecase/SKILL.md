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

Read `${CLAUDE_PLUGIN_ROOT}/knowledge/use-cases/{ID}/{ID}.md` — the `# Description` and
`# Sequence diagrams` sections for the expected flow (including the
diagram images themselves, not just surrounding prose — the real step
order and actors usually live in the images), and frontmatter
`links.components`/`links.apis` for the real ids it depends on. This is
the checklist the implementation gets audited against — build it before
looking at the implementation, not while reading it, so the audit isn't
unconsciously shaped by what the implementation already does.

## Step 3 — Compare against the implementation

For each API the use case links, check whether the implementation
actually calls it — and specifically, whether it calls operations that
exist in the cached schema (`${CLAUDE_PLUGIN_ROOT}/knowledge/apis/{TMFxxx}/{TMFxxx}_v{version}.json`).
A call to an operation or path that isn't in the cached schema is itself
a finding — either the implementation is calling something invalid, or
it's using a newer/older API version than what's cached here (check
`${CLAUDE_PLUGIN_ROOT}/knowledge/index/apis.json` for other cached versions of the same id
before concluding it's wrong).

For each component the use case links, check whether the implementation
has an equivalent piece of functionality — this is necessarily a looser
match than the API check (implementations don't literally instantiate
ODA components), so report it as "functionally maps to X" or "no
equivalent found for X," not as a strict pass/fail.

## Step 4 — Report drift, don't silently normalize it

Every difference between the use case's described flow and the
implementation is a finding, whichever direction it points:

- Implementation calls an API/operation the use case doesn't link — flag
  as either an undocumented extension or a sign the use case's own
  frontmatter is incomplete (cross-check `${CLAUDE_PLUGIN_ROOT}/knowledge/index/matrix-discrepancies.md`
  for this id before assuming the implementation is wrong).
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
