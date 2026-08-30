# knowledge/index/

The ID registry and cross-reference layer for the whole corpus. Every
"what exists, and what links to what" question about `use-cases/`,
`components/`, or `apis/` should be answerable from a file in this
folder, without scanning those folders directly.

If you're an AI agent, read [`AGENTS.md`](AGENTS.md) here first.

## Files

| File | What it answers |
|---|---|
| `use-cases.json` / `components.json` / `apis.json` | the full corpus, one row per artefact, with forward and reverse links |
| `usecase-list.json` | every `TMFSxxx` id IG1228 knows about, including `planned`/`not available` ones with nothing converted yet |
| `usecase-component-matrix.json` | IG1228's own corpus-level "which use case touches which component" table |
| `matrix-discrepancies.md` | where a use case's own document disagrees with that matrix — read **both** sources for a complete answer |
| `gaps-backlog.md` | capability gaps TM Forum's own authors already flagged in use cases' "Lessons learned" sections — proposed components/APIs that don't exist yet, consolidated across every use case that raises each one |
| `component-pdf-coverage.md` | which ODA Components have no narrative PDF, and why (two different, legitimate reasons) |
| `id-registry.md` | the ID prefix glossary (`TMFSxxx`/`TMFCxxx`/`TMFxxx`/`GBxxx`/`IGxxxx`) |
| `component-folder-map.json` / `api-samples-folder-map.json` | id → upstream GitHub folder lookups, internal to `tools/fetch_*.py` |

## Generated vs. static

`use-cases.json`, `components.json`, and `apis.json` are fully generated
— regenerate with `python tools/build_index.py` (idempotent, safe to
re-run any time). Everything else in this folder is either static and
hand-maintained (`id-registry.md`, `gaps-backlog.md`,
`matrix-discrepancies.md`, `component-pdf-coverage.md` — never touched by
an automated refresh) or produced by a one-off extraction from IG1228
that's re-run only when IG1228 itself is republished
(`usecase-list.json`, `usecase-component-matrix.json`).

See [`spec/spec.md`](../../spec/spec.md) §5.4 for the full design
rationale behind the index layer.
