Architecture/block diagram. Appears in the Introduction section as Figure 1-1, "Overview of Partnering Models between B2B2X SupplierRole, Intermediary (EntityRole) and CustomerRole".

It shows the B2B2X stakeholder roles and the main relationships between them as a horizontal chain of boxes connected by double-headed arrows:

- **End user** (stick-figure actor, leftmost) `<-- -->` **Customer** (blue box) via a dashed double-headed arrow.
- **Customer** (blue box) `<-- -->` **Entity** (grey box) via a solid double-headed arrow — labelled in the caption as the "main relationships addressed in this Use Case".
- **Entity** (grey box) `<-- -->` **Suppliers** (stack of yellow boxes, representing multiple Supplier instances) via a solid double-headed arrow.
- **Channel partner (Marketplace, Hyperscaler, Aggregator, ...)** (green box, positioned above and between Customer and Entity) connects to both **Customer** and **Entity** via dashed double-headed arrows, representing an optional intermediary channel.

A legend at the bottom-left explains that the double-headed arrow icon denotes "Main relationships addressed in this Use Case", and a caption at bottom-right reads "B2B2X stakeholders and their relationships". The diagram is explicitly captioned in the body text as a simplification of a generalized B2Bn2Xm model — end customers in practice relate to multiple Entities and Suppliers, and this simplified model can be instantiated multiple times to represent that.
