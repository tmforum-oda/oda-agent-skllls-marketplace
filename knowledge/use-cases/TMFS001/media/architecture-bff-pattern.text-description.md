# architecture-bff-pattern.jpeg

**Type:** Architecture/block diagram, not a sequence diagram.
**Source context:** `## Relationship to BFF pattern` (under `# Appendix`)
— illustrates the backend-for-frontend concept referenced throughout
the use case's sequence diagrams (the "EngagementManagement BFF"
participant in `account-creation-approach-a-sequence.puml` and the
step 1-2/2-3/4-5 diagrams).

A three-layer diagram:

- **Top:** a generic person icon, representing the end user/customer
  device.
- **Systems of Engagement** (purple band): three example frontend
  clients — a Vue app, an IPTV app, and an iOS app — each with an arrow
  down to its own dedicated **BFF** (backend-for-frontend) box.
- **System of Records** (below): three **APIs** boxes (red, light grey,
  dark blue — representing distinct backend API domains). Green arrows
  fan out from all three BFFs to all three APIs boxes, showing that any
  BFF can call any of the backend API domains as needed — the BFFs
  aggregate/adapt calls for their specific frontend, but don't own
  separate backend logic.

Matches the accompanying text: "the BFF... is a well-established IT
concept to technically decouple frontend applications running on
customer device from backend APIs... Both applications, on customer
device and BFF, are parts of the ODA Engagement domain."
