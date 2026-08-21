# fallout-tracking-tool-mockup.png

**Type:** UI wireframe/mockup of an operator dashboard.
**Source context:** `### Sequence diagrams for successful, manual
resolution of the fallout` / `#### Order fallout resolution`, illustrating
the "Fallout Tracking Tool" an operator uses to manually analyse and act
on fallouts, referenced right after the manual-resolution sequence
diagram's note about "an example of such a dashboard."

A search panel with fields for Order, Error type, Error code, Error
description, Assigned user, Priority (dropdown, "High" selected),
Status (dropdown), Order date, and Fallout date, plus a "Search" button.
Below, a sortable results table with columns Order/Order item, Error
type, Error code, Error description, Assigned user, Priority, Status,
Order date, Fallout date, and per-row checkboxes plus a "Select all"
checkbox. Three example rows: `RO123123-5` (Resource Configuration
Failure, code 105201, "HSS subscriber already exists", assigned to John
Smith, High priority, status Raised); `RO123120-2` (Resource Reservation
Failure, code 111097, "SIM card not available", assigned to Peter Green,
Medium priority, status Resolved); `RO123133-1` (Resource Configuration
Failure, code 105201, "HSS subscriber already exists", assigned to Peter
Meyer, Low priority, status In Progress Manual — this row's checkbox is
selected). Action buttons at the bottom: "Retry", "Continue", "Cancel"
(left), and "Back to automatic" (right).
