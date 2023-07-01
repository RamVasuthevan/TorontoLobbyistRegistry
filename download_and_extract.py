from lobby import *
import pprint as pp
import json
from lobby.downloader import Downloader


print("Starting Lobbyist Registry Downloader")
Downloader().extract_files()
print("Finished Lobbyist Registry Downloader")
