import json
import requests
import zipfile
from io import BytesIO
from typing import Dict
from pprint import pprint


LOBBY_ACTIVITY_FILE_NAME = "Lobbyist Registry Activity.zip"
README_FILE_NAME = "lobbyist-registry-readme.xls"

def get_package()-> Dict:
        """Returns response from Toronto Open Data CKAN API"""

        # Toronto Open Data is stored in a CKAN instance. It's APIs are documented here:
        # https://docs.ckan.org/en/latest/api/

        # To hit our API, you'll be making requests to:
        BASE_URL = "https://ckan0.cf.opendata.inter.prod-toronto.ca"

        # Datasets are called "packages". Each package can contain many "resources"
        # To retrieve the metadata for this package and its resources, use the package name in this page's URL:
        URL = BASE_URL + "/api/3/action/package_show"
        ID = "lobbyist-registry"

        params = {"id": ID}
        package = requests.get(URL, params=params).json()

        return package

if __name__ == "__main__":
    package = get_package()
    pprint(package)

    with open("open-data-response.json", "w") as json_file:
        json_file.write(json.dumps(package, indent=4))
    
    resource_response = {}
    for resource in package["result"]["resources"]:
        resource_response[f"{resource['name']}.{resource['format'].lower()}"] =  requests.get(resource["url"])
    
    for resource,response in resource_response.items():
        with open(resource, "wb") as f:
            f.write(response.content)
    
    lobbyactivity_zip = zipfile.ZipFile(BytesIO(resource_response[LOBBY_ACTIVITY_FILE_NAME].content))
    lobbyactivity_zip.extractall()
        
        