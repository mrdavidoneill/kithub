#!/usr/bin/env bash

# Abort on any error (including if wait-for-it fails).
set -e

# Load .env
if [ -f .env ]; then
    # Load Environment Variables
    export $(cat .env | grep -v '#' | sed 's/\r$//' | awk '/=/ {print $1}' )
fi

# Wait for the backend to be up, if we know where it is.
if [ -n $DB_HOST ]; then
  /usr/src/app/api/scripts/wait-for-it.sh "$DB_HOST:$DB_PORT" -t 30
fi

# Run the main container command.
exec "$@"
