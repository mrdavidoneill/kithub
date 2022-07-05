#/bin/bash

# Get an unique venv folder to using *inside* workspace
VENV=".venv-$BUILD_NUMBER"

# Initialize new venv
virtualenv "$VENV"

# Update pip
PS1="${PS1:-}" source "$VENV/bin/activate"

#!/bin/sh
pip install -r requirements.txt

if [ -d "logs" ] 
then
    echo "Log folder exists." 
else
    mkdir logs
    touch logs/error.log logs/access.log
fi

sudo chmod -R 777 logs