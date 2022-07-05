#!/bin/bash
set -euo pipefail

# Get the unique venv folder using *inside* workspace
VENV=".venv-$BUILD_NUMBER"

# Activate virtual environment
source "$VENV/bin/activate"

./manage.py test kithub.api.tests.unit