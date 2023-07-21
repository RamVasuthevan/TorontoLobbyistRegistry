import json
import requests
import zipfile
from io import BytesIO
from typing import Dict
from datetime import datetime

LOBBY_ACTIVITY_FILE_NAME = "Lobbyist Registry Activity.zip"
README_FILE_NAME = "lobbyist-registry-readme.xls"


class Downloader:

    def __init__(self):
        self.package = self._get_package()

    def _get_package(self) -> Dict:
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
    
    def lobbyactivity_zip(self) -> zipfile.ZipFile:
        lobbyist_data_response: requests.models.Response = requests.get(
            self.package["result"]["resources"][1]["url"]
        )
        return zipfile.ZipFile(BytesIO(lobbyist_data_response.content))

    def readme_bytes(self):
        readme_response: requests.models.Response = requests.get(
            self.package["result"]["resources"][0]["url"]
        )
        return readme_response.content


    def extract_files(self):
        lobbyist_data_response: requests.models.Response = requests.get(
            self.package["result"]["resources"][1]["url"]
        )

        # Save zip file
        with open(LOBBY_ACTIVITY_FILE_NAME, "wb") as f:
            f.write(lobbyist_data_response.content)

        # Now you have the zip file, you can create a ZipFile object from it.
        lobbyactivity_zip = zipfile.ZipFile(BytesIO(lobbyist_data_response.content))

        # Extract all files in the zip archive
        lobbyactivity_zip.extractall()

        with open(README_FILE_NAME, "wb") as binary_file:
            binary_file.write(self.readme_bytes())

        with open("open-data-response.json", "w") as json_file:
            json_file.write(json.dumps(self.package, indent=4))
