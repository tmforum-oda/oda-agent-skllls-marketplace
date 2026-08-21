# fallout-path-without-resolution-state-diagram.png

**Type:** Order-item state-transition timeline diagram (parallel tracks
joined by dependency arrows, plus a fallout-process boundary event, a
side "Fallout management process" track, and a rollback process), not a
UML sequence diagram or an entity-relationship model.
**Source context:** `## HSS activation fallout scenario`, Figure 5
("Fallout path without resolution"), showing what happens to order-item
states when the HSS subscriber profile fallout cannot be resolved.

Same shape as Figure 4 up through the fallout: `Mobile Line order item`
fans out into `Logical SIM order item` and `Number order item` tracks
that complete normally, and an `HSS subscriber profile order item`
track that reaches inProgress, raises a fallout ("N" boundary event),
and transitions to **Held** (red double ring). The parallel "Fallout
management process" box runs Initialized → **Not Resolved** (red single
ring) instead of reaching a resolved/completed state, and feeds back
into the HSS track. Because the fallout could not be resolved, the HSS
order item transitions from Held directly to **Cancelled** (red
crossed-out circle) rather than resuming to Completed. The cancellation
triggers a separate "Rollback process" box (bottom right) covering the
`Logical SIM resource` and `Number resource` — the two resources already
configured by the completed Logical SIM and Number order items that now
need to be rolled back since the overall resource order is cancelled.
Legend adds two new states beyond Figure 4's: **Held** (red double
ring), **Not Resolved** (red single ring), and **Cancelled** (red circle
with an X).
