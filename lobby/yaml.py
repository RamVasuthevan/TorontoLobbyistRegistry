import inspect
import sys
import xmltodict
from pprint import pprint as pp
import yaml
import util_dataclasses
from util_dataclasses import *


def add_yaml_representers():
    clsmembers = inspect.getmembers(sys.modules[util_dataclasses.__name__], inspect.isclass)

    for val in clsmembers:
        def _representer(dumper, data):
            return dumper.represent_dict({key:val for key,val in data.__dict__.items() if val is not None and val })

        yaml.add_representer(val[1], _representer)

class CNoAliasDumper(yaml.CDumper):
    def ignore_aliases(self, data):
        return True    

def dump(documents: list[SubjectMatter]):
    add_yaml_representers()
    data = {"SubjectMaters":documents}
    return yaml.dump(data, default_flow_style=False, Dumper=CNoAliasDumper, sort_keys=False)