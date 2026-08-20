# oda-functional-architecture-overview.png

**Type:** ODA functional-block architecture diagram.
**Source context:** `## Objective of the use case` lead-in section (just above
the "Objective" heading), illustrating the general ODA functional layering
that the fiber-access example draws on.

Layout, top to bottom, with `Engagement Management` (purple) and
`Intelligence Management` (grey) as full-height side columns, separated
from the center stack by "Decoupling and Integration" bars:

- `Party Management` (red, top band).
- `Core Commerce Management` (dark grey band).
- `Production` (dark blue band), containing four side-by-side factories,
  each a stack of `Service Catalog` / `Service Order Management` /
  `Service Inventory` boxes (the `Supply Chain Factory` uses `Supply Chain
  Catalog` / `Supply Chain Orchestration` / `Supply Chain Inventory`
  instead): `Access Factory`, `Network Service Factory`, `Soft Service
  Factory`, `Supply Chain Factory`.
