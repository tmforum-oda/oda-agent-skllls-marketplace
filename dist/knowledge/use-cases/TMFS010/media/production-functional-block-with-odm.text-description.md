# production-functional-block-with-odm.png

**Type:** ODA functional-block architecture diagram.
**Source context:** Figure 2 in the document's own "List of Figures"
("Production functional Block with ODM") — present in `media/` but not
actually inserted into the document body by the original DOCX-to-Markdown
conversion (the body jumps from Figure 1 straight to Figure 3). Restored
as Figure 2 immediately after Figure 1, in `# Introduction` /
`## Context or Background`, matching the List of Figures' stated intent.

Layout, top to bottom, with `Engagement Management` (purple) and
`Intelligence Management` (grey) as full-height side columns, separated
from the center stack by "Decoupling and Integration" bars:

- `Party Management` (red, top band).
- `Core Commerce Management` (dark grey band), listing: Product Order
  Management, Product Catalog, Product Management, Billing Account
  Management, Rating & Charging, Contract Management, Business
  Assurance, Sales Management.
- `Production` (dark blue band), showing two `ODM` (Operational Domain
  Management) boxes flanking a central `E2E SM Domain` box. Each of the
  three boxes contains a `CFS` node in a dashed "Service" sub-region;
  the two `ODM` boxes additionally contain an `RFS` node in a dashed
  "Resource" sub-region below. Lines connect: each `ODM`'s `CFS` up
  through the "Decoupling and Integration" bar to a red dot (representing
  the API/event exposure point above Production), and each `ODM`'s `CFS`
  diagonally across to the `E2E SM Domain`'s central `CFS` (showing the
  E2E SM Domain composing the two ODMs' CFS-level services into one).
  Each `ODM`'s `RFS` connects straight up into its own `CFS`.
