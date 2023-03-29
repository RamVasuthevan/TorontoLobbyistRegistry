from lobby import parser, downloader
import pprint as pp
import json

lobbyactivity_xml = downloader.Downloader().download_lobbyactivity_xml()
results = parser.Parse(lobbyactivity_xml).get_results_json()
print(f"{len(results)} SubjectMatters found")

with open('lobbyactivity.json', 'w') as outfile:
    json.dump(results, outfile)

