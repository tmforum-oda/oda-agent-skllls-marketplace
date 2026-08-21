# fallout-path-with-resolution-state-diagram.png

**Type:** Order-item state-transition timeline diagram (parallel tracks
joined by dependency arrows, plus a fallout-process boundary event and a
side "Fallout management process" track), not a UML sequence diagram or
an entity-relationship model.
**Source context:** `## HSS activation fallout scenario`, Figure 4
("Fallout path with resolution"), showing what happens to order-item
states when the HSS subscriber profile order item raises a fallout that
is subsequently resolved.

Same overall shape as the happy-path diagram (Figure 3): a `Mobile Line
order item` track (Acknowledged → inProgress) fans out into `Logical
SIM order item` and `Number order item` tracks (each completing
normally, Acknowledged → inProgress → Completed) and an `HSS subscriber
profile order item` track inside an "Order management process" box.

On the HSS track, after reaching inProgress a boundary escalation event
("N") fires labeled "fallout raised" (red), transitioning the HSS order
item to a red **Held** state rather than continuing to Completed. This
spawns a parallel "Fallout management process" box (Initialized →
Completed), whose completion feeds back (labeled "fallout resolved")
into the HSS track, which then resumes: inProgress → Completed. All
three resource tracks converge back into a Completed state for the
`Mobile Line order item`. Throughout, dashed arrows fan out left to a
vertical "Order ad order item state change events for consumption bby
other processes" bar at each state transition, indicating that every
transition is published as an event. Legend: single ring = Acknowledged
(order) / Initialized (fallout); double ring = inProgress; red double
ring = Held; bold ring = Completed (order) / Resolved (fallout).
