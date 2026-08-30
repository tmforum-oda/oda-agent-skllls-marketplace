# knowledge/sid/

Reserved for a future export of TM Forum's SID (Shared Information/Data
Model) — **not populated in v1**. Currently holds only a `.gitkeep` so
the folder exists in git.

If you're an AI agent, read [`AGENTS.md`](AGENTS.md) here first — in
short: an empty folder here is expected, not a gap to fill in or a fetch
that failed.

SID entity information that already exists in this corpus today lives
inline in each component's own record — see
[`../components/`](../components/) (`component.yaml`'s
`componentMetadata.SIDs`, and a `TMFCxxx.md`'s own "SID ABEs" / "eTOM L2
- SID ABEs links" sections where a narrative PDF exists). One known SID
gap already surfaced by use-case authors is tracked in
[`../index/gaps-backlog.md`](../index/gaps-backlog.md) #5, precisely
because it couldn't be cross-checked against a local SID corpus.

The intended future shape for this folder — TM Forum's Sparx EA model,
exported through a separate XMI → structured YAML → Markdown pipeline —
is recorded in [`spec/spec.md`](../../spec/spec.md) §7, alongside the
same note for [`../etom/`](../etom/). Neither has been built yet.
