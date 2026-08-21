# decomposition-fallout-path-state-diagram.png

**Type:** Order-item state-transition timeline diagram (parallel tracks
joined by dependency arrows, plus a fallout-process boundary event and a
side "Fallout management process" track), not a UML sequence diagram or
an entity-relationship model.
**Source context:** `## Service order decomposition fallout scenario`,
Figure 6 ("Fallout path with resolution"), showing the order-item state
progression when the service-order-to-resource-order decomposition
itself fails, before any resource order items exist.

Unlike Figure 4 (where the fallout occurs on the `HSS subscriber
profile` resource-level track after the mobile line has already fanned
out), here the fallout occurs directly on the `Mobile Line order item`
track itself, inside the "Order management process" box, before the
fan-out: Acknowledged → inProgress → **Held** (red double ring, "fallout
raised") → back to inProgress ("fallout resolved") → the flow then fans
out into three resource-level tracks (`Logical SIM order item`, `Number
order item`, `HSS subscriber profile order item`), each running
Acknowledged → inProgress → Completed with the same sequential
dependency pattern as the happy path (Logical SIM's Completed feeds
Number's Completed, which feeds HSS subscriber profile's Completed). A
parallel "Fallout management process" box (Initialized → Completed)
handles the fallout and feeds the "fallout resolved" transition back
into the main track. As in Figure 4, dashed arrows fan out to an "Order
ad order item state change events for consumption bby other processes"
bar at each transition on the main track.
