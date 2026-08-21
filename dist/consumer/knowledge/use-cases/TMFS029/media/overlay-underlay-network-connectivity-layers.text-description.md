Architecture/block diagram appearing in the Introduction / Scope section (Fig 1.1, referencing IG1373 Use Case Access Domain section 3.3.8 underlay network).

The image shows two stacked, parallelogram-shaped network "planes":

- **Overlay Network / Service Connectivity** (top plane): two network-node icons connected by a solid black line representing a service-level connection.
- **Underlay Network / Network Connectivity** (bottom plane): six network-node icons interconnected by solid black lines, forming a small mesh topology.

Vertical dotted lines connect each of the two overlay nodes straight down to a corresponding node in the underlay plane, illustrating that each overlay (service) connectivity endpoint is realized by, and dependent on, a specific node in the underlay (physical/network) topology. The diagram illustrates the general principle — introduced in this section and reused throughout the use case — that a logical/service-level connection (e.g. an SD-WAN overlay circuit) is layered on top of, and dependent on, an underlay transport network connection (e.g. MPLS/IP transport).
