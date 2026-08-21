---
name: check-usecase-maturity
description: Given a TM Forum ODA use-case id (TMFSxxx), reads its cached frontmatter and returns a plain-language maturity/trust verdict -- whether it's safe to build against today. Reads only YAML frontmatter, no document-body parsing. Use this before starting requirements or test-case work against any TMFSxxx use case.
---

# Check Use-Case Maturity — Skill Instructions

## What this skill answers

"Is TMFSxxx safe to build against right now?" — a plain-language verdict,
not a raw dump of frontmatter fields. Reads only YAML frontmatter, zero
document-body prose parsing.

## Where the data lives

Given an id like `TMFS030`, the file is at a known path — no directory scan,
no search:

```
${CLAUDE_PLUGIN_ROOT}/knowledge/use-cases/{ID}/{ID}.md
```

Read just the YAML frontmatter block (between the two `---` lines at the
top). The fields that matter for this skill:

| Field | Meaning |
|---|---|
| `maturity` | `Alpha` / `Beta` / `GA` — how settled the use case's *content* is |
| `approval_status` | `Member Evaluated` / `Team Approved` / `TM Forum Approved` — how much TM Forum review it's had |
| `release_status` | `Pre-production` / `Production` — TM Forum's own publication-track label |
| `version` | the document's own version string, for citing in the verdict |

`status` is just `"{maturity} - {approval_status}"` concatenated — don't
re-derive it, and don't rely on it alone either. `maturity` and
`approval_status` are surfaced as separate fields specifically because they
can, and do, disagree — see the decision table below.

If the file doesn't exist at that path, say so plainly — don't guess a
nearby id or silently fall back to the matrix/index files. A missing use
case isn't this skill's job to explain; point at
`${CLAUDE_PLUGIN_ROOT}/knowledge/index/usecase-list.json`'s `status_in_ig1228` field if the
caller wants to know why it isn't there.

## Decision table

Do not treat `maturity: GA` alone as "safe." TM Forum's own catalog
listing marks every `Available` document identically, whether it's a
year-stable GA spec or a first-draft Alpha — and `GA` maturity and `TM
Forum Approved` approval do NOT always travel together. `TMFS008` and
`TMFS019A` are both `maturity: GA` but only `approval_status: Team
Approved`, not `TM Forum Approved` — a real, current example in this
corpus, not a hypothetical edge case. Read both fields, always; never
shortcut to a verdict from `maturity` alone.

| `maturity` | `approval_status` | Verdict |
|---|---|---|
| `GA` | `TM Forum Approved` | **Safe to build against.** Fully reviewed and stable; treat as a firm dependency. |
| `GA` | `Team Approved` | **Content is settled, sign-off is not yet complete.** The use case itself won't change shape, but it hasn't cleared full TM Forum review — flag this distinction explicitly rather than reporting it as equivalent to a fully-approved GA document. |
| `Beta` | `Member Evaluated` | **Provisional — expect changes.** Usable for early exploration or a spike, not as a committed dependency. Re-check before any deliverable ships against it. |
| `Alpha` | `Member Evaluated` | **First draft. Do not build production dependencies on this yet.** Treat any component/API links from this use case as directional, not final. |
| anything else | anything else | Don't force it into the rows above — state the raw `maturity`/`approval_status` pair and say explicitly that this combination hasn't been seen in the corpus before, rather than silently picking the nearest row. |

`release_status: Pre-production` vs `Production` is TM Forum's own separate
publication-track signal — report it alongside the verdict (e.g. "GA / TM
Forum Approved, but still Pre-production release status") rather than
folding it into the maturity/approval verdict above; it's supporting
evidence, not a fifth row of the table.

## Output format

A short verdict, not a field dump. Example, for `TMFS030`:

> **TMFS030** (v1.1.0) — Beta / Member Evaluated, Pre-production release
> status. Provisional — expect changes; usable for exploration, not yet as
> a committed dependency.

Always cite the id, version, and both `maturity`/`approval_status` verbatim
(not paraphrased) alongside the plain-language verdict, so a reader can see
the raw fields the verdict was derived from and disagree with the
interpretation if they want to.

## What this skill does NOT do

- Does not read the use case's body (Executive Summary, Description,
  sequence diagrams) — that's `capture-requirements-from-usecase` /
  `generate-test-cases-from-usecase`'s job.
- Does not resolve component/API links or check whether *those* are
  `not_yet_specified`/`fetch_failed` — this skill is about the use case
  document's own maturity, not its dependencies' maturity. (A natural
  follow-on skill, not built yet: cross-check a use case's linked
  components/APIs for their own status too.)
- Does not query TM Forum's website — everything it needs is already in
  `${CLAUDE_PLUGIN_ROOT}/knowledge/`; a skill must be able to answer "is this safe to build
  against?" without a network call.
