# knowledge/components/ — Agent Instructions

`TMFCxxx` — ODA Components, one folder per id. Each component has up to
**two independent source documents**, cached separately:

```
knowledge/components/{TMFCxxx}/
├── component.yaml              machine-readable spec, from GitHub (spec.md §5.2)
├── component.meta.json         envelope for component.yaml
├── {TMFCxxx}.md                narrative spec, from a published PDF (spec-components.md §4)
│                                -- present for 25 of 31 ids, see below
└── media/                      diagrams from the PDF, enriched in place
```

## Rules specific to components

1. **`component.meta.json`'s `status: "specified"` means the YAML was
   fetched — it does not mean a narrative PDF (`{TMFCxxx}.md`) exists.**
   6 of 31 ids have no `{TMFCxxx}.md`: 5 are genuinely unpublished
   (`not_yet_specified`, `Planned`/`Future` — no `.md` should ever be
   created for these), and 1 (`TMFC062`) is `specified` but its PDF was
   simply never published. Read
   [`knowledge/index/component-pdf-coverage.md`](../index/component-pdf-coverage.md)
   before assuming a missing `{TMFCxxx}.md` is a fetch that was never
   attempted — it usually isn't.
2. **`component.yaml`'s version and `{TMFCxxx}.md`'s version are two
   independent numbers for the same nominal component**, and disagree in
   19 of 25 published cases (`spec-components.md` §5). Never reconcile or
   normalize them. `{TMFCxxx}.md`'s own `version:` frontmatter field is
   the PDF's version; its `yaml_spec_version:` field cross-references
   `component.meta.json`'s version at the time of retrieval — read both
   if you need to know whether a component's two documents have drifted.
3. **A component's real diagrams live in `media/` as `.puml` (PlantUML
   source, structured diagrams) or `.text-description.md` (everything
   else), not as raw images** — read those instead of the `.png`/`.jpeg`
   directly; they're cheaper and were already verified against the
   source image (`skills/process-component-media/`). If you see a file
   still named `imageNN.{png,jpeg}` under a component's `media/`, that
   component's media step hasn't run yet — treat its diagrams as
   unprocessed, not missing.
4. **A struck-through table row, a jammed-together `TMF688https://...`
   URL, a literal `"n/a"` typo, or a component with no eTOM activity
   assigned yet are all genuine artifacts of the source PDF**, confirmed
   present on the rendered page — not conversion bugs. Reproduce/report
   them as-is; don't silently "fix" what looks like an error in a
   component's own narrative.

## Provenance and regeneration

`component.yaml`/`component.meta.json` come from
`tools/fetch_component.py` (automated track, `spec.md` §6.2 — public,
unauthenticated, safe to schedule). `{TMFCxxx}.md` comes from
`tools/pdf2md_component.py`, converting a PDF that must first be located
via a real TM Forum ODA directory page load and downloaded — that
discovery+download step has no checked-in script yet (done ad hoc via a
driven browser so far; see the tool's own docstring and
`spec/tasks-components.md` Phase 8.4). Don't hand-edit any of these three
files — regenerate instead. `media/` enrichment
(`skills/process-component-media/`) does write here directly and is the
one exception.
