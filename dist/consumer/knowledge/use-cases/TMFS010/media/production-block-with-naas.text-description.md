# production-block-with-naas.png

**Type:** ODA functional-block architecture diagram.
**Source context:** `## Internet Product with Fiber using NaaS`, right
column of the two-column comparison table for Figure 3 ("Comparison of
Production functional block without and with NaaS"), captioned "ODMs
view with NaaS and E2E Service Management" — the revised, NaaS-enabled
landscape.

Same layered `Engagement Management` / `Party Management` / `Core
Commerce Management` / `Production` / `Intelligence Management`
structure as the "without NaaS" counterpart, but with two additions: a
`NaaS API Component Suite` bar inserted into the "Decoupling and
Integration" layer directly above `Production`, and a `Centralised
Service Catalog*` cylinder inside `Production` (footnoted: "* A
Centralised service catalog OR a Federated per domain catalog, both
patterns are supported by NaaS").

Inside `Production`, the same four ODM domains as before — `Fibre
Domain` and `Copper Domain` (under "Fixed Service Access"), `Network
Service Domain` (under "Fixed Connectivity"), `Soft Service Domain`
(under "TV Channels") — plus a fifth domain, `Soft Service Domain`
(under "E2E Connectivity Service (Internet + Access)", outlined in blue
to distinguish it as the new E2E Service Management domain), each still
a stack of `Service Catalog` / `Service Orchestration` / `Service
Inventory` boxes. The E2E Connectivity Service domain represents the
new composite-service layer that abstracts and orchestrates across the
other four ODMs.
