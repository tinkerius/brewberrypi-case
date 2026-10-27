# Single source of truth for building and checking the case.
# VS Code tasks (.vscode/tasks.json) and CI (.github/workflows/ci.yml) only call these targets.
#
#   make setup   toolchain + BOSL2 submodule (tools/setup.sh)
#   make build   STLs + previews into 04-stl/ (tools/build.sh)
#   make lint    shell, Python and OpenSCAD checks; spec drawings, logo outline and version stamps up to date
#   make test    mesh, overhang, label, collision and dimension checks on the STLs (tools/check.sh)
#   make ci      lint + build + test, what CI runs
#   make status  which pipeline stage is done, stale or waiting for you (tools/status.py)
#
# Claude stages (local only, not in CI; need the `claude` CLI, commit but never push):
#   make claude-scad  /scad headless: bring 03-openscad/ in line with the approved spec
#   make claude-stl   /stl headless: build, check, verify, fill in 04-stl/README.md
#   make pipeline     run whichever of the two is stale, in order, then show the status
# Requirements, spec and print feedback need you: run /requirements, /spec, /feedback in a Claude session.

SHELL := bash
.SHELLFLAGS := -euo pipefail -c
.DEFAULT_GOAL := help

SRC      := 03-openscad/brewberrypi-case.scad
SCRATCH  := scratch
# every value of the `part` selector, read from its Customizer comment
SCAD_PARTS := $(shell sed -n 's|^part *=.*// *\[\(.*\)\].*|\1|p' $(SRC) | tr -d ' ' | tr ',' ' ')

CLAUDE       ?= claude
CLAUDE_FLAGS ?= --permission-mode acceptEdits \
                --allowedTools 'Bash(make:*)' 'Bash(openscad:*)' 'Bash(python3 tools/:*)' 'Bash(tools/:*)' \
                               'Bash(git status:*)' 'Bash(git diff:*)' 'Bash(git add:*)' 'Bash(git commit:*)'

.PHONY: help setup build lint lint-sh lint-py lint-scad lint-drawings lint-logo lint-status test ci status \
        claude-scad claude-stl pipeline clean

help:
	@sed -n 's/^#   make /  make /p' $(MAKEFILE_LIST)

setup:
	tools/setup.sh

build:
	tools/build.sh

lint: lint-sh lint-py lint-scad lint-drawings lint-logo lint-status

lint-sh:
	shellcheck tools/*.sh

lint-py:
	ruff check tools/

lint-scad:   # evaluates every part; any OpenSCAD warning fails
	@mkdir -p $(SCRATCH)
	@for p in $(SCAD_PARTS); do \
	    echo "lint-scad: $$p"; \
	    openscad --hardwarnings -D "part=\"$$p\"" -o $(SCRATCH)/lint-$$p.echo $(SRC); \
	done

lint-drawings:   # drawings must match tools/make_drawings.py
	python3 tools/make_drawings.py >/dev/null
	git -c safe.directory='*' diff --exit-code --stat -- 02-specification/drawings \
	    || { echo "lint-drawings: drawings are stale, run python3 tools/make_drawings.py and commit"; exit 1; }

lint-logo:   # 03-openscad/lib/brand-logo.scad must match tools/make_logo.py and the brand file B2
	python3 tools/make_logo.py >/dev/null
	git -c safe.directory='*' diff --exit-code --stat -- 03-openscad/lib/brand-logo.scad \
	    || { echo "lint-logo: logo outline is stale, run python3 tools/make_logo.py and commit"; exit 1; }

lint-status:   # version stamps agree with the approved spec, STLs built from the current sources
	python3 tools/status.py --check

test:
	tools/check.sh

ci: lint build test

status:
	@python3 tools/status.py

claude-scad:
	python3 tools/status.py --require spec
	$(CLAUDE) -p "/scad" $(CLAUDE_FLAGS)

claude-stl:
	python3 tools/status.py --require scad
	$(CLAUDE) -p "/stl" $(CLAUDE_FLAGS)

pipeline:
	@for i in 1 2; do \
	    next=$$(python3 tools/status.py --next); \
	    if [[ -z "$$next" ]]; then break; fi; \
	    echo "pipeline: $$next is stale, running /$$next"; \
	    $(MAKE) --no-print-directory claude-$$next; \
	    if [[ "$$(python3 tools/status.py --next)" == "$$next" ]]; then \
	        echo "pipeline: $$next is still stale after /$$next"; exit 1; \
	    fi; \
	done
	@python3 tools/status.py

clean:
	rm -rf $(SCRATCH)
