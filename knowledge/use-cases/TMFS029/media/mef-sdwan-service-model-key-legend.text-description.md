Text legend/key ("Key for MEF SD-WAN Service Model MEF 70.1") defining the eight lettered callouts (A–H) used in the accompanying `sdwan-service-provider-network-lettered-overview.png` diagram and reused later in the "OSI Layered Service Model" family of diagrams. Two columns of definitions:

Left column:
- **A — SD-WAN User-to-Network Interface (SD-WAN UNI):** Demarcation between Service Provider and Subscriber responsibility.
- **B — SD-WAN Edge:** Connects SD-WAN UNI to UCSs, maps packets to application flows, enforces policies, and selects TVC, over which to forward each flow.
- **C — SD-WAN Virtual Connection (SWVC):** Logical multipoint connection between the SD-WAN UNIs, which corresponds to the SD-WAN Service.
- **D — Underlay Connectivity Service (UCS):** Any WAN service used by the SD-WAN, e.g., MEF Ethernet Services (MEF 6.2), MEF IP Services (MEF 61.1), MPLS VPNs and Internet Access, and MEF Optical Transport Services (MEF 63).

Right column:
- **E — UCS User-to-Network Interface (UCS UNI):** Demarcation between the service provider of the underlay connectivity service, and the subscriber responsibility.
- **F — SD-WAN Virtual Connection End Point (SWVC EP):** Logical point where application-flow policies are assigned and applied.
- **G — Tunnel Virtual Connection (TVC):** Point-to-point paths across UCSs that compose an SD-WAN Service.
- **H — Internet Breakout:** Application flows forwarded from an SD-WAN UNI directly to the Internet rather than delivered to another SD-WAN UNI.
