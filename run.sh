#!/bin/bash

# Set environment variables
export EMAIL_SENDER="tarunaditya973@gmail.com"
export EMAIL_RECIPIENTS="tarunaditya973@gmail.com"
export SMTP_HOST="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USERNAME="tarunaditya973@gmail.com"
export SMTP_PASSWORD="kold ijqa wcks iwsy"
export SMTP_USE_TLS="true"
export DEFAULT_KEYWORDS="Software,Engineer,Platform,SRE,DevOps"
export LOCATION_FILTER="Remote,Bengaluru,India"

# Run job automation
echo "🚀 Starting Job Application Automation..."
echo "📧 Email: $EMAIL_SENDER"
echo "🔍 Keywords: $DEFAULT_KEYWORDS"
echo "📍 Locations: $LOCATION_FILTER"
echo ""

# Check if dry-run flag is passed
if [ "$1" = "--dry-run" ]; then
    echo "🧪 DRY RUN MODE - No emails will be sent"
    python main.py --companies companies.yml --dry-run
else
    echo "📤 SENDING REAL EMAILS"
    python main.py --companies companies.yml
fi
