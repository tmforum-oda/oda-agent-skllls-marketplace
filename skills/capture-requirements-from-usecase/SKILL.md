---
name: capture-requirements-from-usecase
description: Given a TMFSxxx use-case id, reads its Description/Scope/Objective sections and drafts user stories and acceptance criteria, citing the exact component/API ids from frontmatter for any integration touchpoint rather than inventing them. Use this to turn an existing use case into requirements a delivery team can work from.
---

# Capture Requirements from Use Case — Skill Instructions

## What this skill produces

User stories and acceptance criteria for a TMFSxxx use case, grounded in
its own Objective/Scope/Description text and its real component/API
links — not a generic requirements template filled in from the use
case's title alone.

## Step 0 — Check maturity first

Run `check-usecase-maturity` against the id and include its verdict at
the top of the output. Requirements drafted from an Alpha/Beta use case
should say so explicitly — the underlying flow may still change, and a
delivery team estimating against these stories needs that context.

## Step 1 — Check whether the use case already states its own user stories

Some use cases already contain hand-written "As a X, I want Y" statements
directly under `## Objective of the use case` — a plain narrative form
(e.g. "As a CSP, I want\n- to manage Customer business Intent") or a
table with `AS A`/`I NEED TO`/`SO THAT I` rows. If present, treat this as
the authoritative starting point and refine/expand it rather than
drafting a competing version from scratch — it's the document's own
authors' framing, not something to override. Not every use case has
this; when absent, draft fresh from Step 2.

## Step 2 — Draft from Objective, Scope, and Description

```
knowledge/use-cases/{ID}/{ID}.md
```

Read `# Introduction` → `## Objective of the use case`, `## Scope and
assumptions`, and `# Description`. Each distinct actor/goal named in the
Objective becomes a candidate user story ("As a `<actor>`, I want
`<goal>`, so that `<benefit>`") — actors are usually named explicitly
(Customer, CSP, Party, Organization); don't invent a persona the
document doesn't name. The Scope section's stated boundaries
("Out of Scope: ...") become explicit exclusions on the story set, not
something to silently drop.

## Step 3 — Ground acceptance criteria in real component/API ids

For a story that depends on a specific system capability, cite the real
id from the use case's own frontmatter `links.components`/`links.apis` —
"the system must verify identity via TMFC020 Digital Identity Management"
not "the system must verify identity." If the capability the story needs
isn't in frontmatter at all, check whether it's named in the document's
own body text instead (frontmatter is scoped to the References section
and isn't always exhaustive of everything a use case's body names) before
concluding there's no real id to cite. If truly nothing real backs a
capability the story needs, say so — an acceptance criterion citing an
invented id is worse than one that honestly states the gap.

## Output format

A short maturity caveat (Step 0), followed by user stories grouped by
actor, each with 2-4 acceptance criteria citing real ids where the
criterion involves a specific component/API. Close with the Scope
section's stated exclusions as explicit out-of-scope notes, not silently
omitted.

## What this skill does NOT do

- Does not invent actors, goals, or integration points the source use case doesn't itself name or clearly imply — this drafts from the document, not from the title alone.
- Does not draft sequence-level test scenarios — that's `generate-test-cases-from-usecase`'s job; this skill stops at story/acceptance-criteria level.
- Does not skip Step 0 — every output carries its source use case's maturity caveat.
