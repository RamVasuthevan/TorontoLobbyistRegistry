from lobby import parser, downloader
import pprint as pp
import json

result = downloader.Downloader().extract_files()
pp.pprint(result)