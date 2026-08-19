"""tools/fetch_api.py -- cache the OpenAPI/Swagger specs a cached component
declares it exposes or depends on (spec/spec.md 5.3, 5.3.1).

No separate id->URL lookup needed, unlike components (5.2.1): the URL is
already sitting inside every already-fetched component.yaml, at
{coreFunction,managementFunction,securityFunction}.{exposedAPIs,dependentAPIs}
[].specification[].url. This script only reads component.yaml files that
fetch_component.py has already written -- run that first.

Multiple versions of the same API can coexist side by side
(TMF632_v4.0.0.json, TMF632_v5.0.0.json) because components genuinely
track more than one live generation at once (Gen4/Gen5 coexistence, same
as oda-canvas). Every distinct (id, version) pair found across every
component is fetched once, regardless of how many components reference it.

Public, unauthenticated, safe to run on a schedule (spec/spec.md 6.2).

Usage:
    python fetch_api.py                      # every API referenced by any cached component.yaml
    python fetch_api.py TMFC020 TMFC028       # only APIs referenced by these components
"""
import datetime as _dt
import glob
import hashlib
import json
import os
import re
import sys

import _http
import yaml

KNOWLEDGE_DIR = os.path.join(os.path.dirname(__file__), "..", "knowledge")
FUNCTION_BLOCKS = ("coreFunction", "managementFunction", "securityFunction")
API_LIST_KEYS = ("exposedAPIs", "dependentAPIs")
REAL_API_ID = re.compile(r"^TMF\d+$")


def apis_in(component_yaml_path):
    """Yield (api_id, api_name, url, version) for every specification[] entry
    named anywhere in one component.yaml, across all three function blocks.

    Every component.yaml checked so far has an unfilled Helm-template
    placeholder in managementFunction (id: "exposedAPI_id", url:
    "{{.Release.Name}}-{{.Values.component.name}}-sm", etc. -- literal
    token names, not real values, apparently left over from whatever
    generated these specs). That's the metrics-scraping self-reference for
    the component's own deployed instance, not a TM Forum API to fetch, so
    it's filtered here by id shape rather than trusted as data -- a real
    API id is always TMFxxx."""
    with open(component_yaml_path, encoding="utf-8") as f:
        spec = yaml.safe_load(f)
    s = (spec or {}).get("spec", {})
    for block in FUNCTION_BLOCKS:
        for key in API_LIST_KEYS:
            for api in s.get(block, {}).get(key, []) or []:
                api_id = api.get("id", "")
                if not REAL_API_ID.match(api_id):
                    continue
                for entry in api.get("specification", []) or []:
                    url = entry.get("url")
                    if url:
                        yield api_id, api.get("name", api_id), url, entry.get("version", "unknown")


def component_paths(comp_ids=None):
    if comp_ids:
        return [os.path.join(KNOWLEDGE_DIR, "components", c, "component.yaml") for c in comp_ids]
    return sorted(glob.glob(os.path.join(KNOWLEDGE_DIR, "components", "*", "component.yaml")))


def version_tag(version):
    """'v4.0.0' -> 'v4.0.0'; '4.0.0' -> 'v4.0.0' -- always exactly one leading v."""
    return "v" + version.lstrip("vV")


def fetch_one(api_id, name, url, version):
    tag = version_tag(version)
    out_dir = os.path.join(KNOWLEDGE_DIR, "apis", api_id)
    os.makedirs(out_dir, exist_ok=True)
    json_path = os.path.join(out_dir, f"{api_id}_{tag}.json")
    meta_path = os.path.join(out_dir, f"{api_id}_{tag}.meta.json")

    raw = _http.get_bytes(url)
    with open(json_path, "wb") as f:
        f.write(raw)

    generation = tag.split(".")[0]  # 'v4.0.0' -> 'v4' -- status is just the API's own generation (spec.md 5.3)
    envelope = {
        "id": api_id,
        "type": "api",
        "name": name,
        "version": tag,
        "status": generation,
        "source": {
            "origin": url,
            "license": "RAND",
            "retrieved": _dt.date.today().isoformat(),
            "sha256": hashlib.sha256(raw).hexdigest(),
        },
        "links": {"use_cases": []},
    }
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(envelope, f, indent=2)
    return tag


def write_fetch_failed(api_id, name, tag, url, error):
    """A genuine broken link in an upstream component spec (e.g. TMF641's stale
    Beta S3 path, found while building this) is real signal, not a fluke to
    retry away -- record it as a visible fact in the data layer, the same way
    fetch_component.py's not_yet_specified does, not just a line in a log
    that scrolls away (spec/spec.md 5.2's "no silent gaps" principle applies
    here too, and the analogous file to component.meta.json's precedent)."""
    out_dir = os.path.join(KNOWLEDGE_DIR, "apis", api_id)
    os.makedirs(out_dir, exist_ok=True)
    envelope = {
        "id": api_id,
        "type": "api",
        "name": name,
        "version": tag,
        "status": "fetch_failed",
        "source": {"origin": url, "license": "RAND", "retrieved": _dt.date.today().isoformat(), "error": error},
        "links": {"use_cases": []},
    }
    with open(os.path.join(out_dir, f"{api_id}_{tag}.meta.json"), "w", encoding="utf-8") as f:
        json.dump(envelope, f, indent=2)


def main():
    args = sys.argv[1:]
    comp_paths = component_paths(args if args else None)
    if not comp_paths:
        sys.exit("no component.yaml files found -- run fetch_component.py first")

    seen = {}  # (api_id, tag) -> already fetched this run, don't refetch the same version twice
    fail_count = 0
    for comp_path in comp_paths:
        for api_id, name, url, version in apis_in(comp_path):
            tag = version_tag(version)
            key = (api_id, tag)
            if key in seen:
                continue
            try:
                fetch_one(api_id, name, url, version)
                seen[key] = "ok"
                print(f"{api_id} {tag}: ok")
            except _http.FetchError as e:
                write_fetch_failed(api_id, name, tag, url, str(e))
                seen[key] = "failed"
                fail_count += 1
                print(f"{api_id} {tag}: FETCH FAILED -- {e}")

    print(f"\n{len(seen)} unique API version(s) processed, {fail_count} failure(s)")


if __name__ == "__main__":
    main()
