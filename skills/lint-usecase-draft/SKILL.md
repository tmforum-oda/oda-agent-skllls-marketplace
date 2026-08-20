---
name: lint-usecase-draft
description: Checks a draft TM Forum use-case DOCX or Markdown document's structure against document shapes known to convert badly through this repo's own docx2md.py pipeline, and flags anything likely to silently lose content before the document is ever submitted. Use this as a pre-submission QA pass for someone authoring a new or revised use case.
---

# Lint Use-Case Draft — Skill Instructions

## What this skill checks

Whether a draft use-case document, if run through this repo's conversion
pipeline, would convert cleanly or silently lose real content. This
isn't a generic writing-style linter — every check here traces to a
specific, real way a document's structure can defeat mechanical
extraction, not a stylistic preference.

## Check 1 — References section header phrasing and formatting

The component/API extraction is driven by scanning for `TMFCxxx`/`TMFxxx`
id patterns wherever they appear in the document — but a References
section header formatted as a numbered/bulleted list item (rather than a
plain heading) or worded unusually ("TMF references", "The following
documents are referenced...") can still confuse a reader trying to
locate the section at all. Flag if:

- The References section (or equivalent) doesn't contain a clearly
  labeled subheading naming components and one naming APIs.
- Component/API ids are listed as prose sentences rather than one
  id-bearing item per line — harder for both a human reviewer and
  mechanical extraction to parse reliably.

## Check 2 — One component/API entry per line, no manual line breaks bundling several together

A single list item that packs multiple component or API entries together
using manual line breaks (soft returns within one bullet, rather than
separate bullets) is a real risk: mechanical extraction can end up
treating the whole bundled block as one entry, corrupting both entries.
Flag any References-section bullet that names more than one `TMFCxxx`/
`TMFxxx` id — each id should be its own list item.

## Check 3 — Title block clearly states id and name together, unambiguously

Flag a title block that:
- States only the name, with the bare `TMFSxxx` id appearing later,
  separated by boilerplate ("TM Forum Use Case", version info, etc.)
  rather than adjacent to the name.
- Uses a combined `<ID> <name>` line without a clear separator (e.g. a
  colon or dash) between the id and the name.
- Doesn't state the id at all on the title page, relying on the filename
  or a later reference to establish it.

A title block reading `"Use Case: <Name>"` or `"<ID>: <Name>"`, with the
id unambiguous and adjacent to the name, is the clean, safe shape.

## Check 4 — Placeholder ids, if used, follow the corpus's own convention

If the draft needs to reference a capability that doesn't have a real id
yet, check it uses the literal `TMFCxxx`/`TMFxxx` placeholder pattern (no
real digits) consistently — not a mix of styles (`TMFC-NEW`, `TMFCxx`,
`[component name]`) that a reader or future extraction pass might not
recognize as "not yet assigned."

## Output format

A checklist against the four checks above, each either "clean" or
flagged with the specific location/quote in the draft that trips it and
what to change. Don't report a check as failed without quoting the
specific text that fails it — a vague "References section formatting
could be clearer" isn't actionable the way "the TMFC020/TMFC023 bullet on
page 4 bundles two ids into one line break-separated item" is.

## What this skill does NOT do

- Does not check writing style, grammar, or content completeness — only the four structural patterns above, each tied to a specific extraction failure mode.
- Does not run the actual conversion pipeline — this is a manual-review checklist based on known failure patterns, not a substitute for actually testing the document through `docx2md.py` if that's available.
- Does not assume every flagged pattern is definitely wrong for this specific document — a title block that looks unusual per Check 3 might still convert fine; flag it as worth a second look, not as a certain failure.
