# sid-information-view-party-account.png

**Type:** Information/data model diagram (simplified SID view), not a
sequence diagram.
**Source context:** `# Information View` section — "Resulting
Information View (SID simplified view) and link with ODA Components,"
shown as the state after the use case's create-account flow completes.

An entity-relationship diagram grouped into four labeled boxes, one per
owning ODA component, with real example data for "John Smith":

- **TMFC028 Party Mgt**: `Party/Individual` (John Smith) *defines* a
  `Contact Method` (email address `john.smith@emailprovider.com`).
- **TMFC023 Party Interaction Mgt**: `Communication Interaction`
  ("John Smith'portal interaction 2023/06/15") *contains* a
  `Communication Interaction Item` (subject: "create John Smith's
  account"); the interaction *is initiated by* the Party.
- **TMFC020 Digital Identity Mgt**: `Digital Identity` (login:
  `login123`, password masked), which *identifies* the Party.
- **TMFC035 Party Roles & Permissions Mgt**: the Party *has* a
  `PartyRole` ("John Smith's portal user role," valid from 2023/06/15),
  described by a `PartyRole Spec` ("portal user"). The PartyRole *has
  permission* to two `Permission` entries ("initiate customer order,"
  "contact call center X"), each *described by* a matching
  `Permission Spec`. The PartyRole "is a result of" the Communication
  Interaction Item.

A legend at the bottom maps each box's outline/fill color to its entity
type (Party, Contact Method, PartyRole Spec, PartyRole, Communication
Interaction, Digital Identity, Permission Spec, Permission).
