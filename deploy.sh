#!/bin/bash

# Check if Vercel CLI is available
if ! command -v vercel &> /dev/null; then
    echo "Vercel CLI not found, using token-based deployment"
    DEPLOY_CMD="datasette publish vercel --token $VERCEL_TOKEN"
else
    vercel --version
    DEPLOY_CMD="datasette publish vercel"
fi

# Add deployment options
DEPLOY_CMD="$DEPLOY_CMD lobbyist_registry.db --project=toronto-lobbyist-registry --metadata=metadata.yml --template-dir=templates --install datasette-search-all"

# Check if --no-prod flag is passed
if [[ "$1" == "--no-prod" ]]; then
    DEPLOY_CMD="$DEPLOY_CMD --no-prod"
fi

# Execute the deployment command
eval $DEPLOY_CMD