---
name: process-component-media
description: Given a TMFCxxx component id, processes every image in its knowledge/components/{ID}/media/ folder in turn -- classifies it, renames it descriptively, reverse-engineers structured diagrams (the component architecture overview, eTOM-SID ABE link diagrams, API/Resource/Operation diagrams) into PlantUML .puml files, and writes a text-description.md for everything else -- updating the component's own {ID}.md body to match. Use this to enrich a component's raw extracted images into agent-friendly formats. Unlike other skills here, this one writes to knowledge/, not just reads it.
---

# Process Component Media — Skill Instructions

## What this skill does, and why

A component specification's real diagram content sits in raw images
under `knowledge/components/{ID}/media/imageNN.{png,jpeg}`, referenced
inline in `{ID}.md` (`tools/pdf2md_component.py`'s output — see
`spec/spec-components.md`). Reading an image costs a multimodal call
every time a skill needs to understand it. This skill pays that cost
once per image, converting each into a plain-text form another skill (or
agent) can read cheaply and repeatedly afterward: PlantUML source for
anything with structured entities and relationships, a written
description for anything else.

**This skill modifies files under `knowledge/`** — every other skill in
this repo is read-only against `knowledge/`; this one renames images,
writes new sidecar files, and edits the component's own `.md` body. Treat
that as a deliberate exception, not a precedent for other skills to
follow — the same exception `process-usecase-media` already makes for
use cases.

## Step 1 — Find unprocessed images

```
knowledge/components/{ID}/media/
```

An image still named `imageNN.{png,jpeg}` (the generic pattern
`pdf2md_component.py` extracts with) hasn't been processed yet. An image
with a descriptive name already has been — **skip it**, don't reprocess
or rename an already-processed image. This is what makes the skill safe
to re-run: run it again after a refresh re-converts a component's PDF,
and it only touches genuinely new images.

## Step 2 — Analyze and classify each unprocessed image

Read the image directly (multimodal), and read the surrounding body text
in `{ID}.md` for context — search for the image's current filename
(`media/imageNN.{ext}`) to find where it's referenced, which section
it's in, and what the prose around it says it depicts.

Component specification PDFs use a small, consistent set of diagram
notations — every image across every component processed so far (120
images, 25 components) has landed cleanly in one of the first three
categories below, with zero exceptions:

- **Component architecture diagram** — one per component, in the
  Overview section. A single dark box representing the component itself,
  containing its eTOM Business Activities (dashed-outline rectangles) and
  SID Data Entities (cylinders), with Dependent APIs entering on the left
  (socket/cup connectors) and Exposed APIs leaving on the right (lollipop
  connectors), plus a standard legend explaining the four shapes.
- **eTOM–SID ABE link diagram** — in the SID ABEs section. An
  information/data-model view: SID entities (cylinders) linked to eTOM
  Business Activity boxes by directional arrows, each direction meaning
  something specific per the diagram's own legend (typically "produces"
  one way, "is consumed by" the other).
- **API/Resource/Operation diagram** — in the Exposed APIs, Dependent
  APIs, and Events sections. A tree/list structure: one box per API
  (fields like `id`, `name`, `required`, `resources`) connected via small
  junction nodes to its named resources, each connected to its list of
  operations (`GET`, `POST`, `GET /id`, …) or, for the Events diagram,
  to named event types instead of operations.
- **Other** — anything that isn't one of the three shapes above (a
  screenshot, a UI mockup, a generic block diagram not using the
  architecture notation) — genuinely rare in a component spec PDF, but
  don't force a diagram into one of the three categories above if it
  doesn't actually match.

If a newly-published or not-yet-seen component's PDF shows a diagram that
doesn't fit any of these three shapes, classify it on its own merits
rather than forcing it into the nearest category — treat it the same way
the "Other" bucket already is: describe what it actually is (Step 5).

## Step 3 — Rename descriptively and update every reference

Choose a kebab-case name describing what the image actually shows, not
its position in the document (`agreement-management-architecture`,
`etom-sid-agreement-links`, `exposed-apis-structure`,
`dependent-apis-structure`, `events-structure` — not `diagram-4`). Rename
the file, then find and update **every** `![](media/imageNN.{ext})`
reference to that image in `{ID}.md` — a rename that leaves a body
reference pointing at a now-missing filename is a regression. Verify
afterward: no `media/imageNN` pattern remains anywhere in the body, and
every `media/` reference in the body resolves to a file that actually
exists on disk.

## Step 4 — Structured diagrams: reverse-engineer to PlantUML

Write a `.puml` file with the same base name, sibling to the renamed
image, for each of the three structured categories from Step 2 — this is
a redraw of exactly what the image shows, not a summary or a simplified
approximation:

- **Component architecture diagram** → a PlantUML `component`/`object`
  diagram: one block for the component itself containing its eTOM
  activities and SID entities as nested elements, arrows in from every
  dependent API and out to every exposed API, each arrow labeled with the
  real API id and name from the image (not just "API" generically).
- **eTOM–SID ABE link diagram** → a PlantUML `class`-style diagram:
  entities as `class` blocks (attributes/example values kept as class
  members where the image shows them), labeled relationships as arrows
  carrying the image's own arrow direction and meaning (per its legend —
  don't invent a direction the image doesn't show). The legend typically
  only defines meaning for eTOM-activity↔SID-ABE arrows ("produces" /
  "is consumed by") — it usually does **not** define what an arrow
  directly between two SID entities means (confirmed on `TMFC039`'s own
  diagram, which links three SID entities to each other with six such
  arrows, none covered by its legend). Preserve those arrows' directions
  exactly as drawn without inventing "produces"/"consumed by" semantics
  for them — a plain, unlabeled arrow is the honest redraw when the
  source genuinely doesn't state what it means. Some of these diagrams
  are also dense enough (several near-parallel curved arrows between the
  same few entities) that reading direction correctly from the image at
  normal resolution is genuinely error-prone — zoom into or crop the
  region around the arrowheads before committing to a direction, rather
  than trusting a single full-image read.
- **API/Resource/Operation diagram** → a PlantUML `object` diagram: one
  object per API with its real field values (`id`, `name`, `required`,
  `resources`/`events`), connected to its resources or event names,
  each connected in turn to its actual operations or event types — every
  API, every resource, every operation/event listed, not a representative
  subset. Rendering the operation/event lists as flat `rectangle` blocks
  alongside the `object` blocks reads closest to the source image, but
  PlantUML's diagram-type auto-detection can misfire on the mix (tips
  into a `class`-diagram reading) unless the file starts with an explicit
  `allowmixing` directive — add it whenever a diagram combines `object`
  and `rectangle`/`class` elements together.

**Verify by actually rendering it, not by trusting the transcription by
eye.** If a PlantUML renderer is available, render the `.puml` to a
**scratch/temporary directory outside `media/`** — never render in place
using the diagram's own base name, which collides with the source image
filename and silently overwrites it (`process-usecase-media`'s own
instructions call this out as the one mistake with real, hard-to-notice
consequences — the same risk applies here unchanged). Recovering an
overwritten original means restoring it byte-for-byte from git history
and confirming via checksum before continuing; treat that as a real
failure to avoid, not a routine recovery step. Compare the render against
the source image (every element present, every arrow's direction and
label, every field value) before treating the `.puml` as done — a
`.puml` that merely compiles without error hasn't been verified, only
checked for syntax.

## Step 5 — Everything else: write a text description

Write `{base-name}.text-description.md`, sibling to the renamed image —
one file per image, never a shared file across multiple images in the
same `media/` folder. Ground the description in both the image itself
and the surrounding body text that introduces it: state the image's
type, the section it appears in, and what it actually shows in enough
detail that a reader who trusts the description doesn't need to open the
image. State what the image *is*, not what it *isn't* — e.g. "UI
screenshot of X," not "not one of the standard architecture diagrams."

These files are sidecar annotations, not standalone artefacts — they
don't need the five-field envelope every other file under `knowledge/`
carries, and `tools/validate_envelope.py` already excludes the
`*.text-description.md` suffix for this reason.

## Step 6 — Link the enrichment from the document body

Immediately after each image's `![]()` reference in `{ID}.md`, add a
line linking to its new sibling file as a real markdown link, not a
plain-text mention:

```markdown
![](media/agreement-management-architecture.png)
*([PlantUML source](media/agreement-management-architecture.puml))*
```

```markdown
![](media/some-ui-screenshot.png)
*([text description](media/some-ui-screenshot.text-description.md))*
```

The same `[PlantUML source](...)` link form is used regardless of which
of the three structured-diagram shapes (Step 4) the `.puml` redraws — the
link doesn't need to say which.

## What this skill does NOT do

- Does not process a component's body text, frontmatter, `component.yaml`, or any file outside `media/` — scoped strictly to images and the minimal body edits needed to reference them correctly.
- Does not touch an already-processed image (Step 1) — safe to re-run, not a full reprocessing pass every time.
- Does not treat a `.puml` file as verified just because it rendered without a syntax error — Step 4's visual comparison against the source is required, not optional.
- Does not render verification output into `media/` using the source diagram's own base name — that's the one mistake with real, hard-to-notice consequences (a silently overwritten original), and Step 4 exists specifically to prevent it.
- Does not force an image into one of Step 2's three structured categories if it genuinely doesn't match — the "Other" bucket (Step 5) exists for exactly that case. The three categories cover every image across every component processed so far, but treat that as strong precedent, not a guarantee for a component not yet seen.
