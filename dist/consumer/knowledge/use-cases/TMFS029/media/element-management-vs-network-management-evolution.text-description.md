Architecture/block diagram (Figure 2.2, "Evolution of IP Management") contrasting legacy element management with modern network/controller-based management, side by side.

Left side, titled **"Element Management"**: a single "Element Management" server icon (labelled "Per Device FCAPS") is reached via a "Proprietary API / Per device resource requests" line (example given: "device alarms"). Dashed lines fan out from the Element Management icon down to five network-device icons connected in a small mesh (a chain of routers/switches).

A dark arrow points from the left side to the right side, indicating an evolution.

Right side, titled **"Network Management"**: a pink/magenta "Network Controller" icon (labelled "Network FCAPS") sits inside a green-dashed box "Cross-Operational Domain Control Plane", reached via an "Open API Model Based Domain Specific Language / Per Network Intent Requests" line (example given: "Network Root Cause Event"). Below it, dashed lines fan out to the same style of five-node network mesh, but this time the devices are grouped into three green-dashed sub-domains: "Access Operational Domain", "Physical Operational Domain", and "Underlay Operational Domain" (each containing one or more of the colour-coded device icons).

The diagram illustrates the shift from per-device proprietary element management (FCAPS at the device level) to intent-based, API-driven network management operating across defined Operational Domains.
