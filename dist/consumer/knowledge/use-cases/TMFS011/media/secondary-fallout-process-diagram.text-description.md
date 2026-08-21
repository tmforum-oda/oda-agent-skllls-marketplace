# secondary-fallout-process-diagram.png

**Type:** BPMN-style process flow diagram (start/end events, tasks, and
boundary escalation events), not a UML sequence diagram or an
entity-relationship model.
**Source context:** `# Description` / `## Overview`, Figure 2
("(Secondary) fallout process"), illustrating a nested fallout — a
fallout process that itself raises a further fallout.

Flow: a start event leads into an `Activity` task, which leads to an end
event on the happy path. The `Activity` task carries a boundary
escalation event ("N") that branches to a `Primary fallout process`
task, which itself carries a second boundary escalation event ("N")
that branches further to a `Secondary fallout process` task —
representing the primary fallout process running into its own issue and
raising a nested, secondary fallout.
