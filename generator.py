
import json
from sqlalchemy.orm import class_mapper
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import joinedload, Load

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import backref
from sqlalchemy.orm import Mapped
from sqlalchemy import Table

import pprint as pp
import json
from typing import List, Dict, Any, Union, Optional
from lobby import downloader, parser
from itertools import chain

from uploader import *

import os

engine = create_engine("sqlite:///TorontoLobbyistRegistry.db", echo=False, future=True)

class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for prop in class_mapper(obj.__class__).iterate_properties:
                field = prop.key
                data = obj.__getattribute__(field)
                try:
                    if hasattr(data, '__iter__') and not isinstance(data, str):
                        data = [self.default(item) for item in data]
                    else:
                        json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            return fields
        return json.JSONEncoder.default(self, obj)



import yaml
from sqlalchemy.orm import selectinload
import json



from sqlalchemy.orm import class_mapper
from sqlalchemy.ext.declarative import DeclarativeMeta

def object_to_dict(obj):
    if isinstance(obj.__class__, DeclarativeMeta):
        fields = {}
        for prop in class_mapper(obj.__class__).iterate_properties:
            field = prop.key
            if field == '_sa_instance_state':  # Ignore the _sa_instance_state field
                continue
            data = getattr(obj, field)
            if isinstance(data, (int, float, str, bool, type(None))):
                fields[field] = data
            elif isinstance(data.__class__, DeclarativeMeta):
                fields[field] = object_to_dict(data)
            elif hasattr(data, '__iter__') and not isinstance(data, str):
                fields[field] = [object_to_dict(item) for item in data if isinstance(item.__class__, DeclarativeMeta)]
        return fields
    return None




        
def SubjectMatterPage(subjectmatter:SubjectMatter):
    result = {}
    result['SMNumber'] = subjectmatter.SMNumber
    result['Status'] = subjectmatter.status.Status
    #result['Type'] = subjectmatter.Type.Type
    result['SubjectMatterGroups'] = [group.SubjectMatterGroup.Group for group in subjectmatter.SubjectMatterGroups]
    result['Definition'] = subjectmatter.SubjectMatterDefinition.Definition
    result['Particulars'] = subjectmatter.Particulars
    
    result['Registrant'] = {}
    result['Registrant']['RegistrationNUmber'] = subjectmatter.Registrant.RegistrationNUmber
    result['Registrant']['Type'] = subjectmatter.Registrant.Type
    result['Registrant']['Prefix'] = subjectmatter.Registrant.Prefix
    result['Registrant']['FirstName'] = subjectmatter.Registrant.FirstName
    result['Registrant']['MiddleInitials'] = subjectmatter.Registrant.MiddleInitials
    result['Registrant']['LastName'] = subjectmatter.Registrant.LastName
    result['Registrant']['Suffix'] = subjectmatter.Registrant.Suffix
    result['Registrant']['PositionTitle'] = subjectmatter.Registrant.PositionTitle

    result['Firms'] = []

    for subjectMatterToCommunication in subjectMatter.Communications:
        communication = subjectMatterToCommunication.Communication
        result['Communications'].append({})

    
    for subjectMatterToFirm in subjectmatter.Firms:
        firm = subjectMatterToFirm.Firm
        result['Firms'].append({})
        result['Firms'][-1]['Type'] = firm.Type.Type
        result['Firms'][-1]['Name'] = firm.Name
        result['Firms'][-1]['TradeName'] = firm.TradeName
        result['Firms'][-1]['Description'] = firm.Description
        result['Firms'][-1]['BusinessType'] = firm.BusinessType.Type
        result['Firms'][-1]['BusinessAddress'] = {}
        if firm.BusinessAddress:
            result['Firms'][-1]['BusinessAddress']['AddressLine1'] = firm.BusinessAddress.AddressLine1
            result['Firms'][-1]['BusinessAddress']['AddressLine2'] = firm.BusinessAddress.AddressLine2
            result['Firms'][-1]['BusinessAddress']['City'] = firm.BusinessAddress.City
            result['Firms'][-1]['BusinessAddress']['Province'] = firm.BusinessAddress.Province
            result['Firms'][-1]['BusinessAddress']['Country'] = firm.BusinessAddress.Country
            result['Firms'][-1]['BusinessAddress']['PostalCode'] = firm.BusinessAddress.PostalCode
            result['Firms'][-1]['BusinessAddress']['Phone'] = firm.BusinessAddress.Phone
    
    for subjectMatterToBeneficiary in subjectmatter.Beneficiaries:
        beneficiary = subjectMatterToBeneficiary.Beneficiary
        result['Beneficiaries'].append({})
        result['Beneficiaries'][-1]['Type'] = beneficiary.Type.Type
        result['Beneficiaries'][-1]['Name'] = beneficiary.Name
        result['Beneficiaries'][-1]['TradeName'] = beneficiary.TradeName
        if beneficiary.BusinessAddress:
            result['Beneficiaries'][-1]['BusinessAddress']['AddressLine1'] = firm.BusinessAddress.AddressLine1
            result['Beneficiaries'][-1]['BusinessAddress']['AddressLine2'] = firm.BusinessAddress.AddressLine2
            result['Beneficiaries'][-1]['BusinessAddress']['City'] = firm.BusinessAddress.City
            result['Beneficiaries'][-1]['BusinessAddress']['Province'] = firm.BusinessAddress.Province
            result['Beneficiaries'][-1]['BusinessAddress']['Country'] = firm.BusinessAddress.Country
            result['Beneficiaries'][-1]['BusinessAddress']['PostalCode'] = firm.BusinessAddress.PostalCode
            result['Beneficiaries'][-1]['BusinessAddress']['Phone'] = firm.BusinessAddress.Phone
    

    return result

def sqlalchemy_object_representer(dumper, obj):
    return dumper.represent_mapping('tag:yaml.org,2002:map', object_to_dict(obj))

yaml.SafeDumper.add_multi_representer(DeclarativeMeta, sqlalchemy_object_representer)

print('start')
with Session(engine) as session:
    results = session.query(SubjectMatter).options(selectinload('*')).limit(10).all()
    for val in results:
        print(val.SMNumber)
        with open(val.SMNumber + '.yaml', 'w') as outfile:
            yaml.dump(SubjectMatterPage(val), outfile, sort_keys=False, Dumper=yaml.SafeDumper, default_flow_style=False)    

print('end')