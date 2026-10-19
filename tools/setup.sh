#!/usr/bin/env bash
# Installs the toolchain: OpenSCAD, Xvfb (headless PNG previews), admesh (mesh check), BOSL2 submodule.
# Usage: tools/setup.sh          (interactive / manual)
#        tools/setup.sh --hook   (from the SessionStart hook: installs packages only in Claude Code cloud sessions)
set -euo pipefail
cd "$(dirname "$0")/.."

if [[ ! -f 03-openscad/vendor/BOSL2/std.scad ]]; then
    git submodule update --init --recursive
fi

need=()
command -v openscad >/dev/null || need+=(openscad)
command -v xvfb-run >/dev/null || need+=(xvfb xauth)
command -v admesh   >/dev/null || need+=(admesh)
[[ ${#need[@]} -eq 0 ]] && { echo "setup: toolchain present ($(openscad --version 2>&1 | head -1))"; exit 0; }

if [[ "${1:-}" == "--hook" && "${CLAUDE_CODE_REMOTE:-}" != "true" ]]; then
    echo "setup: missing ${need[*]}. Run tools/setup.sh manually (not auto-installing on a local machine)."
    exit 0
fi

SUDO=""; [[ $EUID -ne 0 ]] && SUDO="sudo"
$SUDO apt-get update -qq
DEBIAN_FRONTEND=noninteractive $SUDO apt-get install -y -qq "${need[@]}" >/dev/null
echo "setup: installed ${need[*]} ($(openscad --version 2>&1 | head -1))"
