# happy-path-state-diagram.png

**Type:** Order-item state-transition timeline diagram (parallel tracks
joined by dependency arrows), not a UML sequence diagram or an
entity-relationship model.
**Source context:** `## HSS activation fallout scenario`, Figure 3
("Happy path"), illustrating the normal (non-fallout) state progression
of the mobile line order and its dependent resource order items, before
introducing the fallout scenario in Figures 4-5.

A start event leads into a single track for the `Mobile Line order item`
(shown collapsed across its product level, green, and CFS level,
orange): Acknowledged → inProgress. From there the flow fans out into
three parallel resource-level tracks (olive): `Logical SIM order item`,
`Number order item`, and `HSS subscriber profile order item`, each
running Acknowledged → inProgress → Completed. Dependency arrows link
the three tracks' Completed states in sequence — Logical SIM's Completed
feeds into Number's Completed, and Number's Completed feeds into HSS
subscriber profile's Completed — showing that the HSS subscriber profile
order item only completes once both the Logical SIM and Number order
items have completed. All three tracks converge back into a single
Completed state for the `Mobile Line order item`, which leads to the end
event. A legend distinguishes the three states by circle style:
Acknowledged (single ring), inProgress (double ring), Completed (bold
ring).
