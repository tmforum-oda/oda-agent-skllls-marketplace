---
name: process-usecase-media
description: Given a TMFSxxx use-case id, processes every image in its knowledge/use-cases/{ID}/media/ folder in turn -- classifies it, renames it descriptively, reverse-engineers UML sequence diagrams and information/data-model diagrams into PlantUML .puml files, and writes a text-description.md for everything else -- updating the use case's own document body to match. Use this to enrich a use case's raw extracted images into agent-friendly formats. Unlike other skills here, this one writes to knowledge/, not just reads it.
---

# Process Use-Case Media — Skill Instructions

## What this skill does, and why

A use case's real diagram content sits in raw images under
`knowledge/use-cases/{ID}/media/imageNN.{png,jpeg}`, referenced inline in
the document body. Reading an image costs a multimodal call every time a
skill needs to understand it. This skill pays that cost once per image,
converting each into a plain-text form another skill (or agent) can read
cheaply and repeatedly afterward: PlantUML source for anything with
structured entities and relationships (a sequence diagram, an
information/data model view), a written description for anything else.

**This skill modifies files under `knowledge/`** — every other skill in
this repo is read-only against `knowledge/`; this one renames images,
writes new sidecar files, and edits the use case's own `.md` body. Treat
that as a deliberate exception, not a precedent for other skills to
follow.

## Step 1 — Find unprocessed images

```
knowledge/use-cases/{ID}/media/
```

An image still named `imageNN.{png,jpeg}` (the generic pattern
`docx2md.py` extracts with) hasn't been processed yet. An image with a
descriptive name already has been — **skip it**, don't reprocess or
rename an already-processed image. This is what makes the skill safe to
re-run: run it again after a refresh adds new images to an
already-partly-processed use case, and it only touches the new ones.

## Step 2 — Analyze and classify each unprocessed image

Read the image directly (multimodal), and read the surrounding body text
in `{ID}.md` for context — search for the image's current filename
(`media/imageNN.{ext}`) to find where it's referenced, which section
it's in, and what the prose around it says it depicts. That context is
often decisive for classification and always useful for naming.

Classify as one of:
- **UML sequence diagram** — actors/participants with lifelines,
  numbered or ordered messages between them, activation bars.
- **Information/data model view** — labeled entities (classes, objects,
  or SID/catalog-style boxes) connected by labeled relationships, with or
  without attributes/example values — an entity-relationship diagram in
  substance, whatever notation the source actually uses.
- **Other** — architecture/block diagrams, UI wireframes/mockups, or
  anything else that isn't one of the two structured types above.

## Step 3 — Rename descriptively and update every reference

Choose a kebab-case name describing what the image actually shows, not
its position in the document (`account-creation-approach-a-sequence`,
not `diagram-4`). Rename the file, then find and update **every**
`![](media/imageNN.{ext})` reference to that image in `{ID}.md` — a
rename that leaves a body reference pointing at a now-missing filename
is a regression. Verify afterward: no `media/imageNN` pattern remains
anywhere in the body, and every `media/` reference in the body resolves
to a file that actually exists on disk.

## Step 4 — Sequence diagrams and information/data model views: reverse-engineer to PlantUML

Write a `.puml` file with the same base name, sibling to the renamed
image — a `sequenceDiagram`-style `.puml` for a sequence diagram, a
`class`-style `.puml` for an information/data model view (entities as
`class` blocks, grouped into `package`s where the source groups them,
e.g. by owning ODA component; attributes and concrete example values
kept as class members; labeled relationships as arrows carrying the
source diagram's own relationship label — `has`, `defines`, `describes`,
`instantiates`, whatever the image actually says). Either way, this is a
redraw of exactly what the image shows — every participant, every
message in order, every entity, every labeled relationship — not a
summary or a simplified approximation.

**Verify by actually rendering it, not by trusting the transcription by
eye.** If a PlantUML renderer is available, render the `.puml` to a
**scratch/temporary directory outside `media/`** — never render in place
using the diagram's own base name, which collides with the source image
filename and silently overwrites it. Recovering an overwritten original
means restoring it byte-for-byte from git history and confirming via
checksum before continuing; treat that as a real failure to avoid, not a
routine recovery step. Compare the render against the source image
(participants/entities present, message order or relationship labels,
grouping structure) before treating the `.puml` as done — a `.puml` that
merely compiles without error hasn't been verified, only checked for
syntax.

## Step 5 — Everything else: write a text description

Write `{base-name}.text-description.md`, sibling to the renamed image —
one file per image, never a shared file across multiple images in the
same `media/` folder, since a folder routinely holds several non-diagram
images and a shared filename would silently overwrite one description
with the next. Ground the description in both the image itself and the
surrounding body text that introduces it: state the image's type, the
section it appears in, and what it actually shows in enough detail that
a reader who trusts the description doesn't need to open the image —
call out labeled entities, relationships, and any real example data the
diagram uses, not just a one-line summary. State what the image *is*,
not what it *isn't* — "UI wireframe/mockup," not "UI wireframe/mockup,
not a UML diagram."

These files are sidecar annotations, not standalone artefacts — they
don't need the five-field envelope every other file under `knowledge/`
carries, and `tools/validate_envelope.py` already excludes the
`*.text-description.md` suffix for this reason.

## Step 6 — Link the enrichment from the document body

Immediately after each image's `![]()` reference in `{ID}.md`, add a
line linking to its new sibling file as a real markdown link, not a
plain-text mention:

```markdown
![](media/account-creation-approach-a-sequence.png)
*([PlantUML source](media/account-creation-approach-a-sequence.puml))*
```

```markdown
![](media/account-creation-ui-mockup.png)
*([text description](media/account-creation-ui-mockup.text-description.md))*
```

The same `[PlantUML source](...)` link form is used whether the `.puml`
is a sequence diagram or a class diagram — the link doesn't need to say
which.

For an image inside a table cell, use `<br>` before the link the same
way the source document already uses `<br>` before the image itself,
keeping both on one logical table-cell line.

## What this skill does NOT do

- Does not process a use case's body text, frontmatter, or any file outside `media/` — scoped strictly to images and the minimal body edits needed to reference them correctly.
- Does not touch an already-processed image (Step 1) — safe to re-run, not a full reprocessing pass every time.
- Does not treat a `.puml` file as verified just because it rendered without a syntax error — Step 4's visual comparison against the source is required, not optional.
- Does not render verification output into `media/` using the source diagram's own base name — that's the one mistake with real, hard-to-notice consequences (a silently overwritten original), and Step 4 exists specifically to prevent it.
- Does not describe an image's type by what it isn't — Step 5's descriptions and this skill's own classifications (Step 2) state what something is.
