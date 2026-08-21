# sase-service-architecture-diagram.png

**Type:** Network architecture illustration, not a UML diagram or
entity-relationship model.
**Source context:** `# Description` section, right after the SASE
architecture explanation, illustrating a simplified SASE (Secure Access
Service Edge) service architecture with three regions and three
subscriber locations.

A central green "SASE Provider Network" region contains two `SASE Edge`
nodes (each with `Security Functions` and `IdAM` diamonds, one further
annotated "for ZTNA: PAP, PIP, PDP" and a red "SASE Policy Endpoint, for
ZTNA: PEP" marker) connected to each other and to a third SASE Edge by
dotted lines. Three "Subscriber Network" octagons (light blue), each
containing an Actor icon (person at a computer), connect to the
provider network:

- **Location A** (Region 1/3 boundary) — an `Actor` connects via
  `Actor Access Conn` (striped red/white overlay link) through a
  "Customer termination point" circle and "SASE UNI" label into the
  left `SASE Edge` node, which itself has `Security Functions (DNS
  security, FWaaS)` and a red marker.
- **Location B** (Region 2, top right) — connects via a striped
  red/white link into the right `SASE Edge` (ZTNA-focused) node.
- **Location C** (bottom right, grey octagon) — contains a yellow
  "Appliance" wedge running a "SASE Edge **Agent**" (with its own IdAM
  diamond and red marker), connecting via "SASE UNI" to a third
  "Subscriber Network" octagon with its own Actor icon.

Faint dashed lines in the background separate the diagram into "Region
1", "Region 2", and "Region 3" zones.
