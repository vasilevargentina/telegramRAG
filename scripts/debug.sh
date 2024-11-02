#!/bin/bash
set -e

# Run the bot with both production and debug configurations
docker-compose -f docker-compose.yml -f docker-compose.debug.yml up bot 