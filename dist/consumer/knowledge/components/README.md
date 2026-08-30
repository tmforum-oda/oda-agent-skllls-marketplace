# knowledge/components/

31 TM Forum ODA Components (`TMFCxxx`) — the reusable building blocks of
the Open Digital Architecture. Each component folder can hold up to two
independent cached documents plus enriched media.

If you're an AI agent, read [`AGENTS.md`](AGENTS.md) here first.

## Layout

```
TMFC001/
├── component.yaml          machine-readable spec (exposed/dependent APIs,
│                           events) -- fetched from TM Forum's public
│                           GitHub repo, spec.md §5.2
├── component.meta.json     envelope for component.yaml
├── TMFC001.md              human-readable narrative -- scope, functional
│                           description, ODA Functional Framework mapping,
│                           API tables -- converted from the published
│                           Component Specification PDF, spec-components.md
└── media/                  diagrams from the PDF: component architecture
                            overview, eTOM-SID ABE link diagram, and
                            API/Resource/Operation diagrams, each as a
                            verified .puml (PlantUML) sidecar
```

**25 of the 31 components have a `TMFCxxx.md`** — the other 6 don't, for
two different, both-legitimate reasons documented in
[`knowledge/index/component-pdf-coverage.md`](../index/component-pdf-coverage.md):
5 have nothing published yet at all, and 1 (`TMFC062`) has a machine
spec but no narrative PDF was ever released.

## Two documents, two version numbers

TM Forum publishes a component's machine-readable YAML and its
human-readable PDF **on independent schedules** — the two often carry
different version numbers for the same nominal component (agreeing in
only 6 of 25 cases surveyed). This is real, not an error: see
[`spec/spec-components.md`](../../spec/spec-components.md) §5 for
concrete examples and why neither number is normalized to match the
other.

## Regenerating

```bash
python tools/fetch_component.py <TMFCxxx>       # component.yaml + .meta.json, automated, no login
python tools/pdf2md_component.py <TMFCxxx> ...  # TMFCxxx.md, once the PDF is already downloaded
```

Locating and downloading a component's PDF isn't yet a checked-in script
— see `tools/pdf2md_component.py`'s own docstring header and
[`spec/tasks-components.md`](../../spec/tasks-components.md) Phase 8.4.
Media enrichment (renaming raw images, writing PlantUML) is its own step:
[`skills/process-component-media/`](../../skills/process-component-media/SKILL.md).
