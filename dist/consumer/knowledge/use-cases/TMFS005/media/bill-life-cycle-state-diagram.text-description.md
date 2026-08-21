# bill-life-cycle-state-diagram.png

**Type:** UML state diagram.
**Source context:** `# Description` section, under "Bill Life Cycle",
illustrating the states a bill instance moves through.

States, in order from the initial node: `New` ("Bill is ready to
validate or to sent") transitions to `OnHold` ("Bill will not be in
further processing until open issues connected to the bill are solved")
or directly to `Validated` ("Bill is checked"); `OnHold` transitions to
`Validated`; `Validated` transitions to `Sent` ("Bill is with the channel
defined in the billingAccount").
