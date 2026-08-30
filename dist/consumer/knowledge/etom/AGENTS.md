# knowledge/etom/ — Agent Instructions

**Reserved, not populated in v1.** This folder holds a `.gitkeep` only —
no eTOM (Business Process Framework) content has been extracted into this
corpus yet.

Do not treat an empty `etom/` as a bug or a fetch that failed. Do not
fabricate eTOM process content to fill this folder. If you need eTOM
activity information for a specific component, it's already embedded in
that component's own `component.yaml` (`componentMetadata.eTOMs`) or
narrative `TMFCxxx.md` (§2.1 "eTOM business activities") — read it from
there, not from here.

The intended future shape (TM Forum's Sparx EA model, exported via a
separate XMI → structured YAML → Markdown pipeline, not yet built) is
recorded in [`spec/spec.md`](../../spec/spec.md) §7. `GBxxx` (`GB921` for
eTOM) is the reserved id prefix for whatever eventually lands here — see
[`knowledge/index/id-registry.md`](../index/id-registry.md).
