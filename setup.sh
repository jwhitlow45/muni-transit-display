#!/bin/bash

# Ensure script is run as root
if (( EUID != 0 )); then
  echo "Error: This script must be run as root or with sudo." >&2
  exit 1
fi

# Install rpi-rgb-led-matrix globally - https://github.com/hzeller/rpi-rgb-led-matrix/tree/master/bindings/python
git clone https://github.com/hzeller/rpi-rgb-led-matrix
cd rpi-rgb-led-matrix
make build-python 
make install-python 
cd -

# Install uv globally and add to path
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

# Install next-transit-display dependencies globally
uv pip install --system -r pyproject.toml --break-system-packages

# Create .env from .env.example
cp .env.example .env