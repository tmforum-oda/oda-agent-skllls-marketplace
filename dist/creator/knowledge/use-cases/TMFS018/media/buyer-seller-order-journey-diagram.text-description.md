# buyer-seller-order-journey-diagram.png

**Type:** Two-lane journey/swimlane illustration connecting Buyer steps
to Seller processes via labeled bidirectional data-flow arrows, not a
UML sequence diagram or entity-relationship model.
**Source context:** `# Sequence diagrams` / `## Operational Stage:
Product Ordering Journey`, Figure 3 ("Buyer/Seller - Journey (order new
product)"), giving the high-level shape of the ordering journey before
the detailed sequence diagrams that follow.

Top teal lane, `Buyer`, six sequential steps (curved arrows between
them): `Input Address Information` → `Input Site Information` → `Input
Product Request` → `Input Installation Date` → `Submit Order` → `Order
Provisioning`. Bottom blue lane, `Seller`, five processes: `Address
Validation`, `Site Validation`, `Product Offering Qualification`,
`Appointment`, `Product Order Management`. Vertical double-headed
arrows connect each Buyer step down to its corresponding Seller process
and back, labeled with the data exchanged: `Customer Address` down /
`Validation ID` up (Address Validation); `Site Information` down /
`Site ID` up (Site Validation); `Product Request` down / `Product ID`
up (Product Offering Qualification); `Information Date` down / `Date
Confirmation` up (Appointment); `Product Order` down / `Order Status`
up, then (after an ellipsis marking omitted intermediate steps) `Order
Status` down / `Order Provisioned` up (Product Order Management).
