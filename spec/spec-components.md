# ODA Component Specifications — Extension Spec

**Status:** Draft v1
**Owner:** Lester Thomas
**Extends:** [`spec.md`](./spec.md) §5.2 (Component artefact). Read that first — this document only adds detail for the one gap it left open: TM Forum publishes each ODA Component as **two independent documents**, not one, and `spec.md` only specified how to cache the first of them.

## 1. The gap this closes

`spec.md` §5.2 caches `component.yaml` — the machine-readable Component specification from the `TMForum-ODA-Ready-for-publication` GitHub repo — plus a `component.meta.json` envelope. That is the interface contract: exposed/dependent APIs, event definitions, dependencies.

TM Forum separately publishes a **human-readable Component Specification PDF** per component — the narrative document (scope, functional description, capability tables, business context) that a person reads to understand *why* a component exists, not just what it exposes. This PDF is not linked from `component.yaml` or `component.meta.json` anywhere, is not hosted in the same repo, and — as §3 below documents — cannot be derived mechanically from the component ID. It is a distinct artefact, gated behind a distinct, undocumented discovery step, and `spec.md` v1 didn't cover it. This spec adds it, following the same principles (ID-first, provenance-in-frontmatter, mechanical boilerplate exclusion) already established for use cases (§5.1.1) and components (§5.2).

## 2. Repository layout addition

```
references/
└── components/                      # NEW — raw cache, mirrors references/use-cases/
    └── TMFC039/
        └── TMFC039_Agreement_Management_v1.1.0.pdf   # exact filename as published — see §3

knowledge/
└── components/
    └── TMFC039/
        ├── TMFC039.md                # NEW — frontmatter + converted PDF body (§4)
        ├── media/                    # NEW — images extracted from the PDF, unprocessed
        │   └── imageNN.png           #   (same convention as use-case media pre-processing, spec.md §12)
        ├── component.yaml            # unchanged — from spec.md §5.2
        └── component.meta.json       # unchanged — from spec.md §5.2
```

`TMFCxxx.md` sits as a sibling to the existing `component.yaml`/`component.meta.json`, the same way a use case's single `.md` carries its own envelope — see §4.

## 3. Discovery — why this can't be a URL pattern

§5.2.1 solved discovery for `component.yaml` with a clean rule: list the GitHub tag once, split the folder name on its first `-`. The PDF has no equivalent rule, for two compounding reasons, both confirmed empirically against all 31 components currently under `knowledge/components/`:

1. **The filename isn't derivable from the ID + short name.** Sometimes it's the full name with every word underscored (`TMFC024_Billing_Account_Management_v2.1.0.pdf`), sometimes it's the bare short name with no separators at all (`TMFC027_ProductConfigurator_v2.1.1.pdf`), sometimes a word is silently dropped (`TMFC009_Service_Qualification_v1.1.0.pdf` — the directory calls it "Service **Qualification Management**"), and casing of joining words varies (`_and_` vs `_And_`). None of this is predictable from `component-folder-map.json` or `component-list.md`.
2. **The version number in the filename routinely does not match the version already cached in `component.meta.json`.** Of the 25 components with a published PDF, only 6 had matching version numbers; the rest differed, and not always upward — e.g. `TMFC005`'s cached YAML is v1.0.4 but its PDF is v1.0.3; `TMFC007`'s YAML is v2.0.0 but its PDF is v1.2.2. See §5 — this is not a bug to reconcile, it's a real finding about how TM Forum versions these two documents independently.

**The only reliable discovery path found:** load the component's page on the TM Forum ODA Component Directory —

```
https://www.tmforum.org/oda/directory/components-map/{any-slug}/{CODE}
```

— and read the actual embedded S3 link out of the rendered page. The `{any-slug}` segment is decorative: the site's router resolves purely on the trailing `{CODE}`, confirmed by requesting `TMFC039` under a deliberately wrong category slug and getting the correct "Agreement Management" page back. A component's page also carries three fields worth capturing alongside the link: **Component version** (the YAML's version — should already match `component.meta.json`), **Component specification status**, and the **PDF's own version**, read off the extracted filename, not off the "Component version" field (§5).

This is a `find-the-real-link` step, not a `construct-the-link` step — closer in spirit to how §6.1 treats IG1228/use-case downloads (assisted, page-read, not purely mechanical) than to §5.2.1's tag-listing automation. It can still run unattended in a scripted browser (no login required, unlike §6.1's member-gated flow), but the extraction logic has to parse the page, not assemble a string.

### 3.1 "Specified" doesn't always mean a PDF exists

`component.meta.json`'s `status: specified` (§5.2) means the YAML was fetched. It does **not** guarantee a PDF was published. `TMFC062` (Resource Configuration and Activation) is `specified` — its YAML exists, cached, version `1.0.0` — but its directory page shows only a **YAML SPECIFICATION** resource block; there is no **COMPONENT SPECIFICATIONS** download block at all. Detect this by checking for the actual PDF link on the page, never by trusting `status: specified` as a proxy.

Separately, the five components already recorded as `not_yet_specified` in `knowledge/components/` (no `component.yaml` fetched — §5.2) are confirmed to have no PDF either, and the directory names/statuses for them (not previously in this repo's index) are:

| ID | Name | Directory status |
|---|---|---|
| TMFC013 | Service Balance Management | Planned |
| TMFC015 | Service Usage Management | Future |
| TMFC032 | Supply Chain Management | Planned |
| TMFC033 | Purchase Management | Planned |
| TMFC051 | Document Management | Future |

So there are two independent reasons a component can have no PDF to fetch — `Planned`/`Future` (nothing published at all, §5.2 already handles this by writing no `component.yaml`) and `specified`-but-undocumented (`TMFC062` — a new case this spec introduces: write the meta record, note the absence explicitly, don't treat a missing PDF as a fetch failure).

## 4. Data model — `knowledge/components/TMFCxxx/TMFCxxx.md`

Same envelope as `spec.md` §5.0, in frontmatter form (this artefact's content is prose, so it follows the frontmatter branch of the container-format rule in §5.0, not the sidecar-`.meta.json` branch `component.yaml` uses):

```yaml
---
id: TMFC039
type: component
name: "Agreement Management"
version: "1.1.0"                      # the PDF's OWN version — may differ from component.yaml's, see §5
status: "specified"
source:
  origin: "https://oda-production.s3.eu-west-2.amazonaws.com/v1.0.0/TMFC039_Agreement_Management_v1.1.0.pdf"
  license: RAND
  retrieved: 2026-08-29
  sha256: "<hash of the fetched pdf>"
  raw_path: "references/components/TMFC039/TMFC039_Agreement_Management_v1.1.0.pdf"
links:
  apis: []            # from the same component's exposed/dependent API tables — populated by build_index.py
  use_cases: []        # reverse links — computed only, per spec.md §5.0, never hand-authored here
# --- extension field: cross-references the sibling machine-readable artefact ---
yaml_spec_version: "1.1.0"            # component.meta.json's version, for this same component, at time of retrieval
---
```

`yaml_spec_version` exists so a reader of this file never has to open a second file to notice the two documents have drifted — see §5.

### 4.1 Content model — what's excluded

TM Forum's component PDFs share the same administrative-boilerplate shape as the use-case DOCX files documented in `spec.md` §5.1.1, and the same mechanical, heading-driven filter applies: drop the title/cover page, the copyright/IPR **Notice**, the **Table of Contents**, **Document History**/**Version History**/**Release History**, and **Acknowledgments**. Keep everything substantive: the component's overview/scope, functional description and capabilities, ODA Functional Framework mapping, exposed/dependent Open API tables, information/data model, and any component-interaction or sequence diagrams. As with `docx2md.py`, this is a whole-section keep-or-drop filter, not a summarization step.

### 4.2 Media

Diagrams embedded in the PDF are extracted into `knowledge/components/TMFCxxx/media/` with the same generic `imageNN.{png,jpeg}` naming `docx2md.py` uses for use cases, linked inline from `TMFCxxx.md` at the point each one actually appears (`pdf2md_component.py` interleaves images with prose/tables by vertical position on the page — see its own docstring), but otherwise left unprocessed. `skills/process-component-media/` (a sibling of `spec.md` §12's `process-usecase-media`, built the same way — writes to `knowledge/`, excluded from both distributable plugins) is the follow-on step that classifies, renames, and reverse-engineers these into PlantUML/text-description sidecars. Its three structured-diagram categories (component architecture overview, eTOM–SID ABE link diagrams, API/Resource/Operation diagrams) are grounded in one component's real media (`TMFC039`'s five images) — not yet confirmed exhaustive across all 25 components with a PDF, the same "shape held up on the first real component, not yet run at scale" status `process-usecase-media` itself started from.

## 5. Version drift is real, not an error to fix

The single most important finding from surveying all 31 components: **`component.yaml`'s version and the PDF specification's version are two independent numbers for the same nominal component**, and they agree in only 6 of 25 published cases. The PDF version is sometimes ahead, sometimes behind:

| Direction | Example |
|---|---|
| PDF ahead of YAML | `TMFC003`: YAML v1.1.1, PDF v2.0.0 |
| PDF behind YAML | `TMFC005`: YAML v1.0.4, PDF v1.0.3 |
| PDF behind YAML | `TMFC007`: YAML v2.0.0, PDF v1.2.2 |
| Match | `TMFC039`: both v1.1.0 |

Do not normalize, reconcile, or treat one as authoritative for the other. Record both — the envelope's own `version` field carries the PDF's version (because this artefact's `source` *is* the PDF, per §5.0's rule that `version` is "the artefact's own version string"); `yaml_spec_version` (§4) carries the YAML's, read from the already-cached `component.meta.json`. A future `assess-change-impact`-style skill (`spec.md` §11.1.2) should treat a widening gap between these two numbers as a signal worth surfacing, the same way `spec.md` §5.4 already treats matrix/frontmatter disagreement as signal rather than noise.

## 6. Full survey (as retrieved 2026-08-29)

| ID | Name | YAML version (cached) | Directory status | PDF version | PDF |
|---|---|---|---|---|---|
| TMFC001 | Product Catalog Management | 2.1.2 | specified | 2.1.2 | ✅ match |
| TMFC002 | Product Order Capture And Validation | 2.1.0 | specified | 2.1.1 | ✅ drift |
| TMFC003 | Product Order Delivery Orchestration And Management | 1.1.1 | specified | 2.0.0 | ✅ drift |
| TMFC005 | Product Inventory | 1.0.4 | specified | 1.0.3 | ✅ drift |
| TMFC006 | Service Catalog Management | 1.2.0 | specified | 1.2.1 | ✅ drift |
| TMFC007 | Service Order Management | 2.0.0 | specified | 1.2.2 | ✅ drift |
| TMFC008 | Service Inventory | 1.2.0 | specified | 1.2.1 | ✅ drift |
| TMFC009 | Service Qualification Management | 1.1.0 | specified | 1.1.0 | ✅ match |
| TMFC010 | Resource Catalog Management | 1.3.2 | specified | 1.3.1 | ✅ drift |
| TMFC011 | Resource Order Management | 1.2.0 | Pre-production | 1.1.2 | ✅ drift |
| TMFC012 | Resource Inventory | 2.2.0 | specified | 2.1.1 | ✅ drift |
| TMFC013 | Service Balance Management | — | Planned | — | ❌ none |
| TMFC014 | Location Management | 1.2.1 | specified | 1.2.0 | ✅ drift |
| TMFC015 | Service Usage Management | — | Future | — | ❌ none |
| TMFC020 | Digital Identity Management | 1.1.0 | specified | 1.1.0 | ✅ match |
| TMFC022 | Party Privacy Management | 1.1.0 | specified | 1.1.1 | ✅ drift |
| TMFC023 | Party Interaction Management | 1.1.2 | specified | 1.1.1 | ✅ drift |
| TMFC024 | Billing Account Management | 2.1.1 | specified | 2.1.0 | ✅ drift |
| TMFC027 | Product Configurator | 2.1.1 | specified | 2.1.1 | ✅ match |
| TMFC028 | Party Management | 2.1.0 | specified | 2.1.1 | ✅ drift |
| TMFC030 | Bill Generation Management | 2.0.0 | specified | 2.2.0 | ✅ drift |
| TMFC031 | Bill Calculation | 3.0.0 | specified | 2.0.0 | ✅ drift |
| TMFC032 | Supply Chain Management | — | Planned | — | ❌ none |
| TMFC033 | Purchase Management | — | Planned | — | ❌ none |
| TMFC035 | Permissions Management | 1.1.1 | specified | 1.1.0 | ✅ drift |
| TMFC036 | Lead And Opportunity Management | 1.2.0 | specified | 1.2.1 | ✅ drift |
| TMFC039 | Agreement Management | 1.1.0 | specified | 1.1.0 | ✅ match |
| TMFC040 | Product Usage Management | 1.1.0 | specified | 1.1.0 | ✅ match |
| TMFC050 | Product Recommendation Management | 1.0.0 | specified | 1.1.0 | ✅ drift |
| TMFC051 | Document Management | — | Future | — | ❌ none |
| TMFC062 | Resource Configuration and Activation | 1.0.0 | specified | — | ❌ none (§3.1) |

**25 of 31** components currently under `knowledge/components/` have a fetchable PDF specification; **6 do not** (5 genuinely unpublished — `Planned`/`Future` — plus `TMFC062`'s specified-but-undocumented case). The 25 PDF URLs, as resolved by §3's page-read method, are recorded in each component's own `TMFCxxx.md` frontmatter (`source.origin`) once fetched — not duplicated here, to avoid a second copy that can silently drift (the same reasoning `spec.md` §5.1.1 gives for dropping a use case's own References section).

## 7. Refresh

Folds into `spec.md` §6.2 (automated track) as an additional step after `fetch_component.py` refreshes `component.yaml`: for each component whose directory status shows a PDF block, re-resolve the link per §3, compare `sha256` against the cached `TMFCxxx.md` frontmatter, and only re-fetch/re-convert on change — same idempotence contract as everything else in that track (`spec.md` principle 7). Unlike `component.yaml`'s tag-pinned discovery, this step requires an actual page load per component (31 requests, not one tag listing), so it is heavier than the rest of §6.2 but still fully unattended — no login gate, same as the rest of the automated track.

## 8. Open question

Should `yaml_spec_version` (§4) be promoted into `knowledge/index/components.json` (`spec.md` §5.4) as a first-class column, so "components where the two specs have drifted" is a one-file lookup instead of a per-component read? Deferred — no skill in `spec.md` §8/§11 currently needs this cross-check; revisit if `assess-change-impact` (§11.1.2) gets built.
