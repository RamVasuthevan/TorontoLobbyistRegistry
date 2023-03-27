from lobby import parser, downloader
import inspect
import sys
import xmltodict
import pprint as pp
import yaml

lobbyactivity_xml = downloader.Downloader().download_lobbyactivity_xml()
results = parser.Parse(lobbyactivity_xml).get_results_json()
print(len(results))

