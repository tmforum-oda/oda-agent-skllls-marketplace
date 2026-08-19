"""tools/fetch_api_samples.py -- OPTIONAL enrichment (spec/spec.md 5.3.1, tasks.md 2.6).

Pulls documentation/operation-samples/ and documentation/notification-samples/
from the *authoring* repo, tmforum-rand/OAS_Open_API_And_Data_Model, into
knowledge/apis/TMFxxx/samples/ for every API already cached from the
*published* source (fetch_api.py). These are real, human-authored example
request/response/event payloads TM Forum's own API authors wrote for
conformance testing -- genuinely useful for a test-data-generation skill,
better than synthesizing examples from the schema alone.

This is a DIFFERENT, PRIVATE repo requiring tmforum-rand GitHub org access
-- a third access tier, distinct from both the fully-public component/API
fetch (fetch_component.py, fetch_api.py) and the TM Forum website member
login (docx2md.py's assisted track). Never required: nothing in spec.md
5/8 depends on samples being present, and a skill using them must degrade
gracefully to the schema alone when they're not. Fails closed -- skip and
log, never raise past a single API's samples -- for exactly that reason.

The dev repo mostly tracks Gen5-in-progress APIs; most of what fetch_api.py
cached is Gen4 (the currently published generation). Version numbers won't
usually match, and that's fine -- samples are illustrative regardless of the
exact minor version, so this fetches whatever version folder exists rather
than insisting on an exact match.

Usage:
    python fetch_api_samples.py               # every API already cached under knowledge/apis/
    python fetch_api_samples.py TMF632 TMF644  # just these
"""
import glob
import json
import os
import subprocess
import sys
import urllib.parse

import _http

REPO = "tmforum-rand/OAS_Open_API_And_Data_Model"
KNOWLEDGE_DIR = os.path.join(os.path.dirname(__file__), "..", "knowledge")
MAP_PATH = os.path.join(KNOWLEDGE_DIR, "index", "api-samples-folder-map.json")
SAMPLE_DIRS = ("documentation/operation-samples", "documentation/notification-samples")


def gh_token():
    try:
        result = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def check_access(token):
    if not token:
        return False
    try:
        _http.get_json(f"https://api.github.com/repos/{REPO}", headers={"Authorization": f"Bearer {token}"})
        return True
    except _http.FetchError:
        return False


def build_folder_map(token):
    entries = _http.get_json(
        f"https://api.github.com/repos/{REPO}/contents/apis", headers={"Authorization": f"Bearer {token}"}
    )
    folder_map = {}
    for entry in entries:
        if entry["type"] == "dir" and entry["name"].startswith("TMF"):
            api_id, _, _short = entry["name"].partition("_")
            folder_map[api_id] = entry["name"]
    os.makedirs(os.path.dirname(MAP_PATH), exist_ok=True)
    with open(MAP_PATH, "w", encoding="utf-8") as f:
        json.dump(folder_map, f, indent=2, sort_keys=True)
    return folder_map


def latest_version_dir(api_folder, token):
    entries = _http.get_json(
        f"https://api.github.com/repos/{REPO}/contents/apis/{api_folder}",
        headers={"Authorization": f"Bearer {token}"},
    )
    versions = sorted((e["name"] for e in entries if e["type"] == "dir"), reverse=True)
    return versions[0] if versions else None


def fetch_samples_for(api_id, api_folder, token):
    version_dir = latest_version_dir(api_folder, token)
    if not version_dir:
        return 0, 0
    out_dir = os.path.join(KNOWLEDGE_DIR, "apis", api_id, "samples")
    count, failed = 0, 0
    for sample_kind in SAMPLE_DIRS:
        url = f"https://api.github.com/repos/{REPO}/contents/apis/{api_folder}/{version_dir}/{sample_kind}"
        try:
            files = _http.get_json(url, headers={"Authorization": f"Bearer {token}"})
        except _http.FetchError:
            continue  # this API has no samples of this kind -- not an error, just nothing to fetch
        for entry in files:
            if entry["type"] != "file":
                continue
            # entry["download_url"]'s signed token turned out unreliable in practice (frequent
            # SSL_CONNECT_ERROR, curl 35, not fixed by retrying the same URL -- looks single-use
            # or very short-lived). Fetch through the same authenticated Contents API call we
            # already know works instead, asking for raw bytes via the Accept header, rather than
            # a separate signed URL mechanism.
            # a handful of source filenames have spaces in them (e.g. an accidental
            # "... copy.json" duplicate in the upstream repo) -- quote() or the URL breaks
            file_url = f"https://api.github.com/repos/{REPO}/contents/apis/{api_folder}/{version_dir}/{sample_kind}/{urllib.parse.quote(entry['name'])}"
            try:
                raw = _http.get_bytes(file_url, headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github.raw"})
            except _http.FetchError as e:
                failed += 1
                print(f"    {api_id}/{entry['name']}: FAILED -- {e}")
                continue
            os.makedirs(out_dir, exist_ok=True)
            with open(os.path.join(out_dir, entry["name"]), "wb") as f:
                f.write(raw)
            count += 1
    return count, failed


def cached_api_ids():
    ids = set()
    for path in glob.glob(os.path.join(KNOWLEDGE_DIR, "apis", "*", "*.meta.json")):
        with open(path, encoding="utf-8") as f:
            ids.add(json.load(f)["id"])
    return sorted(ids)


def main():
    token = gh_token()
    if not check_access(token):
        print(f"No usable tmforum-rand-authorized GitHub token -- skipping {REPO} entirely (this is optional, spec.md 5.3.1). Nothing else is affected.")
        return

    folder_map = build_folder_map(token)
    ids = sys.argv[1:] or cached_api_ids()

    matched, unmatched, total_files, total_failed = 0, 0, 0, 0
    for api_id in ids:
        folder = folder_map.get(api_id)
        if not folder:
            unmatched += 1
            continue
        try:
            n, failed = fetch_samples_for(api_id, folder, token)
        except _http.FetchError as e:
            print(f"{api_id}: FETCH FAILED -- {e}")
            continue
        total_failed += failed
        if n:
            matched += 1
            total_files += n
            suffix = f" ({failed} file(s) failed)" if failed else ""
            print(f"{api_id}: {n} sample file(s){suffix}")
        else:
            unmatched += 1

    print(
        f"\n{matched}/{len(ids)} API(s) got samples ({total_files} files, {total_failed} individual file failures); "
        f"{unmatched} had no matching folder or no samples in it -- expected, not an error, per this script's docstring."
    )


if __name__ == "__main__":
    main()
