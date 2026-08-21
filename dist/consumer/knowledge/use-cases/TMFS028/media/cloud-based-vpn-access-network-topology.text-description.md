Network architecture/topology diagram. Appears at the end of the enterprise networking scenario description, illustrating the access methods and network segments that make up the Cloud-Based VPN product.

Left column: six customer-premises access setups, each a device icon connected via a line to an access-network cloud, all converging on the central **"Private Network (CN2)"** cloud:

1. **GATEWAY** (computer + router icon) → **PON** cloud → **MAN MPLS VPN** cloud → also connects out to a separate **INTERNET** globe icon.
2. **U** (computer + router icon, labelled CE-side) → **IPRAN/STN** cloud → Private Network (CN2).
3. **CE** (building + router icon) → directly to Private Network (CN2), no intermediate cloud.
4. **CE** (computer + router icon) → **SD-WAN Device** router → an **INTERNET** globe icon → **SD-WAN POP** router → Private Network (CN2).
5. **5G CPE** (device icon) → connected by a zigzag (radio) line to a cell-tower icon → **STN** cloud → Private Network (CN2).
6. **CPE** (computer + router icon) → **OTN** cloud → Private Network (CN2).

The **MAN MPLS VPN** cloud and the **STN** cloud both also connect directly into the central **Private Network (CN2)** cloud (shown by the converging lines from the upper and middle access paths).

Right side: the central **Private Network (CN2)** cloud connects out (via a bracket/junction) to two destination clouds:
- **Oversea Third-Party Cloud**
- **Domestic Third-Party Cloud**

In summary, the diagram shows every supported access method (PON/MAN-MPLS-VPN, IPRAN/STN, direct CE, SD-WAN over Internet, 5G/STN, and OTN) funnelling into the shared Private Network (CN2), which in turn provides connectivity out to both overseas and domestic third-party cloud resource pools — the physical/network realization of the Fixed Access, Mobile Access, and Cloud Access CFSs described in the Information View.
