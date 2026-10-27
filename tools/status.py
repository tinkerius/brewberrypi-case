#!/usr/bin/env python3
"""Pipeline status: which stage is done, which is stale, which waits for you.

Reads the spec version stamps the stages leave behind and checks they agree with the approved spec:
  requirements  "## Open questions" in requirements.md says "None"
  spec          top row of the version table in spec.md is approved   -> version V
  drawings      SPEC_VERSION in tools/make_drawings.py == V
  scad          "Built from spec version" in brewberrypi-case.scad == V
  stl           "Built from spec version" in 04-stl/README.md == V, 04-stl/.source-hash matches the .scad sources,
                no failed AC in the verification table
  print test    open ACs in the verification table (needs a print)
  readme        spec version in the README.md status table == V

States: done · stale (out of date with the approved spec, run the skill) · needs-you (human input or approval)
        · blocked (an earlier stage is not done) · warn.
Usage: python3 tools/status.py               table
       python3 tools/status.py --check       exit 1 if any stage is stale
       python3 tools/status.py --require S   exit 1 unless stage S and every stage before it are done
       python3 tools/status.py --next        first stale stage that runs headless (scad, stl), or nothing
       python3 tools/status.py --hash        hash of the .scad sources (tools/build.sh writes it to 04-stl/.source-hash)
"""
import hashlib
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
REQ = ROOT / "01-requirements" / "requirements.md"
SPEC = ROOT / "02-specification" / "spec.md"
DRAWINGS = ROOT / "tools" / "make_drawings.py"
SCAD_DIR = ROOT / "03-openscad"
SCAD = SCAD_DIR / "brewberrypi-case.scad"
STL_README = ROOT / "04-stl" / "README.md"
HASH_FILE = ROOT / "04-stl" / ".source-hash"
README = ROOT / "README.md"

ORDER = ["requirements", "spec", "drawings", "scad", "stl"]   # gated stages, in pipeline order
SKILL = {"requirements": "/requirements", "spec": "/spec", "drawings": "/spec", "scad": "/scad", "stl": "/stl",
         "print test": "/feedback", "readme": "README.md status table"}
HEADLESS = {"scad", "stl"}                                       # stages `make pipeline` may run via `claude -p`


def text(path):
    return path.read_text(encoding="utf-8") if path.exists() else ""


def source_hash():
    h = hashlib.sha256()
    for f in sorted(p for p in SCAD_DIR.rglob("*.scad") if "vendor" not in p.relative_to(SCAD_DIR).parts):
        h.update(f.relative_to(SCAD_DIR).as_posix().encode() + b"\0" + f.read_bytes() + b"\0")
    return h.hexdigest()


def built_from(path):
    m = re.search(r"Built from spec version:\s*\**\s*v?([\d.]+\d)", text(path))
    return m.group(1) if m else None


def evaluate():
    rows = {}   # stage -> (state, detail)

    section = re.search(r"^## Open questions\s*\n(.*?)(?=^## |\Z)", text(REQ), re.S | re.M)
    items = [ln for ln in (section.group(1).splitlines() if section else []) if ln.strip()]
    if section and items and re.match(r"-\s*None\b", items[0].strip()):
        rows["requirements"] = ("done", "no open questions")
    else:
        rows["requirements"] = ("needs-you", f"{len(items)} open question line(s)" if section else "no Open questions section")

    v = None
    top = next((ln for ln in text(SPEC).splitlines() if re.match(r"\|\s*v?\d+\.\d+\s*\|", ln)), None)
    if top is None:
        rows["spec"] = ("needs-you", "no version table in spec.md")
    else:
        version, status = [c.strip() for c in top.strip("|").split("|")][:2]
        version = version.lstrip("v")
        if "approved" in status.lower():
            v = version
            rows["spec"] = ("done", f"v{v} approved")
        else:
            rows["spec"] = ("needs-you", f"v{version} {re.sub(r'[*]', '', status)}, needs your approval")

    def stamp(stage, found, where):
        if v is None:
            rows[stage] = ("blocked", "no approved spec")
        elif found == v:
            rows[stage] = ("done", f"v{found}")
        else:
            rows[stage] = ("stale", f"{where} says v{found}, approved spec is v{v}")

    m = re.search(r'^SPEC_VERSION\s*=\s*"([\d.]+)"', text(DRAWINGS), re.M)
    stamp("drawings", m.group(1) if m else None, "make_drawings.py")
    stamp("scad", built_from(SCAD), "scad header")
    stamp("stl", built_from(STL_README), "04-stl/README.md")

    table = re.findall(r"^\|\s*(AC\d+)\s*\|[^|]*\|\s*([^|]*?)\s*\|", text(STL_README), re.M)
    failed = [ac for ac, res in table if "fail" in res.lower() or "❌" in res]
    open_ = [ac for ac, res in table if "open" in res.lower() or "⏳" in res]
    if rows["stl"][0] == "done":
        if not HASH_FILE.exists():
            rows["stl"] = ("stale", "no 04-stl/.source-hash yet, run a full `make build`")
        elif HASH_FILE.read_text().strip() != source_hash():
            rows["stl"] = ("stale", ".scad sources changed since the last full build (04-stl/.source-hash)")
        elif failed:
            rows["stl"] = ("stale", f"failed: {', '.join(failed)}")
        elif not table:
            rows["stl"] = ("stale", "no verification table")
    rows["print test"] = (("needs-you", f"open: {', '.join(open_)}") if open_ else ("done", "no open ACs"))

    m = re.search(r"^\|\s*2\. Specification\s*\|[^|]*\|[^|]*?v([\d.]+\d)", text(README), re.M)
    if v and (m is None or m.group(1) != v):
        rows["readme"] = ("warn", f"status table says v{m.group(1) if m else '?'}, approved spec is v{v}")
    else:
        rows["readme"] = ("done", "status table current")
    return rows


def main(argv):
    if argv[:1] == ["--hash"]:
        print(source_hash())
        return 0
    rows = evaluate()
    if argv[:1] == ["--check"]:
        stale = [s for s, (state, _) in rows.items() if state == "stale"]
        for s in stale:
            print(f"status: {s} is stale: {rows[s][1]} (run {SKILL[s]})", file=sys.stderr)
        return 1 if stale else 0
    if argv[:1] == ["--require"] and len(argv) == 2:
        upto = ORDER[: ORDER.index(argv[1]) + 1]
        missing = [s for s in upto if rows[s][0] != "done"]
        for s in missing:
            print(f"status: {s} is {rows[s][0]}: {rows[s][1]}", file=sys.stderr)
        return 1 if missing else 0
    if argv[:1] == ["--next"]:
        nxt = next((s for s in ORDER if rows[s][0] != "done"), None)
        if nxt in HEADLESS and rows[nxt][0] == "stale":
            print(nxt)
        return 0
    if argv:
        print(__doc__, file=sys.stderr)
        return 2
    for stage, (state, detail) in rows.items():
        hint = f"  → {SKILL[stage]}" if state in ("stale", "needs-you", "warn") else ""
        print(f"{stage:13s} {state:10s} {detail}{hint}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
