#!/usr/bin/env bash
# Renders every printable part to 04-stl/ and PNG previews to 04-stl/previews/.
# Usage: tools/build.sh [part ...]     (default: all parts in PARTS + assembly previews; non-printable parts get previews only)
set -euo pipefail
cd "$(dirname "$0")/.."

SRC=03-openscad/brewberrypi-case.scad
PARTS=(body divider top_lid bottom_lid)   # printable parts; keep in sync with the `part` selector
OUT=04-stl
PREV=$OUT/previews
mkdir -p "$PREV"

# PNG export needs an OpenGL context. Use a virtual display when none exists.
RUN=(); [[ -z "${DISPLAY:-}" ]] && command -v xvfb-run >/dev/null && RUN=(xvfb-run -a)

# name:camera (gimbal rotx,roty,rotz) and projection
VIEWS=("iso:55,0,325:p" "iso-back:55,0,145:p" "top:0,0,0:o" "front:90,0,0:o")

render_previews() {   # $1 = part name
    for v in "${VIEWS[@]}"; do
        IFS=: read -r name rot proj <<<"$v"
        "${RUN[@]}" openscad -q -D "part=\"$1\"" --camera="0,0,0,$rot,0" --viewall --autocenter \
            --projection="$proj" --imgsize=1200,900 --colorscheme=Tomorrow \
            -o "$PREV/$1-$name.png" "$SRC"
    done
}

if [[ $# -gt 0 ]]; then targets=("$@"); else targets=("${PARTS[@]}"); fi
for p in "${targets[@]}"; do
    echo "build: $p"
    if [[ " ${PARTS[*]} " == *" $p "* ]]; then       # STLs only for printable parts; e.g. `assembly` = previews only
        openscad -q -D "part=\"$p\"" --export-format binstl -o "$OUT/brewberrypi-case-$p.stl" "$SRC"
    fi
    render_previews "$p"
done
[[ $# -eq 0 ]] && { echo "build: assembly previews"; render_previews assembly; }
echo "build: done → $OUT/"
