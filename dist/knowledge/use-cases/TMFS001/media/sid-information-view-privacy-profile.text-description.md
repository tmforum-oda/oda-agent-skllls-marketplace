# sid-information-view-privacy-profile.png

**Type:** Information/data model diagram (simplified SID view), not a
sequence diagram.
**Source context:** `# Information View` section — the privacy-related
counterpart to `sid-information-view-party-account.png`, following the
sentence "Based on the Party Privacy Profile Type defined for the Portal
User Party Role specification, at the end of the use case the
information related to privacy management will be:".

An entity-relationship diagram, again using "John Smith" as the worked
example, spanning three owning components:

- **TMFC035 Party Roles & Permissions Mgt**: a `PartyRoleSpecification`
  ("Portal User") *describes* the `PartyRole` ("John Smith Portal User
  Role"), which is *applicable for* a `PartyPrivacyProfileType`
  ("Portal User Profile Type").
- **TMFC028 Party Mgt**: the `Party/Individual` ("John Smith") *has* the
  `PartyRole` and *defines* a `ContactMethod` (email address
  `john.smith@emailprovider.com`).
- **TMFC022 Party Privacy Management**: the `PartyPrivacyProfileType`
  *describes* two `PartyPrivacyProfileTypeCharacteristic` entries
  ("emailAddressforMarketing purpose," "emailAddressforInternal
  purpose"), each *enumerated by* `PartyPrivacyProfileTypeCharValue`
  options (e.g. authorized/unauthorized, with default and validation
  period). These *instantiate* actual
  `PartyPrivacyProfileCharValue` records (value: authorized, with
  start/end dates) tied to "John Smith Privacy Profile" — a
  `PartyPrivacyProfile` that is *agreed by* the Party, *approved by* a
  `PartyPrivacyProfileApproval` record (date, hour, channel: "Lambda
  Portal"), and *described by* the two char-value records.

Everything inside the outer red box belongs to TMFC022 Party Privacy
Management; the two smaller boxes above it belong to TMFC035 and
TMFC028 respectively.
