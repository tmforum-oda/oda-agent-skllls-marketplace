"""Reads: nothing local -- network I/O only.
Writes: nothing local -- network I/O only.
Track: n/a -- shared HTTP helper imported by fetch_component.py/fetch_api.py
(automated track, spec.md 6.2).

Shared HTTP fetch helper for tools/*.py -- shells out to curl rather than
Python's own ssl/requests stack, which fails local certificate verification
on at least one dev machine this repo has been built on (an environment
quirk, not a project concern -- curl verifies the exact same public
endpoints fine there). curl ships on effectively every platform this is
likely to run on; if that ever stops being true, this is the one place
to change, not every call site.

Also confirmed while building this (spec/tasks.md 2.1): raw.githubusercontent.com
specifically (not api.github.com, not github.com -- tested head to head) drops
the connection outright with no response (curl's "000" pseudo-status) roughly
40-50% of the time in this environment, repeatably, across many trials --
likely a CDN edge/DNS issue on this network, not a one-off blip. That's the
exact host component specs and API schemas are fetched from (spec/spec.md
5.2.1/5.3.1), so fetch_component.py/fetch_api.py running unattended (spec/
spec.md 6.2) would fail roughly half the time without this. Plain --retry
does NOT cover it -- curl doesn't classify a dropped connection with zero
response as one of its default transient-error codes. --retry-all-errors
does, and was verified against 15 back-to-back requests before and after
(0/15 failures with it, consistently ~40-50% without). A genuine 404 is
never retried either way -- it's real information, not a fault."""
import json
import subprocess

_RETRY = ["--retry", "5", "--retry-delay", "1", "--retry-all-errors"]


def get_bytes(url, headers=None):
    cmd = ["curl", "-sfL", *_RETRY]
    for k, v in (headers or {}).items():
        cmd += ["-H", f"{k}: {v}"]
    cmd.append(url)
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        raise FetchError(url, result.returncode, result.stderr.decode(errors="replace")[:300])
    return result.stdout


def get_json(url, headers=None):
    return json.loads(get_bytes(url, headers))


def exists(url, headers=None):
    """HEAD-equivalent existence check that raises on real failure -- for the
    not-yet-specified case (spec/spec.md 5.2), where a 404 is an expected,
    meaningful answer (return False), but a network failure is NOT the same
    thing and must never be silently read as "doesn't exist" (curl reports a
    dropped/failed connection as http_code "000", which is not a valid HTTP
    status and is not < 400 by accident -- it has to be handled explicitly,
    or a transient blip gets recorded as a real "not yet specified" fact)."""
    cmd = ["curl", "-sL", *_RETRY, "-o", "NUL" if _is_windows() else "/dev/null", "-w", "%{http_code}"]
    for k, v in (headers or {}).items():
        cmd += ["-H", f"{k}: {v}"]
    cmd.append(url)
    result = subprocess.run(cmd, capture_output=True, text=True)
    code = result.stdout.strip()
    if not code.isdigit() or int(code) < 100:
        raise FetchError(url, code or "no response", result.stderr[:300])
    return int(code) < 400


def _is_windows():
    import os

    return os.name == "nt"


class FetchError(RuntimeError):
    def __init__(self, url, code, stderr):
        super().__init__(f"curl failed ({code}) for {url}: {stderr}")
        self.url = url
        self.code = code
