#!/usr/bin/env bash
# Mesh sanity check for every STL in 04-stl/: facet count, problems admesh had to repair, bounding box.
# Read-only: admesh is run without write options, so files are not modified.
# Exits non-zero if any mesh needed repairs (= not cleanly manifold).
set -euo pipefail
cd "$(dirname "$0")/.."

status=0
shopt -s nullglob
files=(04-stl/*.stl)
[[ ${#files[@]} -eq 0 ]] && { echo "check: no STL files in 04-stl/. Run tools/build.sh first."; exit 1; }

for f in "${files[@]}"; do
    report=$(admesh "$f")
    echo "== $f"
    grep -E "Min X|Min Y|Min Z|Number of facets|Number of parts|Degenerate facets|Edges fixed|Facets removed|Facets added|Backwards edges|Normals fixed" <<<"$report" | sed 's/^/   /' || true
    bad=$(grep -E "Degenerate facets|Edges fixed|Facets removed|Facets added|Backwards edges" <<<"$report" | grep -Ev ":[[:space:]]+0$" || true)
    if [[ -n "$bad" ]]; then echo "   !! mesh needed repairs"; status=1; else echo "   ok"; fi
done
exit $status
