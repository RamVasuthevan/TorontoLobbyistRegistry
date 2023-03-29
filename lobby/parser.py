import inspect
import sys
import xmltodict
import yaml
from .util import *
from functools import cache
import dataclasses

class Parse:
    
    def __init__(self,lobbyactivity_xml):
        self.lobbyactivity_xml_documents = lobbyactivity_xml

    @staticmethod
    def parse_doument_xml(document: dict)->List[SubjectMatter]:
        assert list(document['ROWSET'].keys()) == ['ROW'], f"ROWSET should have only one key 'ROW'. Actual keys: {list(document['ROWSET'].keys())}"

        results = []
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

    @cache
    def get_results_dataclasses(self):
        results = []
        for file_name,zipfile in self.lobbyactivity_xml_documents.items():
            document = xmltodict.parse(zipfile, dict_constructor=dict)
            results += self.parse_doument_xml(document)
        return results

    def _add_yaml_representers(self):
        clsmembers = inspect.getmembers(sys.modules[util.__name__], inspect.isclass)

        for val in clsmembers:
            def _representer(dumper, data):
                return dumper.represent_dict({key:val for key,val in data.__dict__.items() if val is not None and val })

            yaml.add_representer(val[1], _representer)
    
    class _CNoAliasDumper(yaml.CDumper):
        def ignore_aliases(self, data):
            return True    

    @cache
    def get_results_yaml(self):
        self._add_yaml_representers()
        data = {"SubjectMaters":self.get_results_json()}
        return yaml.dump(data, default_flow_style=False, Dumper=self._CNoAliasDumper, sort_keys=False)

    @cache
    def get_results_json(self):
        return [dataclasses.asdict(result) for result in self.get_results_dataclasses()]