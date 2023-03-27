import inspect
import sys
import xmltodict
from pprint import pprint as pp
import yaml
import util_dataclasses
from util_dataclasses import *

FILE_NAMES = {"active": "lobbyactivity-active.xml", "closed": "lobbyactivity-closed.xml"}

def parse_xml(document: dict):
    assert list(document['ROWSET'].keys()) == ['ROW'], f"ROWSET should have only one key 'ROW'. Actual keys: {list(document['ROWSET'].keys())}"

    for ROW in document['ROWSET']['ROW']:
        assert set(ROW.keys()) == {'SMXML'}, f"ROW should have only one key 'SMXML'. Actual keys: {list(ROW.keys())}"
        assert set(ROW['SMXML'].keys()) == {'SM'}, f"SMXML should have only one key 'SM'. Actual keys: {list(ROW['SMXML'].keys())}"
        assert set(ROW['SMXML']['SM'].keys()).issuperset({'SMNumber','Status','Type','SubjectMatter','Particulars','InitialApprovalDate','EffectiveDate','ProposedStartDate','ProposedEndDate'})

        if 'GMTFUNDINGS' in ROW['SMXML']['SM']:
            ROW['SMXML']['SM']['Gmtfundings'] = ROW['SMXML']['SM']['GMTFUNDINGS']
            del ROW['SMXML']['SM']['GMTFUNDINGS']

        subjectMatter = SubjectMatter(**ROW['SMXML']['SM'])
        subjectMatter.SubjectMatter = list(val if len(val.replace(":",",").split(','))==1 else list(val.replace(":",",").split(',')) for val in list(subjectMatter.SubjectMatter.split(";")))
        

        subjectMatter.Registrant = Registrant(**subjectMatter.Registrant)
        subjectMatter.Registrant.BusinessAddress = BusinessAddress(**subjectMatter.Registrant.BusinessAddress)
        
        if subjectMatter.Communications:
            if type(subjectMatter.Communications['Communication']) == dict:
                subjectMatter.Communications = [Communication(**subjectMatter.Communications['Communication'])]
            else:
                subjectMatter.Communications = [Communication(**communication) for communication in subjectMatter.Communications['Communication']]
            for communication in subjectMatter.Communications:
                communication.LobbyistBusinessAddress = BusinessAddress(**communication.LobbyistBusinessAddress)
        
        if type(subjectMatter.Firms['Firm']) == dict:
            subjectMatter.Firms = [Firm(**subjectMatter.Firms['Firm'])]
        else:
            subjectMatter.Firms = [Firm(**firm) for firm in subjectMatter.Firms['Firm']]
        for firm in subjectMatter.Firms:
            firm.BusinessAddress = BusinessAddress(**firm.BusinessAddress)

        if subjectMatter.Grassroots:
            if type(subjectMatter.Grassroots["GRASSROOT"]) == dict:
                subjectMatter.Grassroots = [Grassroot(**subjectMatter.Grassroots["GRASSROOT"])]
            else:
                subjectMatter.Grassroots = [Grassroot(**grassroot) for grassroot in subjectMatter.Grassroots["GRASSROOT"]]
        
        if subjectMatter.Beneficiaries:
            if type(subjectMatter.Beneficiaries["BENEFICIARY"]) == dict:
                subjectMatter.Beneficiaries = [Beneficiary(**subjectMatter.Beneficiaries["BENEFICIARY"])]
            else:
                subjectMatter.Beneficiaries = [Beneficiary(**beneficiary) for beneficiary in subjectMatter.Beneficiaries["BENEFICIARY"]]
            for beneficiary in subjectMatter.Beneficiaries:
                beneficiary.BusinessAddress = BusinessAddress(**beneficiary.BusinessAddress)

        if subjectMatter.Privatefundings:
            if type(subjectMatter.Privatefundings["Privatefunding"]) == dict:
                subjectMatter.Privatefundings = [Privatefunding(**subjectMatter.Privatefundings["Privatefunding"])]
            else:
                subjectMatter.Privatefundings = [Privatefunding(**privatefunding) for privatefunding in subjectMatter.Privatefundings["Privatefunding"]]
            
        if subjectMatter.Gmtfundings:
            key = tuple(subjectMatter.Gmtfundings.keys())[0]
            if type(subjectMatter.Gmtfundings[key]) == dict:
                subjectMatter.Gmtfundings = [Gmtfunding(**subjectMatter.Gmtfundings[key])]
            else:
                subjectMatter.Gmtfundings = [Gmtfunding(**gmtfunding) for gmtfunding in subjectMatter.Gmtfundings[key]]

        if subjectMatter.Meetings:
            if type(subjectMatter.Meetings['Meeting']) == dict:
                subjectMatter.Meetings = [Meeting(**subjectMatter.Meetings['Meeting'])]
            else:
                subjectMatter.Meetings = [Meeting(**meeting) for meeting in subjectMatter.Meetings['Meeting']]
            
            for meeting in subjectMatter.Meetings:
                if meeting.POHS:
                    if type(meeting.POHS['POH']) == dict:
                        meeting.POHS = [POH(**meeting.POHS['POH'])]
                    else:
                        meeting.POHS = [POH(**poh) for poh in meeting.POHS['POH']]
                
                if meeting.Lobbyists:
                    if type(meeting.Lobbyists['Lobbyist']) == dict:
                        meeting.Lobbyists = [Lobbyist(**meeting.Lobbyists['Lobbyist'])]
                    else:
                        meeting.Lobbyists = [Lobbyist(**lobbyist) for lobbyist in meeting.Lobbyists['Lobbyist']]

        results.append(subjectMatter)
    return results

def add_yaml_representers():
    clsmembers = inspect.getmembers(sys.modules[util_dataclasses.__name__], inspect.isclass)

    for val in clsmembers:
        def _representer(dumper, data):
            return dumper.represent_dict({key:val for key,val in data.__dict__.items() if val is not None and val })

        yaml.add_representer(val[1], _representer)

results = []
for key,value in FILE_NAMES.items():
    with open (value, "rb") as file:
        document = xmltodict.parse(file, dict_constructor=dict)
        results += parse_xml(document)
        print(f"Now {value} processed")

add_yaml_representers()

results = results
results = {"SubjectMaters":results}
print(f"Parsed {len(results['SubjectMaters'])} records")

print("Create YAML _representer() ...")

print("Dumping to YAML ...")

class CNoAliasDumper(yaml.CDumper):
    def ignore_aliases(self, data):
        return True
    

dump = yaml.dump(results, default_flow_style=False, Dumper=CNoAliasDumper, sort_keys=False)

with open("lobbyactivity3.yaml", "w") as file:
    file.write(dump)

print("Done")
