from lobby import parser, downloader
import pprint as pp
import json

lobbyactivity_xml = downloader.Downloader().download_lobbyactivity_xml()
results = parser.Parse(lobbyactivity_xml).get_results_json()
print(f"{len(results)} SubjectMatters found")

sample_results = {}

for satus in ["Active","Closed"]:
    count=3
    for result in results:
        if result['Status'] == satus:
            sample_results[result['SMNumber']] = result
            count-=1
            if count == 0: break

for collection in ["Firms","Communications","Grassroots","Beneficiaries","Privatefundings","Gmtfundings","Meetings"]:
    count=3
    for result in results:
        if result[collection] is None or len(result[collection])==0:
            sample_results[result['SMNumber']] = result
            count-=1
            if count == 0: break

    count=3
    for result in results:
        if result[collection] is not None and len(result[collection])==1:
            sample_results[result['SMNumber']] = result
            count-=1
            if count == 0: break

    count=3
    for result in results:
        if result[collection] is not None and len(result[collection])>1:
            sample_results[result['SMNumber']] = result
            count-=1
            if count == 0: break

sample_results = list(sample_results.values())

print(f"Sample results:{len(sample_results)}")
with open('lobbyactivity.json', 'w') as outfile:
    json.dump(sample_results, outfile)

