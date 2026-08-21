Functional and topology architecture diagram, captioned "Figure . Wholesale NTN Cell: Functional and topology architecture". Appears in the "Functional Architecture Diagram" section, illustrating the physical/functional split between the Satellite Network Operator (SNO) and Mobile Network Operator (MNO) domains for delivering Wholesale NTN Cell Capacity.

Left side: an Earth globe (Europe/Africa/Middle East visible) with three satellite icons in orbit around the top. Two satellite ground-station dish icons sit on the globe's surface, each connected by colored beam cones down to a cluster of small circle icons on the ground, labelled with a "Region1" callout and a specific cell, **"Cell 1.1"** (the red-beam cluster). A third beam cluster (green) is shown from the third satellite to a second ground station, and a fourth unlabelled dark cluster sits near the center of the visible landmass. A handset icon sits near "Region1".

A vertical dashed line separates **SNO** (left of the line) from **MNO** (right of the line).

Right side, two parallel horizontal chains, one per ground station/teleport:
- **NTN Teleport link 1** (dark navy bar) receives the beam from the first ground station and fans out to four **RU per cell** icons (chip/radio-unit icons), each connected onward to a shared **RAN: CU/DUs** box, which connects to a **Core Network** box.
- **NTN Teleport link 2** (dark navy bar) receives the beam from the second ground station and fans out to its own four **RU per cell** icons, connected to its own **RAN: CU/DUs** box and **Core Network** box.

The diagram illustrates the text's key point: the SNO does not run 3GPP gNB functions on the satellite or at the ground station gateway — the MNO fully forms the radio signal structure and deploys the Radio Units (RUs), which output digitized (not RF-amplified) signals; the SNO's ground-station equipment performs the RF amplification and satellite uplink, connected to the MNO's RUs over a terrestrial high-capacity data link via the NTN Teleport link.
