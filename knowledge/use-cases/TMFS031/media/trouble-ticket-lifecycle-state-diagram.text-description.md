UML state machine diagram, titled "Lifecycle view". Appears in the "Information View" section, illustrating the lifecycle states a trouble/incident ticket moves through from creation to closure.

States and transitions, starting from the UML initial node (filled black circle):

- Initial node → **Acknowledged** (labelled "Reprted problem is assigned" [sic]).
- **Acknowledged** → **New**.
- **New** → **In Progress** (labelled "Begin Investigation").
- **New** → **Cancelled** (labelled "Reported ticket cancelled").
- **In Progress** → **On Hold** (labelled "Put on Hold").
- **On Hold** → **In Progress** (labelled "Work resumed").
- **In Progress** → **Cancelled** (labelled "Problem ticket cancelled").
- **On Hold** → **Cancelled** (labelled "Problem ticket cancelled").
- **In Progress** → **Resolved** (labelled "Ticket Resolved").
- **Resolved** → **Closed** (labelled "Closed").
- **Cancelled** → **Closed** (labelled "Closed").
- **Closed** → final node (filled black circle inside a ring), labelled "Final".

In summary: a ticket is Acknowledged then becomes New; from New it either begins investigation (In Progress) or is cancelled; while In Progress it can be put On Hold and later resumed, cancelled from either In Progress or On Hold, or resolved; both Resolved and Cancelled tickets are ultimately moved to Closed, which is the terminal state.
