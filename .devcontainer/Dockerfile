# Toolchain for `make ci`. Keep the package list in sync with tools/setup.sh.
FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        make openscad xvfb xauth admesh python3 python3-pip shellcheck \
 && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir --break-system-packages ruff==0.16.9
