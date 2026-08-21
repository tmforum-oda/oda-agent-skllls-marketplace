# fallout-lifecycle-state-diagram.png

**Type:** UML state diagram, with a composite/nested state.
**Source context:** `# Information View` / `## Fallout lifecycle`,
Figure 7 ("Order fallout lifecycle"), defining the lifecycle every
fallout management process instance is assumed to follow.

States, from the initial node: `Created` ("Fallout created and
initialized") transitions via "start order fallout execution" into the
composite state `Processing`, which contains two substates: `Analysing`
("Fallout is analysed to determine resolution options") and `Resolving`
("Automatic resolution ongoing"), linked by "start fallout automatic
resolution".

From `Processing`, two exits: "fallout process **Completed**" leads to
the `Completed` state ("Execution finished. Resolution status might be
resolved or not resolved"); "fallout process **Cacelled**" [sic, kept as
spelled in the source] leads to `Cancelled` ("Execution cancelled").

From `Processing` (specifically from `Analysing`), "manual intervention
needed" leads to `Held` ("Manual intervention required"), which can
return "back to automatic treatment" into `Analysing`, or exit via
"fallout process **Completed**" to `Completed`, or "fallout process
**Cacelled**" to `Cancelled`.

Both `Completed` and `Cancelled` transition via "Final" to the final
node.
