# extended-scenario-orchestration-diagram.png

**Type:** Cross-layer orchestration flowchart (Start/End nodes,
sequencing arrows, and bidirectional "interaction" arrows between
layers), not a UML sequence diagram and not an entity-relationship model.
**Source context:** `### Order structure` section, Figure 8, the
extended-scenario counterpart to Figure 6 — same layered pattern with
`*eSIM` in place of the SIM card as the tangible-delivery item.

Flow: `Start` → **product layer** (green) `*eSIM order item`, then in
parallel `Mobile Line order item`, `Recurring Package order item`,
`Voice Mail order item`, `Extra Data Package order item` → `End`.

Each product-layer item has a bidirectional double-headed arrow (per the
legend, "Interaction between order management components (including
supply chain management) consisting in TMF Open API calls") down to its
counterpart layer:

- `*eSIM order item` (product) ↕ `*eSIM order item` (service layer,
  orange) ↕ `*eSIM profile order item` (resource layer, olive,
  standalone).
- The service layer (orange box) also contains `Mobile Line order item`,
  which fans out (orange orchestration arrows, inside a dotted
  sub-region) to `Voice Mail order item`, `Recurring Package CFS order
  item`, and `Extra Data Package CFS order item`.
- `Mobile Line order item` (service) ↕ a resource-layer box containing
  `Logical SIM order item`, `Number order item`, `*PCF profile order
  item`, and `*OCS profile order item`, all feeding into `*UDM/UDR
  subscriber profile order item`.
- `Recurring Package CFS order item` ↕ its own `*PCF profile order item`
  resource box; `Extra Data Package CFS order item` ↕ a separate `*PCF
  profile order item` resource box; `Voice Mail order item` ↕ `VMS
  profile order item` resource box.
