# Component PDF coverage

Static, hand-maintained note — not generated, not touched by `tools/fetch_component.py`
or `tools/build_index.py` (neither script reads or writes files under `knowledge/index/`
other than the specific generated files they each own), so it survives a refresh cycle
that would otherwise leave "why is there no `TMFCxxx.md`?" unanswered. Same convention as
`id-registry.md`.

25 of the 31 `TMFCxxx` component folders have a `TMFCxxx.md` narrative file, converted from
a published ODA Component Specification PDF (`tools/pdf2md_component.py`, `spec/tasks-components.md`
Phases 1–6). The other 6 do not, for two genuinely different reasons — see
`spec/spec-components.md` §3.1/§6 for the full survey this is drawn from:

## No `component.yaml` at all — nothing published yet

`TMFC013`, `TMFC015`, `TMFC032`, `TMFC033`, `TMFC051` — directory status `Planned`/`Future`.
`tools/fetch_component.py` correctly writes a meta-only record (`status: "not_yet_specified"`,
no `component.yaml`) for these per `spec/spec.md` §5.2. No PDF exists to fetch, and no
`TMFCxxx.md` should ever be created for these while they remain in this state — that would be
fabricated content standing in for a document that doesn't exist yet.

## Has `component.yaml`, but still no PDF: `TMFC062`

`TMFC062` (Resource Configuration and Activation) is the one exception to "`status: specified`
means a PDF exists." Its `component.yaml` was fetched and cached normally (`status: "specified"`,
version `1.0.0`), but its TM Forum directory page has only a **YAML SPECIFICATION** download
block — no **COMPONENT SPECIFICATIONS** (PDF) block at all. Confirmed by loading the directory
page directly, not inferred from the YAML alone (`spec/spec-components.md` §3.1).

**No `TMFC062.md` exists, and this is expected, not a gap in this pipeline's work** — there is
no PDF to convert. If a future refresh of `spec/spec-components.md` §6's survey ever finds a PDF
now published for `TMFC062`, this note should be deleted and `TMFC062` converted normally
through the same pipeline as the other 25.
