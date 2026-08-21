Architecture/block diagram, captioned "Figure 1. SNO to MNO Integration models". Appears in the "Context or Background" section, showing three side-by-side deployment/integration models between a Satellite Network Operator (SNO) and a Mobile Network Operator (MNO), each ending at the same handset icon at the bottom.

**Same PLMN or "satellite cell provider"** (left): a single grey "Mobile Operator A" box contains a Core Network, which connects down to both a 3GPP NTN RAN (blue) and a 3GPP RAN (grey); the 3GPP NTN RAN connects down to a "Satellite Operator" sub-box (satellite-dish icon) and the 3GPP RAN connects to a terrestrial tower icon. Everything is inside one operator's domain.

**Roaming** (middle): two separate boxes side by side — "Satellite-Mobile Operator B" (darker grey, containing its own Core Network → 3GPP NTN RAN → Satellite pipe/satellite icon) and "Mobile Operator A" (lighter grey, containing its own Core Network → 3GPP RAN → tower icon) — with a dashed line connecting the two Core Network boxes, representing a roaming interconnection between independent operators.

**RAN Sharing** (right): the same two-box layout as Roaming (Satellite-Mobile Operator B and Mobile Operator A, each with their own Core Network, RAN, and satellite/tower icons), but the dashed interconnection line is drawn between the 3GPP NTN RAN box and the 3GPP RAN box instead of between the Core Networks — representing RAN-level sharing rather than core-level roaming.

All three models terminate at the same handset icon at the bottom, indicating the end-user device is served identically regardless of which integration model the operators chose.
