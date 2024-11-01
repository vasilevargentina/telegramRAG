#!/bin/bash
set -e

# Add the current directory to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/app"

# Run database migrations using alembic directly
echo "Running database migrations..."
alembic upgrade head

# Start the bot
echo "Starting the bot..."
exec python -m src.main