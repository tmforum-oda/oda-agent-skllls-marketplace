---
name: draft-new-usecase-from-scenario
description: Given a business scenario description, drafts a new TMFSxxx-shaped use-case document matching this corpus's own observed structure, citing real existing component/API ids wherever the scenario matches existing ODA capability and flagging genuine gaps rather than inventing plausible-sounding new ids. Use this when a requirement doesn't match any existing use case or known gap closely enough to just reuse.
---

# Draft New Use Case from Scenario — Skill Instructions

## When to use this, and when not to

Run `recommend-oda-components-for-requirement` against the scenario
first. Only draft a new use case if that skill reports no close match
and the scenario also doesn't match an entry in
`${CLAUDE_PLUGIN_ROOT}/knowledge/index/gaps-backlog.md` — if it does match a known gap, the
right next step is `propose-component-or-api-extension` against that
gap, not a brand-new use case document.

## Step 1 — Structure the draft against the corpus's own observed shape

This corpus's use cases consistently follow this section order (heading
wording varies slightly document to document, but the shape holds):

```
# Executive Summary
# Introduction
  ## Context or Background
  ## Objective of the use case
  ## Scope and assumptions
# Description
# Information View          (optional -- catalog/data model views, if relevant)
# Sequence diagrams
# Conclusion
  ## Lessons learned
  ## Impacts identified
# Appendix                  (optional)
```

Draft the new document in this order. Don't invent a different structure
even if it seems like a cleaner fit for the scenario — consistency with
the corpus is what lets this document convert cleanly through the same
pipeline every other use case went through, and lets a reader who knows
this corpus navigate it without relearning a new shape.

## Step 2 — Cite real ids wherever the scenario touches existing capability

For every component/API the draft scenario would plausibly use, check
`${CLAUDE_PLUGIN_ROOT}/knowledge/index/{components,apis}.json` first. If a real match exists,
cite it by id and name — don't invent a new id for something that
already exists. Building this draft is exactly the situation
`generate-test-cases-from-usecase`'s citation discipline exists for: an
id that doesn't trace back to something real in `${CLAUDE_PLUGIN_ROOT}/knowledge/` doesn't
belong in the draft.

## Step 3 — Flag genuine gaps using the corpus's own convention, don't assign new ids

Where the scenario needs a capability that genuinely doesn't exist yet,
mark it the same way TM Forum's own authors already do in this corpus —
literal `TMFCxxx`/`TMFxxx` placeholder text (no real digits), not a
guessed next-available number. Check `${CLAUDE_PLUGIN_ROOT}/knowledge/index/gaps-backlog.md`
first — the gap the scenario needs might already be identified and
tracked there (cite the existing gap-backlog entry instead of writing a
fresh, uncorrelated placeholder), or it might be genuinely new (mark it
as a new, uncorrelated gap and say so explicitly, since it hasn't been
cross-corroborated by any other use case yet).

## Step 4 — Frontmatter is a draft stub, not a finished envelope

A draft has no real catalog page yet, so the catalog-only fields
(`maturity`, `approval_status`, `release_status`, `team_approved`,
`published`, `source.origin`/`retrieved`/`sha256`) can't be filled in for
real. Leave them as `TODO`, the same convention `docx2md.py` uses before
`add_usecase_metadata.py` runs — don't fabricate plausible-looking dates
or a maturity level for a document that hasn't been through TM Forum's
own review process at all yet. `id` should be left as `TMFSxxx-DRAFT` (no
real number) until TM Forum actually assigns one — this repo's own id
registry (`${CLAUDE_PLUGIN_ROOT}/knowledge/index/usecase-list.json`) is the authority on real
ids, not this skill.

## Output format

A Markdown document following Step 1's structure, with every
component/API citation resolved per Step 2/3, and a frontmatter stub per
Step 4. Close with a short "What's grounded vs. proposed" summary: which
components/APIs are real existing capability the draft reuses, and which
are gaps the draft depends on that don't exist yet.

## What this skill does NOT do

- Does not assign a real `TMFSxxx`/`TMFCxxx`/`TMFxxx` id to anything — id assignment is TM Forum's own process, not this skill's to simulate.
- Does not submit the draft anywhere — this is a starting document for a human contributor to take into TM Forum's own review process, the same posture `feedback-propose-matrix-correction` and `propose-component-or-api-extension` take toward their own outputs.
- Does not skip checking `recommend-oda-components-for-requirement` and `gaps-backlog.md` first — drafting a redundant new use case when a close match or known gap already exists wastes the reviewer's time.
