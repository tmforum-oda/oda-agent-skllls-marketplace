# knowledge/apis/

51 TM Forum Open API schemas (`TMFxxx`) — the OpenAPI/Swagger contracts
that ODA Components expose or depend on, cached exactly as published.

If you're an AI agent, read [`AGENTS.md`](AGENTS.md) here first.

## Layout

```
TMF620/
├── TMF620_v4.0.0.json         the OpenAPI/Swagger schema, unmodified
├── TMF620_v4.0.0.meta.json    envelope: id/type/name/version/status/source
└── samples/                   real example request/response JSON payloads,
                                where available (best-effort, GitHub-sourced)
```

The `v{version}` in the filename is deliberate: this layout supports
multiple versions of the same API coexisting (a component or use case can
reference an older version without it being overwritten by a newer
fetch), even though every API in the corpus currently has just one cached
version.

## Where these come from

Each API a cached `component.yaml` declares as an exposed or dependent
API gets fetched here — see [`spec/spec.md`](../../spec/spec.md) §5.3 for
the discovery mechanism (no separate directory to browse; API ids and
versions are read straight out of the components that reference them).

## Regenerating

```bash
python tools/fetch_api.py             # schema -- automated, public, safe to schedule
python tools/fetch_api_samples.py     # sample payloads -- optional, needs a GitHub token
```

Both only rewrite files whose content actually changed.
