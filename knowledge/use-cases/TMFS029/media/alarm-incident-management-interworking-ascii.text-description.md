ASCII-art architecture diagram (Fig 3.3.3, "Interworking with Alarm Management IETF NMOP Network Incident YANG-03") illustrating Alarm/Incident Management Service interworking in the Reactive assurance section.

The diagram is a nested box-and-line tree drawn in monospace text, top to bottom:

- **"OSS"** (top box), containing two child boxes side by side: **"Alarm handler"** and **"Incident handler"**.
- Below, connected up to the Alarm handler via an **"alarm"** labelled line and to the Incident handler via an **"incident"** labelled line, is a **"controller"** box.
- Below the controller, two child boxes side by side: **"Alarm process"** (which sends an **"alarm"**-labelled arrow across to) **"Incident Process"**.
- Both the Alarm process and Incident Process connect down to a **"Network"** box at the bottom, via lines labelled **"alarm"** and **"metrics/trace/etc."** respectively.

The diagram shows how raw network alarms and metrics/traces flow up from the Network, through a controller's Alarm process (which also feeds the Incident Process), and are exposed to the OSS as separate Alarm and Incident handler interfaces — illustrating how alarm reporting and incident reporting interwork at the controller level.
