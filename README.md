# TorontoLobbyistRegistry


# Downloader
- Downloader is a class that contains methods to download the lobbyist registry and readme files from the Toronto Open Data CKAN API.

# LobbyParser
- Parse the lobbyist registry xml files into Dataclasses

# Uploader
- Generates db based on data from the Downloader and Parser
- Calls Downloader and Parser
- Needs to be refactored
    - Deletes TorontoLobbyistRegistry.db
    - Creates TorontoLobbyistRegistry.db
    - TorontoLobbyistRegistry.db hard coded in
    - Called Downloader and Parser
    - Need to be able to given existing zip file
# Generator
- Generates zip file of yaml files for Jekyll

# Util
- Dataclasses for LobbyParser


