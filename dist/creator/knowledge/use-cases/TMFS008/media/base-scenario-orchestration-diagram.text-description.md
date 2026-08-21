# base-scenario-orchestration-diagram.png

**Type:** Cross-layer orchestration flowchart (Start/End nodes, sequencing
arrows, and bidirectional "interaction" arrows between layers), not a UML
sequence diagram (no lifelines/messages) and not an entity-relationship
model.
**Source context:** `### Order structure` section, Figure 6, showing how
the base-scenario order items orchestrate across the product, service,
and resource layers, color-coded green/orange/olive per layer.

Flow: `Start` → **product layer** (green) `SIM Card order item`, then in
parallel `Mobile Line order item`, `Recurring Package order item`,
`Voice Mail order item`, `Extra Data Package order item` → `End`.

Each product-layer box has a bidirectional double-headed arrow (labeled
in a legend as "Interaction between order management components
(including supply chain management) consisting in TMF Open API calls")
down to its **resource/service layer** counterpart:

- `SIM Card order item` (product) ↕ `SIM card order item` (resource,
  olive box, standalone).
- The `Mobile Line`/`Recurring Package`/`Voice Mail`/`Extra Data Package`
  product-layer items ↕ the whole **service layer** (orange box)
  containing `Mobile Line order item`, which fans out (orange
  orchestration arrows) to `Voice Mail order item`, `Recurring Package
  CFS order item`, and `Extra Data Package CFS order item`.
- Within the service layer box, `Mobile Line order item` ↕ a
  resource-layer box containing `Logical SIM order item` and `Number
  order item`, both feeding into `HSS subscriber profile order item`.
  `Recurring Package CFS order item` ↕ its own `PCRF profile order item`
  resource box; `Extra Data Package CFS order item` ↕ a separate `PCRF
  profile order item` resource box; `Voice Mail order item` ↕ `VMS
  profile order item` resource box.
