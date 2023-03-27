import requests
import zipfile
from io import BytesIO
from functools import cache
from typing import Dict
from datetime import datetime

class Downloader:

    def __init__(self):
        self._called = False
        self.package = self._get_package()
        self.metadata = self._get_metadata()
        
    def _get_package(self):
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

        params = { "id": ID}
        package = requests.get(URL, params = params).json()

        self._called = True
        return package

    def _get_metadata(self)-> Dict[str,Dict[str,str]]:
        package = self.package
        metadata = {'package':{
                'last_refreshed':package['result']['last_refreshed'],
                'metadata_modified':package['result']['metadata_modified']},
            'lobbyist-registry-readme':{
                'last_modified':package['result']['resources'][0]['last_modified'],
                'metadata_modified':package['result']['resources'][0]['metadata_modified'],
                'url':package['result']['resources'][0]['url'],
            },
            'lobbyist-registry':{
                'last_modified':package['result']['resources'][1]['last_modified'],
                'metadata_modified':package['result']['resources'][1]['metadata_modified'],
                'url':package['result']['resources'][1]['url'],
            }
            }
        return metadata

    @cache
    def download_lobbyactivity_zip(self,url)->bytes:
        lobbyist_data = requests.get(url)
        lobbyist_data_zip = lobbyist_data.content
        return lobbyist_data_zip
    
    @cache
    def unzip_lobbyactivity_files(self,lobbyist_data_zip:bytes)->Dict[str,zipfile.ZipExtFile]:
        zf = zipfile.ZipFile(BytesIO(lobbyist_data_zip))
        return {memberName:zf.open(memberName) for memberName in zf.namelist()}

    @cache
    def download_lobbyactivity_xml(self):
        lobbyist_data_zip: bytes = self.download_lobbyactivity_zip(self.metadata['lobbyist-registry']['url'])
        self.files:Dict[str,zipfile.ZipExtFile] = self.unzip_lobbyactivity_files(lobbyist_data_zip)
        return self.files
    
    @cache
    def download_readme(self)->str:
        lobbyist_readme = requests.get(self.metadata['lobbyist-registry-readme']['url'])
        return lobbyist_readme

    @cache
    def last_modified(self):
        datetimes = [
            self.metadata['package']['last_refreshed'],
            self.metadata['package']['metadata_modified'],
            self.metadata['lobbyist-registry']['last_modified'],
            self.metadata['lobbyist-registry']['metadata_modified'],
            self.metadata['lobbyist-registry-readme']['last_modified'],
            self.metadata['lobbyist-registry-readme']['metadata_modified'],
        ]
        return max(datetime.strptime((val.split(".")[0] if "." in val else val).replace("T"," "),'%Y-%m-%d %H:%M:%S') for val in datetimes)