# ODA Knowledge Base — Specification

**Status:** Draft v1
**Owner:** Lester Thomas
**Scope of this document:** what we're building, why it's organized the way it is, and what "done" looks like for the pilot. Build steps live in [`tasks.md`](./tasks.md).

## 1. Purpose

We want a set of **Agent Skills** that use TM Forum's Open Digital Architecture (ODA) source knowledge to accelerate specific steps of the software delivery lifecycle — starting with:

- capturing business requirements (from a use case's Description/Scope into user stories or acceptance criteria),
- generating test cases and test data (from a use case's sequence diagrams and the API schemas it calls),
- validating a design (checking a proposed component/API design against what ODA already specifies).

Skills are only as good as the knowledge they read. Today that knowledge is a pile of member-gated DOCX/PDF files with no consistent shape, no links between a use case and the components/APIs it depends on, and no way to tell a document that's been stable for a year from one still in first-draft review. This spec defines a **repository layout, provenance model, and linking scheme** that fixes that — organized around how a skill will actually query it, not around how TM Forum happens to publish it.

This is informed by hands-on work already done in this repo: six TMFSxxx use cases (TMFS001, 002, 009, 029, 030, 031) were downloaded and converted to Markdown, and the ODA GitHub repos (`oda-canvas`, `reference-example-components`) were audited for how they already publish Component specs and Open APIs as machine-readable data and package contributor tooling as Claude-format Agent Skills. See [`../references/`](../references/) for the pilot conversions and the research artifact referenced in project history for the full audit.

## 2. Pilot scope

**In scope for v1:**

- **IG1228** ("How to use ODA – Using Open APIs to Realize Use Cases") as the index/entry point.
- Every standalone **TMFSxxx use case** IG1228 currently references (~32 identifiers at v31.0.0, not all published yet — see §6.3 on status).
- For every **ODA Component (TMFCxxx)** a use case's References section names: the Component specification, vendored or linked (§5).
- For every **Open API (TMFxxx)** a component exposes or a use case calls: the OpenAPI/Swagger spec, vendored or linked (§5).
- A **refresh process** that works with TM Forum's actual publication cadence (IG1228 has released roughly every 4–8 weeks since Oct 2020 — see its own version history).

**Out of scope for v1** (future extensions the layout must not preclude — see §7):

- eTOM (Business Process Framework) and SID (Information Framework) — these are Sparx EA models/posters/Excel exports, not documents with a DOCX→Markdown path. They need a separate XMI export pipeline. Reserve the namespace; don't build it yet.
- An MCP server or any network-facing interface. v1 skills read the filesystem directly.
- Automating the member-gated download step itself (§6.1) — TM Forum requires a logged-in member session; this cannot be a headless cron job without sharing credentials, which is out of scope on policy grounds, not just effort.
- IG1242 (ODA Component Inventory) as an independently maintained artefact — for v1 we only need the maturity/status fields already present on each document's own catalog page (§6.3), not a full mirror of IG1242.

## 3. Design principles

1. **ID-first, not title-first.** TM Forum document titles drift between versions (TMFS001's own in-document title literally differs from its catalog title). Every path, filename, and cross-reference is keyed on the stable identifier (`TMFS001`, `TMFC020`, `TMF632`), never on the title.
2. **One current version per artefact, versioned by git.** We store the latest version of each document at a stable path and let git history be the version history — mirroring how TM Forum itself treats "Production version" as the one that matters, with everything else archived. No `TMFS001_v5.0.4/`, `TMFS001_v5.0.5/` sibling folders.
3. **Separate raw input from processed knowledge.** `references/` (already in this repo) is the raw cache of what was actually downloaded — DOCX/PDF, unmodified, kept for provenance and re-conversion. `knowledge/` is the generated, agent-facing corpus. Skills read `knowledge/`, never `references/`. Everything under `knowledge/` should be regeneratable from `references/` plus the public GitHub/S3 sources.
4. **Provenance travels with the content.** Every file in `knowledge/` carries frontmatter recording where it came from, when it was fetched, and what its maturity/approval status was at that time. A skill must be able to answer "is this safe to build against?" without a network call — see §6.3, motivated directly by the finding that IG1228's own index marks GA and Alpha documents identically as `Available`.
5. **Links are data, not prose.** A use case's dependency on `TMFC020` or `TMF632` is a structured field in frontmatter, not just a sentence in a References section. This is what makes `trace-usecase-impact`-style skills possible without re-parsing Markdown prose.
6. **Optimize for a skill doing a single lookup.** A skill answering "what does TMFS001 require" should need one file read at a known path, not a directory scan. A skill answering "which use cases touch TMFC003" needs one index file, not a corpus grep. See §4 and §5.4.
7. **Idempotent regeneration.** Running the conversion/index pipeline twice on unchanged inputs produces byte-identical output. This is what makes the 8-week refresh cheap and diffable (§6).
8. **An artefact holds knowledge, not boilerplate.** The copyright/IPR notice, the title-page metadata block, the "Table of Contents," and the acknowledgments/version-history appendix are the same handful of paragraphs repeated in every TM Forum document and add nothing an agent can reason with. None of it belongs in `knowledge/`. What TM Forum treats as front-matter-the-English-word (a notice page) is not what we mean by frontmatter-the-YAML-block — see §5.0.
9. **One envelope, shared by every artefact type.** A use case, a component spec, and an API spec are different shapes of content, but "what is this, what version, is it safe to use, what does it link to" is the same five-field question regardless of type. Every artefact answers it the same way, so a skill or index-builder never needs type-specific code just to find out what something *is* — only to read what it *contains*. See §5.0.

## 4. Repository layout

```
tm-forum-sdlc/
├── spec/
│   ├── spec.md                      # this file
│   └── tasks.md                     # build plan
├── references/                      # RAW cache — unmodified downloads, kept for provenance/re-conversion
│   ├── ig1228/
│   │   └── IG1228_v{version}.pdf
│   └── use-cases/
│       └── TMFS001/
│           └── TMFS001_v{version}.docx
├── knowledge/                       # PROCESSED — what skills actually read
│   ├── use-cases/
│   │   └── TMFS001/
│   │       ├── TMFS001.md           # frontmatter + converted body (§5.1)
│   │       └── media/
│   │           ├── image01.png
│   │           └── ...
│   ├── components/
│   │   └── TMFC020/
│   │       ├── component.yaml       # cached ODA Component spec (§5.2)
│   │       └── component.meta.json  # provenance for the cached file
│   ├── apis/
│   │   └── TMF632/
│   │       ├── TMF632_v4.0.0.json   # cached OpenAPI/Swagger spec (§5.3)
│   │       ├── TMF632_v4.0.0.meta.json
│   │       └── samples/             # OPTIONAL, org-access-gated enrichment (§5.3.1) — absent is fine
│   │           └── Party_create_1_request.sample.json
│   ├── etom/                        # RESERVED — empty in v1, see §7
│   ├── sid/                         # RESERVED — empty in v1, see §7
│   └── index/
│       ├── use-cases.json           # catalog: envelope + extensions, path, links.components[], links.apis[]
│       ├── components.json          # catalog: envelope + reverse links.use_cases[], path
│       ├── apis.json                # catalog: envelope + reverse links.use_cases[], path
│       ├── usecase-component-matrix.json   # bipartite graph extracted from IG1228 ch.2 (§5.4)
│       ├── component-folder-map.json       # {id: folder_name} from the v1.0.0 tree listing (§5.2.1)
│       └── id-registry.md           # the ID prefix glossary (§4.1)
├── tools/
│   ├── docx2md.py                   # DOCX → Markdown converter incl. boilerplate strip (already built, §5.1/§5.1.1)
│   ├── fetch_component.py           # builds component-folder-map.json, pulls each Component YAML (§5.2.1)
│   ├── fetch_api.py                 # follows specification[].url from a cached component to fetch its APIs (§5.3.1)
│   ├── extract_usecase_matrix.py    # parses IG1228 ch.2 into usecase-component-matrix.json
│   ├── build_index.py               # regenerates index/*.json from knowledge/**/*.md + *.yaml frontmatter
│   └── refresh_report.py            # diffs this run's index against the last committed one, writes a changelog entry
├── CHANGELOG.md                     # human-readable refresh history (generated + hand-annotated)
└── skills/                          # pilot Agent Skills consuming knowledge/ (§6, built last)
    └── ...
```

### 4.1 ID registry

| Prefix | Means | Example | Where it lives |
|---|---|---|---|
| `IGxxxx` | Introductory Guide (often an index/inventory doc) | `IG1228` | not vendored in full; only its extracted matrix is (`index/usecase-component-matrix.json`) |
| `TMFSxxx` | Standalone Use Case | `TMFS001` | `knowledge/use-cases/TMFSxxx/` |
| `TMFCxxx` | ODA Component | `TMFC020` | `knowledge/components/TMFCxxx/` |
| `TMFxxx` | TM Forum Open API | `TMF632` | `knowledge/apis/TMFxxx/` |
| `GBxxx` | Guidebook (eTOM = GB921, SID = GB922) | `GB921` | reserved, §7 |

This table is also written to `knowledge/index/id-registry.md` so a skill (or a person) can resolve an unfamiliar ID without leaving the repo.

## 5. Data model

### 5.0 The universal envelope

Every knowledge artefact — regardless of type — answers the same five questions the same way. This is the envelope; every artefact has it, nothing type-specific is allowed to shadow or rename these keys.

| Field | Meaning | Example |
|---|---|---|
| `id` | Stable identifier, never the title | `TMFS001` |
| `type` | `use-case` \| `component` \| `api` \| (reserved: `etom-process`, `sid-entity`) | `use-case` |
| `name` | Human-readable name, for display only — never used as a key or path segment | `New Party – Create your account` |
| `version` | The artefact's own version string, as TM Forum publishes it | `5.0.5` |
| `status` | One-line, human-and-agent-readable rollup of "is this safe to use" | `GA · TM Forum Approved` |
| `source` | Nested: `origin` (URL), `license` (IPR mode), `retrieved` (date fetched), `sha256` (hash of the fetched file), `raw_path` (only when a distinct raw file exists — omitted for components/APIs, where the fetched file *is* the knowledge artefact) | — |
| `links` | Nested: `components: []`, `apis: []`, `use_cases: []` — ids only, of related artefacts. **Forward links** (what this artefact declares it depends on) are authored at conversion time. **Reverse links** (what depends on this artefact) are computed by `build_index.py` and live only in the index files (§5.4) — never written back into a source artefact's own envelope. Writing computed data back into source files would break idempotence (principle 7). | — |

**Container format follows content format, not the other way round.** Where the source content is prose (a use case today; eTOM/SID prose sections later), the envelope is a YAML frontmatter block on top of Markdown body text — a person and a model both read it the same way, top to bottom. Where the source content is *already* structured data (a Component spec, an OpenAPI schema), we do not degrade it into Markdown prose to make room for frontmatter — that would lose precision an agent generating test data actually needs. The native file (`component.yaml`, `TMFxxx_v{version}.json`) is kept untouched, and the envelope lives in a sidecar `*.meta.json` next to it, using the exact same field names as frontmatter. A skill or `build_index.py` reads the envelope the same way either way; only the container differs.

Type-specific fields extend the envelope — they never replace or duplicate what's already in it. A use case's `maturity` / `approval_status` / `release_status` are more granular than the envelope's rollup `status` string; a skill that only needs a quick trust check reads `status`, one that needs the precise TM Forum vocabulary reads the extension fields.

### 5.1 Use case (`knowledge/use-cases/TMFSxxx/TMFSxxx.md`)

```yaml
---
id: TMFS001
type: use-case
name: "New Party – Create your account"
version: "5.0.5"
status: "GA · TM Forum Approved"
source:
  origin: "https://www.tmforum.org/resources/technical-specification/tmfs001-use-case-new-party-create-your-own-account-v5-0-5/"
  license: RAND
  retrieved: 2026-08-19
  sha256: "<hash of the raw docx>"
  raw_path: "references/use-cases/TMFS001/TMFS001_v5.0.5.docx"
links:
  components:
    - id: TMFC020
      name: Digital Identity Management
      spec_version: "1.0.0"
    - id: TMFC022
      name: Party Privacy Management
      spec_version: "1.0.0"
    - id: TMFC023
      name: Party Interaction Management
      spec_version: "1.0.0"
    - id: TMFC028
      name: Party Management
      spec_version: "1.2.0"
    - id: TMFC035
      name: Permissions Management
      spec_version: "1.0.0"
  apis:
    - id: TMF632
      name: Party Management
      api_version: v4
    - id: TMF644
      name: Privacy Management
      api_version: v4
    # ... one entry per API named in the source document's References section
  use_cases: []          # populated by build_index.py — related/successor use cases, not hand-authored
# --- extension fields: use-case-specific, beyond the universal envelope ---
maturity: GA                          # Alpha | Beta | GA
approval_status: "TM Forum Approved"  # e.g. "Member Evaluated"
release_status: Production            # Production | Pre-production
team_approved: 2025-04-24
published: 2025-05-19
sid_references:
  - "Communication Interaction ABE"
  - "Party ABE"
  - "Digital Identity ABE"
  - "Party Privacy ABE"
---
```

**Why frontmatter and not a separate metadata file:** a skill reading one use case needs exactly one file read, and the metadata a skill needs most often (`status`, `links.components`, `links.apis`) is right next to the prose it'll quote from.

#### 5.1.1 Content model — what's excluded

The knowledge artefact is the substance, not the document TM Forum wrapped it in. The following sections exist in every source DOCX, are identical (or near-identical) boilerplate in all of them, and are **dropped entirely** by the converter rather than carried into `knowledge/`:

| Source section | Why it's dropped |
|---|---|
| Title block (`TM Forum Use Case`, title, ID, maturity table) | Fully redundant with the envelope — `name`, `id`, `status`, `version` already say this |
| `Notice` (copyright/IPR paragraphs, "AS IS" disclaimer, patent-claim boilerplate, TM Forum office address) | Identical text in every TM Forum document; carries the *fact* of the license (`source.license: RAND`), not any information a skill needs to reason with |
| `Table of Contents` | Always empty after conversion (it's a generated TOC field in the DOCX); the Markdown heading structure *is* the table of contents |
| `References` subsection | Fully re-expressed as `links.components` / `links.apis` / `sid_references` — keeping the prose bullet list too would just be the same facts said twice, and the two copies could drift |
| `Administrative Appendix` → `Document History` (Version History table, Release History table) | Redundant with `version`, `team_approved`, `published`, and — per principle 2 — with git history itself |
| `Administrative Appendix` → `Acknowledgments` | Named contributors and companies; zero SDLC value, and about the people who wrote the standard rather than what it says |

Everything else — Introduction/Executive Summary, Context, Objective, Scope, Assumptions, Description, Information View, Sequence Diagrams, Conclusion, Lessons Learned, Impacts Identified, and any named Appendix that isn't the Administrative one — is substantive and is kept in full, including its diagrams.

This is a **mechanical, heading-name-driven filter**, not a summarization step — nothing is rewritten or shortened, whole sections are either kept verbatim or dropped whole. The heading text for each dropped section is consistent across all six pilot documents (`Notice`, `Table of Contents`, `Administrative Appendix`, `Document History`, `Version History`, `Release History`, `Acknowledgments`), so the filter is a fixed heading-name list in `tools/docx2md.py`, not a fuzzy heuristic — see `tasks.md` Phase 0.

### 5.2 Component (`knowledge/components/TMFCxxx/component.yaml`)

This is the actual TM Forum Component specification YAML, fetched unmodified from the public, tagged `tmforum-rand/TMForum-ODA-Ready-for-publication` repository — already machine-readable at the source, so there is no conversion step and nothing to strip, only caching + an envelope.

#### 5.2.1 Discovery — going from a component ID to its spec URL

A component's folder name isn't just its ID — it's `{ID}-{ShortName}` (e.g. `TMFC020-DigitalIdentityManagement`), and the spec file inside repeats the same compound name (`Specification/{ID}-{ShortName}.yaml`). The ID alone isn't enough to build the URL; the short name has to be known too. **We don't invent a way to solve this — TM Forum's own tooling already has, and we reuse it exactly:**

`tmforum-oda/reference-example-components`, in `skills/create-oda-component/references/component-list.md`, maintains a hand-checked Markdown table of every published component (`TMFC001` … `TMFC062`) mapped to its short name and functional block, states the URL pattern —

```
https://raw.githubusercontent.com/tmforum-rand/TMForum-ODA-Ready-for-publication/v1.0.0/{CODE}-{ShortName}/Specification/{CODE}-{ShortName}.yaml
```

— and gives the fallback for confirming a folder name it doesn't have memorized: `https://api.github.com/repos/tmforum-rand/TMForum-ODA-Ready-for-publication/contents/?ref=v1.0.0`, which lists every folder at the pinned tag directly.

We do the same thing mechanically instead of by hand: `tools/fetch_component.py` calls that same contents-listing endpoint **once per refresh** (§6.2), builds an `{id: folder_name}` map from the results (a folder is always `{ID}-{ShortName}`, so splitting on the first `-` recovers both halves), caches it as `knowledge/index/component-folder-map.json`, and only then constructs each spec URL. This is the automated equivalent of `component-list.md` — same data, generated instead of hand-maintained, so it can't go stale between ODA releases.

Sibling `component.meta.json` carries the envelope (§5.0):

```json
{
  "id": "TMFC020",
  "type": "component",
  "name": "Digital Identity Management",
  "version": "1.0.0",
  "status": "Specified",
  "source": {
    "origin": "https://raw.githubusercontent.com/tmforum-rand/TMForum-ODA-Ready-for-publication/v1.0.0/TMFC020-DigitalIdentityManagement/Specification/TMFC020-DigitalIdentityManagement.yaml",
    "license": "RAND",
    "retrieved": "2026-08-19",
    "sha256": "<hash>"
  },
  "links": { "apis": [], "use_cases": [] }
}
```

`status` here uses IG1242's own vocabulary (`Future` | `Planned` | `Specified` | `Prototype` | `Available`) rather than the use case's `Alpha`/`Beta`/`GA` — the two artefact types are at different points in genuinely different lifecycles, and forcing one vocabulary onto both would be lossy in one direction or the other. If a use case references a component whose status is `Planned` or `Future`, there is no spec YAML to fetch yet: write only `component.meta.json` (`status` set accordingly, `source.sha256` omitted) and no `component.yaml` — a skill checking for the file's existence gets a clean, unambiguous answer instead of a 404 it has to interpret.

#### 5.2.2 Found but deliberately out of scope for v1

Each component's folder in `TMForum-ODA-Ready-for-publication` holds more than the spec: a `ComponentConformanceProfile/` (a PDF+DOCX conformance report — same document-shaped problem as eTOM/SID, §7) and a `CTK/` (Component Test Kit) with a full Helm reference-implementation chart *and* a set of Gherkin `.feature` files exercising that component's APIs, some of which explicitly reference other components' IDs (`TMFC001`'s CTK includes `TMFC002_ProductOrder.feature`, `TMFC005_ProductInventory.feature`, etc. — components are tested against each other, not in isolation). This is real, valuable, and squarely aimed at exactly the "generate test cases" goal in §1 — but it's a v2 addition, not v1: pulling it in now would mean building a second conversion pipeline (Gherkin + Helm, not DOCX) before the first one (use cases) has even scaled past the pilot. Note it here so it isn't rediscovered from scratch later; don't build against it yet.

### 5.3 API (`knowledge/apis/TMFxxx/TMFxxx_v{version}.json`)

#### 5.3.1 Discovery — going from a component to its APIs, and two different upstream repos

The path from a use case to a live OpenAPI schema is: **use case → `links.components` (§5.1) → each component's `component.yaml` → `coreFunction.dependentAPIs[]`/`exposedAPIs[]`, each with a `specification[].url` field pointing straight at a versioned swagger file.** No separate lookup is needed once the component spec is cached — the URL is already sitting inside it (this is the same field the pilot's `create-oda-component` skill reads to download a component's APIs, and the same field visible in TMFC001's own spec, e.g. its `TMF633` dependency resolving to `https://tmf-open-api-table-documents.s3.eu-west-1.amazonaws.com/OpenApiTable/TMF633_Service_Catalog/4.0.0/swagger/TMF633_Service_Catalog_Management_API_v4.0.0_swagger.json`).

That S3-hosted file — the **published, generated** deliverable — is what `tools/fetch_api.py` caches into `knowledge/apis/TMFxxx/TMFxxx_v{version}.json`, unmodified. It requires no authentication. Multiple versions can coexist side by side (`TMF632_v4.0.0.json`, `TMF632_v5.0.0.json`) because, unlike use cases, components genuinely need to track more than one live API generation at once (Gen4/Gen5 coexistence is already how `oda-canvas` models this). Sibling `.meta.json` mirrors the component pattern (`status` here is just the API's own version generation, e.g. `"v4"`, since Open APIs don't carry a separate maturity ladder).

There is a **second, distinct repository** for Open APIs, easy to conflate with the one above but serving a different purpose: `tmforum-rand/OAS_Open_API_And_Data_Model` is the **authoring source** the S3 swagger files are generated *from* — per-API folders (`apis/TMF632_Party/TMF632_Party_v5.0/`) holding validation rules (`.rules.yaml`), generation config, AsciiDoc conformance specs, and — genuinely useful, beyond what the generated swagger alone offers — `documentation/operation-samples/` and `documentation/notification-samples/`: real, ready-made example request/response and event-notification JSON payloads TM Forum's own API authors wrote for conformance testing (e.g. `Party_create_1_request.sample.json`). This is exactly the kind of thing a `generate-test-data-from-usecase` skill wants and would otherwise have to synthesize from the schema alone.

It is also **access-gated differently from everything else in this repo**: it's a *private* GitHub repository requiring TM Forum-rand org membership (confirmed directly — `gh api repos/tmforum-rand/OAS_Open_API_And_Data_Model` returns `"private": true`, and only succeeds with an authenticated, authorized token; browsing it logged into GitHub needs that same org access, which is a different login from the TM Forum website member account §6.1 relies on). This is a **third access tier**, distinct from both "fully public" (§5.2, §5.3's S3 bucket) and "TM Forum member website login" (§6.1) — see §6.2's revised split.

**v1 scope call:** cache the S3 swagger (no auth, always available) as the API spec of record. Treat the sample payloads from `OAS_Open_API_And_Data_Model` as an **optional enrichment**, fetched into `knowledge/apis/TMFxxx/samples/` only when org-level GitHub access is actually available, and never required — a skill generating test data must work from the schema alone when samples aren't present, and get better (real, human-authored examples instead of synthesized ones) when they are.

### 5.4 Indexes (`knowledge/index/*.json`)

Generated, never hand-edited. `build_index.py` walks every artefact's envelope — frontmatter for Markdown files, `*.meta.json` for everything else — so it never needs type-specific parsing to build the top-level catalogs:

- **`use-cases.json`** — flat array, one row per use case: the envelope fields plus the use-case extension fields a skill filters on most (`maturity`, `approval_status`).
- **`components.json`** / **`apis.json`** — same envelope-driven shape, plus a reverse `links.use_cases: [TMFSxxx, ...]` computed here (never in the source artefact — see §5.0) so "what uses this component" is a lookup, not a scan.
- **`usecase-component-matrix.json`** — the bipartite graph, extracted by `extract_usecase_matrix.py` from IG1228 chapter 2 (the same table already hand-extracted with `pdfplumber` during the research phase — see `references/ig1228/`). This is the corpus-level cross-check against each use case's own `links.components`: IG1228 says which components a use case *touches*; the use case's own envelope says which components and *API versions* it specifically calls. They should agree; where they don't, that's a real signal (a use case that's drifted from the inventory, or vice versa) worth surfacing, not silently resolving.

## 6. Refresh process

TM Forum republishes on a rolling ~4–8 week cadence (IG1228's own version history: 31 revisions between Oct 2020 and Jul 2026, no dead time longer than about two months). The refresh process has **three tracks**, because there are three genuinely different access models in play, not two:

| Tier | Requires | Artefacts | Track |
|---|---|---|---|
| Fully public | Nothing | Component specs (GitHub, tagged), Open API swagger (S3) | §6.2, scriptable |
| GitHub org membership | An authenticated, `tmforum-rand`-authorized token | `OAS_Open_API_And_Data_Model` sample payloads (§5.3.1, optional enrichment) | §6.2, scriptable, best-effort |
| TM Forum website member login | A logged-in human, browser session | IG1228, TMFSxxx use cases | §6.1, human-in-the-loop |

### 6.1 Assisted track — IG1228 and TMFSxxx use cases (member-gated)

These cannot be fetched unattended; they require a logged-in TM Forum member session and a manual "Download" click per document (confirmed while building the pilot — the download is a JS-driven modal, not a stable direct URL). The refresh runbook is:

1. A human (with a member seat) checks `https://www.tmforum.org/resources/introductory-guide/how-to-use-oda-using-open-apis-to-realize-use-cases-v31-0-0-ig1228/` for a new version, and downloads the current version's DOCX and PDF to `references/ig1228/`.
2. Diff the new IG1228's use-case list (§1, chapter 1) against `knowledge/index/use-cases.json` to get a changed-or-new list: version bumps, new TMFSxxx identifiers, status transitions (`planned` → `Available`).
3. For each changed/new identifier, download its DOCX via `https://www.tmforum.org/?s=TMFSxxx&post_type=product` → highest version, highest-authority result (Production over Pre-production) — this is the exact procedure already used for the six pilot documents.
4. Run `tools/docx2md.py` on each, updating `knowledge/use-cases/TMFSxxx/`.
5. Re-run `tools/extract_usecase_matrix.py` against the new IG1228 chapter 2.
6. Run `tools/build_index.py`, then `tools/refresh_report.py` to generate a `CHANGELOG.md` entry.

This is a documented, repeatable checklist — not a script — because step 1 and step 3 need a human in the loop. Steps 4–6 are one command each.

### 6.2 Automated track — Components and Open APIs

Component specs (GitHub, tagged releases) and Open API specs (versioned S3 URLs) require no login at all. `tools/fetch_component.py` re-lists the `TMForum-ODA-Ready-for-publication` tag once (§5.2.1) to refresh `component-folder-map.json`, then re-fetches every component; `tools/fetch_api.py` follows the URLs already sitting inside each freshly-fetched component spec. Both compare `sha256` against the cached `.meta.json` and only rewrite files that actually changed. This half of the track can be a fully unattended scheduled job.

The optional sample-payload enrichment (§5.3.1) needs a `tmforum-rand`-authorized GitHub token — still fully scriptable, still no human clicking through a web UI, but it will fail closed (skip, don't error) in any environment that doesn't have org access configured. Treat it as best-effort within this same automated track, never as a blocker: nothing in §5/§8 depends on the samples being present.

Either way, this track can run on a schedule; the assisted track (§6.1) cannot.

### 6.3 Maturity is a first-class refresh signal, not an afterthought

The pilot's single most important finding: **of the six use cases converted, the three approved before November 2025 are GA and TM Forum Approved; the three approved since are Beta or Alpha and Member Evaluated only** — and IG1228's own index marks all six identically as `Available`. A newly-added or newly-changed use case is very likely to be pre-GA. The refresh report must surface maturity/status transitions explicitly (`TMFS0xx: Beta → GA`), and any skill reading `knowledge/use-cases/**` must treat `maturity` and `approval_status` as required filter fields, not optional metadata — this is why `check-usecase-maturity` is the first pilot skill in §8, not an afterthought bolted on later.

## 7. Extensibility (not built now, but the layout must not block it)

- `knowledge/etom/` and `knowledge/sid/` are reserved. When TM Forum's Sparx EA model is exported (a separate, heavier effort — see project history for the proposed XMI → structured YAML → Markdown pipeline), it lands here with the same provenance-in-frontmatter pattern as §5.1.
- An MCP server is a thin read-only wrapper over `knowledge/index/*.json` and the per-document files — nothing in this layout needs to change to add one later; it would expose `get_use_case(id)`, `list_use_cases(maturity=...)`, `get_component(id)`, `trace_usecase_impact(component_id)` as tools reading exactly the files described above.
- Nothing here assumes only one CSP/deployment context; component and API caches are shared, version-addressed data, not tied to any one use case.

## 8. How this gets consumed: pilot skills

Not built as part of this spec, but the layout is validated against them — if a skill can't be written cleanly against §4/§5, the layout is wrong. Candidates, roughly in build order (see `tasks.md` Phase 6):

1. **`check-usecase-maturity`** — given a TMFSxxx id, reads its frontmatter and returns a plain-language maturity/trust verdict. Deliberately the simplest possible skill; exists to prove the frontmatter schema is sufficient on its own, with zero prose-parsing.
2. **`capture-requirements-from-usecase`** — given a TMFSxxx id, reads the Description/Scope/Objective sections and drafts user stories or acceptance criteria, citing the exact component/API IDs from frontmatter rather than inventing integration points.
3. **`generate-test-cases-from-usecase`** — given a TMFSxxx id, reads its sequence-diagram section (and, for the API calls named in each step, the cached OpenAPI schema in `knowledge/apis/`) and drafts BDD-style scenarios — the same shape as `oda-canvas`'s existing `write-bdd-feature` skill, but pointed at real use-case content instead of hand-written scenarios.
4. **`validate-design-against-oda`** — given a proposed component/API design, checks it against the cached specs for components/APIs it claims to extend or depend on, flagging drift.

## 9. Success criteria for the v1 pilot

- [ ] All ~32 TMFSxxx identifiers IG1228 v31.0.0 lists as `Available` exist under `knowledge/use-cases/`, with the 6 already-converted docs re-homed into the new layout.
- [ ] Every component and API named in any pilot use case's References section has either a cached spec under `knowledge/components/` or `knowledge/apis/`, or an explicit `not_yet_specified` meta record.
- [ ] `knowledge/index/*.json` regenerates byte-identical on a second run with no input changes (idempotence, principle 7).
- [ ] `knowledge/index/usecase-component-matrix.json` cross-checked against at least 3 use cases' own frontmatter, with any disagreement logged, not silently dropped.
- [ ] The assisted and automated refresh tracks (§6) are each exercised at least once end-to-end, including a `CHANGELOG.md` entry produced by `refresh_report.py`.
- [ ] At least one pilot skill from §8 runs end-to-end against `knowledge/` and produces a correct, citation-backed output for a use case it wasn't specifically tuned on.

## 10. Open questions (decide during Phase 0, don't block on them here)

- ~~Should `references/` (raw DOCX/PDF) be committed to git at all, or `.gitignore`'d as a local cache with only `knowledge/` tracked?~~ **Decided (0.2): committed.** DOCX files run 0.5–4MB each; at ~32 use cases that's under 100MB, well within git's comfort zone without LFS. The deciding factor wasn't size — it's that `references/` holds member-gated content that isn't independently re-obtainable without a TM Forum login (§6.1). Gitignoring it would mean a fresh clone can regenerate `knowledge/`'s public artefacts (§6.2) but not its use cases, silently defeating principle 3. `.gitignore` at the repo root excludes only actual junk (`__pycache__/`, `.venv/`, OS cruft).
- Do we snapshot `knowledge/components/` and `knowledge/apis/` at the ODA release they were fetched against (a `v1.0.0/` subdirectory), or always overwrite to "latest known good"? Overwrite-in-place (matching principle 2) is the default assumption above; revisit if a skill ever needs to reason about two ODA release trains side by side.
- Where does `CHANGELOG.md` sit if this repo is later merged into a larger monorepo — keep it root-level regardless, since refresh history should survive a restructuring.
