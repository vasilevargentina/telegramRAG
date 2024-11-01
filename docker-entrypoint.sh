#!/bin/bash
set -e

# Run database migrations
echo "Running database migrations..."
python -m alembic upgrade head

# Start the bot
echo "Starting the bot..."
exec python -m src.main 