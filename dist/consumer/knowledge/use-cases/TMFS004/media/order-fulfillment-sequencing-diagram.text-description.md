# order-fulfillment-sequencing-diagram.png

**Type:** Orchestration/fork-join flow diagram (not a UML sequence diagram
— no actors or messages — and not an entity-relationship model).
**Source context:** `## Order delivery view`, directly under the caption
"Orchestration of orders:", illustrating the parallel-then-serial
dependency between the shipping and service orders spawned by the
example order.

Two parallel branches feed into a fork/join gateway (diamond with a
cross): `ShippingOrder #26` (Supply Chain domain, containing `Shipping
CFS`, linked to stock keeping unit `SKU 3`) and `ServiceOrder #51` (Access
domain, containing `Landline access`). After the join, the flow proceeds
serially to `ServiceOrder #52` (Network domain, `Landline connectivity`)
and then `ServiceOrder #53` (Soft Service domain, `TV Channels`).
