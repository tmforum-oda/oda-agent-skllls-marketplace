# order-state-dependencies-diagram.png

**Type:** Order-state timeline/dependency diagram (four parallel state
tracks joined by precondition arrows), not a UML sequence or
entity-relationship diagram.
**Source context:** `## Order lifecycle` section, Figure 1, illustrating
how the product order, product-related resource order, service order,
and service-related resource order progress through their lifecycles in
this use case's steps.

Four horizontal tracks, each a left-to-right chain of states joined by
black solid arrows (that order's own state transitions):

- **Product order**: Acknowledged (starting point, unlabeled box) →
  In Progress → Completed (dotted border, out of this use case's scope).
- **Product related resource order**: Acknowledged (orange) →
  In Progress (orange) → Completed (orange).
- **Service order**: Acknowledged (magenta) → In Progress (magenta) →
  Completed (green).
- **Service related resource order**: Acknowledged (magenta) →
  In Progress (green) → Completed (green).

Blue arrows cross between tracks marking preconditions (a state change
in one order that requires or triggers a state in another): Product
order's "In Progress" triggers the Product related resource order's
"Acknowledged"; the Product related resource order's "Acknowledged"
triggers the Service order's "Acknowledged"; the Service order's
"In Progress" triggers the Service related resource order's
"Acknowledged"; the Service related resource order's "Completed"
triggers the Service order's "Completed"; the Product related resource
order's "Completed" and the Service order's "Completed" both trigger the
Product order's "Completed".
