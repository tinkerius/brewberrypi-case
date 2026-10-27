#!/usr/bin/env bash
# Automated checks for the STLs in 04-stl/ (spec §9):
#   AC1 bounding boxes · AC2 manifold (admesh, read-only) · AC6 overhang report · AC8 label sizes
#   AC3/AC10 collision check · AC4/AC5 dimension report from the model.
# Exits non-zero if a mesh needed repairs or the collision check is not empty.
set -euo pipefail
cd "$(dirname "$0")/.."

SRC=03-openscad/brewberrypi-case.scad
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
status=0
shopt -s nullglob
files=(04-stl/*.stl)
[[ ${#files[@]} -eq 0 ]] && { echo "check: no STL files in 04-stl/. Run tools/build.sh first."; exit 1; }

echo "### AC1 / AC2: meshes and bounding boxes"
for f in "${files[@]}"; do
    report=$(admesh "$f")
    echo "== $f"
    grep -E "Min X|Min Y|Min Z|Number of facets|Number of parts|Degenerate facets|Edges fixed|Facets removed|Facets added|Backwards edges|Normals fixed" <<<"$report" | sed 's/^/   /' || true
    bad=$(grep -E "Degenerate facets|Edges fixed|Facets removed|Facets added|Backwards edges" <<<"$report" | grep -Ev ":[[:space:]]+0$" || true)
    if [[ -n "$bad" ]]; then echo "   !! mesh needed repairs"; status=1; else echo "   ok"; fi
done

echo; echo "### AC6: overhangs steeper than 45° (print orientation, not on the bed)"
python3 tools/overhangs.py "${files[@]}"

echo; echo "### AC8: label and logo sizes (capitals ≥ 6 mm, raised 0.6 / logo 130 × 85.17 at (95, 80), raised 0.8)"
python3 tools/labels.py

echo; echo "### AC3 / AC10: collision check (must be empty)"
collision=$(openscad -D 'part="collision_check"' -o "$TMP/collision.stl" "$SRC" 2>&1 || true)   # exits 1 when empty
if grep -q "Current top level object is empty" <<<"$collision"; then
    echo "   ok: no overlaps"
else
    echo "   !! collision check is not empty: open part=collision_check in OpenSCAD"; status=1
fi

echo; echo "### AC4 / AC5: dimensions as modelled"
openscad -D 'part="top_lid"' -o "$TMP/report.stl" "$SRC" 2>&1 | grep REPORT | sed 's/^ECHO: "REPORT /   /; s/"$//'

exit $status
