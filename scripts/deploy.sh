#!/bin/bash
set -e

# Run migrations first
docker-compose --profile migrations up migrations --exit-code-from migrations

# If migrations successful, start the bot
docker-compose up -d bot 