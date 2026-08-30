# knowledge/sid/ — Agent Instructions

**Reserved, not populated in v1.** This folder holds a `.gitkeep` only —
no SID (Shared Information/Data Model) content has been extracted into
this corpus yet.

Do not treat an empty `sid/` as a bug or a fetch that failed. Do not
fabricate SID entity/attribute definitions to fill this folder. If you
need SID information for a specific component, it's already embedded in
that component's own `component.yaml` (`componentMetadata.SIDs`) or
narrative `TMFCxxx.md` (§2.2 "SID ABEs", §2.3 "eTOM L2 - SID ABEs
links") — read it from there, not from here.
[`knowledge/index/gaps-backlog.md`](../index/gaps-backlog.md) #5 already
notes one known SID gap that couldn't be cross-checked against a local
corpus for exactly this reason.

The intended future shape (TM Forum's Sparx EA model, exported via a
separate XMI → structured YAML → Markdown pipeline, not yet built) is
recorded in [`spec/spec.md`](../../spec/spec.md) §7. `GBxxx` (`GB922` for
SID) is the reserved id prefix for whatever eventually lands here — see
[`knowledge/index/id-registry.md`](../index/id-registry.md).
