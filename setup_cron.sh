#!/bin/bash

echo "📅 Setting up scheduled tasks..."

# Load credentials from .env
export $(grep -v '^#' .env | xargs)

# Remove old recordings every 3 days
CRON_JOB_CLEANUP="0 3 * * * find /var/www/html/ -type f -name '*.mp4' -mtime +3 -delete"

# Restart services if they fail (runs every 5 minutes)
CRON_JOB_HEALTH_CHECK="*/5 * * * * /usr/local/bin/health_check.sh"

# Check if cron jobs already exist
(crontab -l 2>/dev/null | grep -v -F "$CRON_JOB_CLEANUP"; echo "$CRON_JOB_CLEANUP") | crontab -
(crontab -l 2>/dev/null | grep -v -F "$CRON_JOB_HEALTH_CHECK"; echo "$CRON_JOB_HEALTH_CHECK") | crontab -

echo "✅ Crontab configured successfully."
