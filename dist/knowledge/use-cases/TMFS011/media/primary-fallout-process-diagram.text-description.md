# primary-fallout-process-diagram.png

**Type:** BPMN-style process flow diagram (start/end events, a task, and
a boundary escalation event), not a UML sequence diagram or an
entity-relationship model.
**Source context:** `# Description` / `## Overview`, Figure 1
("(Primary) fallout process"), illustrating how a fallout process is
triggered directly by the activity that experiences the exception.

Flow: a start event leads into an `Activity` task, which leads to an end
event on the happy path. The `Activity` task carries a boundary
escalation event (the "N" circle) that, when triggered, branches off to
a separate `Fallout process` task — representing the "main" activity's
own component raising a fallout process itself.
