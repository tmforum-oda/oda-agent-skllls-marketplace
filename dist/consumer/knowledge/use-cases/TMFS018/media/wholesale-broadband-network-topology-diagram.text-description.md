# wholesale-broadband-network-topology-diagram.png

**Type:** Network topology illustration, not a UML or
entity-relationship diagram.
**Source context:** `# Information View` / `## Products Understanding`,
mapping the four wholesale broadband products (WB Access, WB Bitstream
Profile, WB Bitstream Transport, WB ENNI) onto the physical network path
from end customer to buyer, and marking who is responsible for each
segment.

Left-to-right physical chain: `End Customer Router` — `Network
Terminating Unit (NTU)/L2 CPE` — `Access Node/Optical Line Termination
(OLT)` — `Local/National Network (Metro)` cloud — `Network-to-Network
(NNI) Router` — `Network-to-Network (NNI) Router` — `Buyer Network`
cloud. Four dashed overlay lines mark the products: `WB Access` (NTU to
Access Node), `WB Bitstream Profile` (a circle above the Access Node),
`WB Bitstream Transport` (Access Node through the Metro cloud to the
first NNI Router), `WB ENNI` (between the two NNI Routers). Bottom
brackets mark ownership zones: `Customer Premises Equipment` / `Seller
network` / `Point of Interconnect (POI)` segments, and below that
`End customer/Buyer responsibility` / `Seller responsibility` / `Buyer
responsibility` spans.
