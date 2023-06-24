from lobby import *
import pprint as pp
import json
import lobby.generator as generator


print("Starting Lobbyist Registry Downloader")
Downloader().extract_files()
print("Finished Lobbyist Registry Downloader")
