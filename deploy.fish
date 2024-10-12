#!/usr/bin/fish

set -x SERVER_IP 192.34.62.11
pipenv install
pipenv run main.py
rsync -avz --delete ./ root@$SERVER_IP:/root/TorontoLobbyistRegistry
ssh root@$SERVER_IP "systemctl restart TorontoLobbyistRegistry"
