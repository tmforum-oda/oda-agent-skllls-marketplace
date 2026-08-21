Architecture/block diagram appearing in the Introduction section, immediately after the description of what the TMF Operate API lets a Channel Partner do (subscribe to/manage Service APIs, onboard/manage Application Owners, create/manage Applications for those Application Owners).

The diagram is a simple left-to-right actor chain:

- Three **End User** icons on the far left, each connected by a line to a single **Developer** box, labelled "Developer (Application Service Provider, B2B Customer, ...)".
- The **Developer** box connects to a **Channel Partner** box, labelled "Channel Partner (Aggregator, Hyperscaler, ...)".
- The **Channel Partner** box fans out to four CSP boxes on the right: **CSP #1**, **CSP #2**, **CSP #3**, and **CSP #N**, each connection marked with a blue star icon.
- A legend box in the top-right explains the blue star icon: "Operate Api".

The diagram illustrates the general ecosystem chain the use case operates in: end users are served by a developer/application, the developer relies on a Channel Partner, and the Channel Partner reaches an arbitrary number of CSPs (CSP #1 through CSP #N) through the Operate API.
