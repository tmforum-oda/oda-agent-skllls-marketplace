"""Reads: nothing itself -- library of frontmatter parse/emit functions.
Writes: nothing itself -- library of frontmatter parse/emit functions.
Track: n/a -- shared helper imported by docx2md.py, add_usecase_metadata.py,
build_index.py, and fetch_component.py (both tracks).

Shared, dependency-free YAML frontmatter read/write for tools/*.py.

Writing uses a minimal, deterministic emitter (not PyYAML's dump) so every
tool that touches a knowledge artefact's frontmatter produces byte-identical
formatting for identical data -- required for idempotent regeneration
(spec/spec.md principle 7). Reading uses PyYAML (safe_load), which is fine:
consistency only matters for what we write, not for what we're willing to
parse back in.
"""
import re

import yaml

FRONTMATTER_RE = re.compile(r"^---\n(.*?\n)---\n\n?", re.DOTALL)


def split(text):
    """(frontmatter_dict, body_str). Raises ValueError if there's no frontmatter block."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        raise ValueError("no --- frontmatter block found at the start of the file")
    data = yaml.safe_load(m.group(1)) or {}
    body = text[m.end() :]
    return data, body


def dump(obj, indent=0):
    """Minimal, dependency-free YAML emitter -- good enough for this repo's fixed
    schema shape (dicts, lists of dicts/scalars, strings, None). Not a general
    purpose serializer; don't reach for it outside tools/*.py's own frontmatter."""
    pad = "  " * indent
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, (dict, list)) and v:
                out.append(f"{pad}{k}:")
                out.append(dump(v, indent + 1))
            elif isinstance(v, list):
                out.append(f"{pad}{k}: []")
            else:
                out.append(f"{pad}{k}: {scalar(v)}")
    elif isinstance(obj, list):
        for item in obj:
            if isinstance(item, dict):
                first = True
                for k, v in item.items():
                    prefix = f"{pad}- " if first else f"{pad}  "
                    out.append(f"{prefix}{k}: {scalar(v)}")
                    first = False
            else:
                out.append(f"{pad}- {scalar(item)}")
    return "\n".join(out)


def scalar(v):
    if v is None:
        return '"TODO"'
    s = str(v)
    if s == "TODO" or any(c in s for c in ":#\"'") or s != s.strip():
        return f'"{s}"'
    return s


def render(data, body):
    return "---\n" + dump(data) + "\n---\n\n" + body


def write(path, data, body):
    with open(path, "w", encoding="utf-8") as f:
        f.write(render(data, body))
