#!/bin/bash
set -e

# Run database migrations using alembic directly
echo "Running database migrations..."
alembic upgrade head

# Start the bot
echo "Starting the bot..."
exec python -m src.main