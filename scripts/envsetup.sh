#!/bin/bash
set -euo pipefail

# Get an unique venv folder to using *inside* workspace
VENV=".venv-$BUILD_NUMBER"

# Initialize new venv
python3 -m venv "$VENV"

# Update pip
PS1="${PS1:-}" source "$VENV/bin/activate"

#!/bin/sh
pip install -r requirements.txt
