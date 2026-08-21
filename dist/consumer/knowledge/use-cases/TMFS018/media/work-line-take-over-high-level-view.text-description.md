# image35.png

**Type:** Broken diagram render (source-document defect), not a usable
sequence diagram.
**Source context:** `## Operational Stage: Work Line Take Over` / `###
High Level View`.

The embedded image is not a rendered sequence diagram: it is a
screenshot of a PlantUML tool window showing a **render failure**. The
visible content is green monospace text on a black background —
PlantUML's own startup banner ("PlantUML 1.2024.7", a warning that the
version is 641 days old and should be upgraded) — followed by a
fragment of the PlantUML *source* that was being rendered:

```
@startuml
title Work Line Take Over - High Level View
skinparam ParticipantFontColor automatic
autonumber
box Receiving Wholebuyer
participant "BuyerGW" as BGW1 #Grey
end box Donating Wholebuyer
```

Below that fragment, in red text, PlantUML reports the error
**"Cannot create group"** — caused by the malformed `end box Donating
Wholebuyer` line (a second box's label was appended to the `end box`
keyword instead of opening a new `box` block), which aborted the
render before the diagram body could be drawn.

This appears to be an authoring mistake in the source document: an
error screenshot was captured and pasted in place of the intended
"Work Line Take Over - High Level View" sequence diagram. Only the
title and the first two participant declarations of the intended
diagram are recoverable from the visible source fragment; the rest of
the diagram (the Donating Wholebuyer box, the Wholeseller side, and
all message flow) is not present in the image and cannot be
reconstructed. The equivalent, fully-rendered diagram for the
"Gaining Provider Led Switch Order" variant of this same operational
stage is available immediately below this one — see
`work-line-take-over-gaining-provider-switch-sequence.puml`
(`image36.png`).
