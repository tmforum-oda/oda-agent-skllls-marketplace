UML state machine diagram, titled "Service Specification Lifecycle view". Appears in the Information View section immediately after the Service Catalog view diagram, illustrating the lifecycle states a ServiceSpec moves through. The body text notes this view is "informative and not normative."

States and transitions, starting from the UML initial node (filled black circle):

- Initial node → **In Design** (labelled "Initial").
- **In Design** → **Designed** (labelled "ServiceSpec approved").
- **In Design** → **Rejected** (labelled "ServiceSpec design abandoned").
- **Designed** → **Rejected** (labelled "ServiceSpec design abandoned").
- **Designed** → **Active** (labelled "ServiceSpec passes test, and it is ready in production").
- **Active** → **In Design** (labelled "ServiceSpec test failed, redesign needed") — a redesign loop back from Active.
- **Active** → **Unavailable** (labelled "Associated instances remain, but the ServiceSpec is scheduled for retirement").
- **Active** → **Retired** (labelled "No associated instance") — a direct path when Active has no associated instances.
- **Unavailable** → **Retired** (labelled "No associated instance").
- **Rejected** → final node (labelled "Final").
- **Retired** → final node (labelled "Final").

In summary: a ServiceSpec starts in Design, and either gets rejected/abandoned or is approved into Designed; from Designed it is either abandoned (Rejected) or passes testing into Active; an Active spec that fails testing loops back to In Design for rework; an Active spec with no more instances retires directly, while one still holding instances first becomes Unavailable (blocking new instance creation) before retiring once its last instance is removed. Both Rejected and Retired are terminal states.
