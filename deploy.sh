#!/bin/bash

# Function to ask for confirmation
confirm() {
    while true; do
        read -p "Are you sure you want to push to prod? (y/n): " yn
        case $yn in
            [Yy]* ) return 0;;
            [Nn]* ) echo "Aborting."; exit 1;;
            * ) echo "Please answer yes or no.";;
        esac
    done
}

# Initialize flags
prod_flag=false
yes_flag=false

# Parse arguments
for arg in "$@"; do
    case $arg in
        --prod)
            prod_flag=true
            ;;
        --yes)
            yes_flag=true
            ;;
    esac
done

# If --prod is passed
if [ "$prod_flag" = true ]; then
  # If --yes is not passed, ask for confirmation
  if [ "$yes_flag" = false ]; then
    confirm
  fi
  
  # Run the command without --no-prod
  datasette publish vercel lobbyist_registry.db --project=toronto-lobbyist-registry --metadata=metadata.yml --template-dir=templates --install datasette-search-all
else
  # Run the command with --no-prod
  datasette publish vercel lobbyist_registry.db --project=toronto-lobbyist-registry --metadata=metadata.yml --template-dir=templates --install datasette-search-all --no-prod --public
fi
