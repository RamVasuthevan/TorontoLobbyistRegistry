import json
import requests
import zipfile
from io import BytesIO
from functools import cache
from typing import Dict
from datetime import datetime


class Downloader:
    LOBBY_ACTIVITY_FILE_NAME = "Lobbyist Registry Activity.zip"
    README_FILE_NAME = "lobbyist-registry-readme.xls"

    def __init__(self, load_from_url=True):
        self._called = False
        self.package = self._get_package()
        self.metadata_dates = self._get_metadata_metadata_dates()

    @cache
    def _get_package(self) -> Dict:
        """Returns response from Toronto Open Data CKAN API"""
        if self._called:
            raise Exception("This method should only be called once")

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

        self._called = True
        return package

    @cache
    def _get_metadata_metadata_dates(self) -> Dict[str, Dict[str, str]]:
        """Returns last modified dates for lobbying registry and readme"""
        package = self.package
        metadata_dates = {
            "package": {
                "last_refreshed": package["result"]["last_refreshed"],
                "metadata_modified": package["result"]["metadata_modified"],
            },
            "lobbyist-registry-readme": {
                "last_modified": package["result"]["resources"][0]["last_modified"],
                "metadata_modified": package["result"]["resources"][0][
                    "metadata_modified"
                ],
            },
            "lobbyist-registry": {
                "last_modified": package["result"]["resources"][1]["last_modified"],
                "metadata_modified": package["result"]["resources"][1][
                    "metadata_modified"
                ],
            },
        }
        return metadata_dates

    @cache
    def last_modified(self):
        """Returns the most recent last_modified date from the package metadata"""
        datetimes = [
            self.package["package"]["last_refreshed"],
            self.package["package"]["metadata_modified"],
            self.package["lobbyist-registry"]["last_modified"],
            self.package["lobbyist-registry"]["metadata_modified"],
            self.package["lobbyist-registry-readme"]["last_modified"],
            self.package["lobbyist-registry-readme"]["metadata_modified"],
        ]
        return max(
            datetime.strptime(
                (val.split(".")[0] if "." in val else val).replace("T", " "),
                "%Y-%m-%d %H:%M:%S",
            )
            for val in datetimes
        )

    @cache
    def lobbyactivity_zip(self) -> zipfile.ZipFile:
        lobbyist_data_response: requests.models.Response = requests.get(
            self.package["result"]["resources"][1]["url"]
        )
        return zipfile.ZipFile(BytesIO(lobbyist_data_response.content))

    @cache
    def readme_bytes(self):
        readme_response: requests.models.Response = requests.get(
            self.package["result"]["resources"][0]["url"]
        )
        return readme_response.content

    @cache
    def lobbyactivity_xml(self) -> Dict[str, zipfile.ZipExtFile]:
        return {
            memberName: self.lobbyactivity_zip().open(memberName)
            for memberName in self.lobbyactivity_zip().namelist()
        }

    @cache
    def extract_files(self):
        lobbyactivity_zip = self.lobbyactivity_zip()
        lobbyactivity_zip.extractall()
        
        with open('lobbyactivity.zip', 'wb') as f:
            f.write(lobbyactivity_zip.read())

        with open(self.README_FILE_NAME, "wb") as binary_file:
            binary_file.write(self.readme_bytes())

        with open("open-data-response.json", "w") as json_file:
            json_file.write(json.dumps(self.package, indent=4))
