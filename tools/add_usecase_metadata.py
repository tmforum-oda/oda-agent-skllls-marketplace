"""tools/add_usecase_metadata.py -- fill in the catalog-page envelope fields
tools/docx2md.py can't derive from the DOCX alone (spec/spec.md 5.1, tasks.md 0.6).

docx2md.py owns the body Markdown and everything parseable straight out of the
DOCX (id, name, version, source.sha256/raw_path, links.components/apis,
sid_references). This script owns everything that only exists on the
document's TM Forum catalog page: status, maturity, approval_status,
release_status, team_approved, published, source.origin, source.license.

Deliberately a separate script, not folded into docx2md.py: the catalog page
requires the same TM Forum member login as the download itself (spec/spec.md
6.1's assisted track), so these fields have to be collected by a human
alongside the download, on a different cadence than reconverting the DOCX.
This script only ever *merges* -- every field it doesn't touch (links, body,
sid_references, ...) is written back exactly as it was read.

Usage: fill in the fields below for the use case you just downloaded and run

    python add_usecase_metadata.py <path/to/TMFSxxx.md> \
        --status "GA . TM Forum Approved" --maturity GA \
        --approval-status "TM Forum Approved" --release-status Production \
        --team-approved 2025-04-24 --published 2025-05-19 \
        --origin "https://www.tmforum.org/resources/..." --license RAND
"""
import argparse
import sys

import _yaml_lite as yaml_lite

parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("path", help="path to the knowledge/use-cases/TMFSxxx/TMFSxxx.md file")
parser.add_argument("--status", required=True, help='envelope rollup, e.g. "GA . TM Forum Approved"')
parser.add_argument("--maturity", required=True, choices=["Alpha", "Beta", "GA"])
parser.add_argument("--approval-status", required=True, help='e.g. "TM Forum Approved", "Member Evaluated"')
parser.add_argument("--release-status", required=True, choices=["Production", "Pre-production"])
parser.add_argument("--team-approved", required=True, help="YYYY-MM-DD")
parser.add_argument("--published", required=True, help="YYYY-MM-DD")
parser.add_argument("--origin", required=True, help="the document's TM Forum catalog page URL")
parser.add_argument("--license", default="RAND", help="IPR mode as shown on the catalog page")
args = parser.parse_args()

with open(args.path, encoding="utf-8") as f:
    data, body = yaml_lite.split(f.read())

missing = [k for k in ("id", "type", "name", "version", "links") if k not in data]
if missing:
    sys.exit(f"{args.path}: missing envelope field(s) {missing} -- did docx2md.py run cleanly on this file?")

data["status"] = args.status
data["source"]["origin"] = args.origin
data["source"]["license"] = args.license
data["maturity"] = args.maturity
data["approval_status"] = args.approval_status
data["release_status"] = args.release_status
data["team_approved"] = args.team_approved
data["published"] = args.published

yaml_lite.write(args.path, data, body)
print(f"Updated {args.path}: status={args.status!r}")
