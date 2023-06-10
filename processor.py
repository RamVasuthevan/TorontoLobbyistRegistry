from typing import List,Dict
import os
import xmltodict
import time
import pprint
from app import db as app_db
from app.models import LobbyingReport, LobbyingReportStatus, LobbyingReportType, Registrant, RegistrantStatus, RegistrantType, get_enum_error_message, Prefix
from datetime import datetime, date
from enum import Enum


DATA_PATH = 'data'
DATA_FILES = ['lobbyactivity-active.xml','lobbyactivity-closed.xml']



def xml_to_dict(data_file: str) -> Dict:
    with open(os.path.join(DATA_PATH, data_file)) as fd:
        return xmltodict.parse(fd.read())

def setup_db(db):
    db.drop_all()  # Delete all tables in the database
    db.create_all()  # Create all tables in the database
    return db

def get_rows(file_dict: Dict)->List[Dict]:
    rows = [val['SMXML']['SM'] for val in  file_dict['ROWSET']['ROW']]
    return rows

def process_lobbying_report(row: Dict, db):
    smnumber = row['SMNumber']
    status = LobbyingReportStatus(row['Status'])
    _type = LobbyingReportType(row['Type'])
    subject_matter = row['SubjectMatter']
    particulars = row['Particulars']
    proposed_start_date = datetime.strptime(row['ProposedStartDate'], '%Y-%m-%d').date() if row.get('ProposedStartDate', None) is not None else None
    proposed_end_date = datetime.strptime(row['ProposedEndDate'], '%Y-%m-%d').date() if row.get('ProposedEndDate', None) is not None else None
    initial_approval_date = datetime.strptime(row['InitialApprovalDate'], '%Y-%m-%d').date()
    effective_date = datetime.strptime(row['EffectiveDate'], '%Y-%m-%d').date()
    registrant = process_registrant(row['Registrant'],db)

    try:
        report = LobbyingReport(
            smnumber=smnumber,
            status=status,
            type=_type,
            subject_matter=subject_matter,
            particulars=particulars,
            proposed_start_date=proposed_start_date,
            proposed_end_date=proposed_end_date,
            initial_approval_date=initial_approval_date,
            effective_date=effective_date,
            registrant=registrant
        )
    except Exception as e:
        pprint.pprint(row)
        raise e
    db.session.add(report)

def process_prefix(raw_prefix: str) -> Prefix:
    if raw_prefix is None:
        return None
    prefix = raw_prefix.strip().lower().replace('.', '').replace(',', '')
    try:
        return Prefix[prefix.upper()]
    except KeyError:
        #print(raw_prefix)
        #raise ValueError(get_enum_error_message("raw_prefix", Prefix, raw_prefix))
        pass
    return Prefix.ERROR
    

def process_registrant(registrant_dict,db):
    REGISTRANT_WITH_INCONSISTENT  = {
    "25883S", "19633S", "11191S", "16466S", "12186S", "16806S", "25611S", "21295S",
    "19441S", "33945S", "12077S", "12322S", "11382S", "10877S", "12889S", "13289S",
    "23257S", "12642S", "17586S", "24174S", "11215S", "13476S", "14775S", "12021S"
    }

    if registrant_dict['RegistrationNUmber'] in REGISTRANT_WITH_INCONSISTENT:
         return Registrant(
            registration_number="00000S",
            status=RegistrantStatus.SUPERSEDED,
            effective_date=date.fromisoformat('1970-01-01'),
            type=RegistrantType.CONSULTANT,
            prefix=Prefix.MR,
            first_name="ERROR",
            middle_initial=None,
            last_name="ERROR"
        )
    
    registration_number = registrant_dict['RegistrationNUmber']
    #print(registrant_dict['RegistrationNUmberWithSoNum'])
    status = RegistrantStatus(registrant_dict['Status'])
    effective_date = datetime.strptime(registrant_dict['EffectiveDate'] , '%Y-%m-%d').date() if registrant_dict.get('EffectiveDate', None) is not None else None
    _type = RegistrantType(registrant_dict['Type'])
    prefix = process_prefix(registrant_dict['Prefix'])
    first_name = registrant_dict['FirstName']
    middle_initial = registrant_dict['MiddleInitials']
    last_name = registrant_dict['LastName']
    suffix = registrant_dict['Suffix']

    try:
        registrant = Registrant(registration_number=registration_number,status=status,effective_date=effective_date,type=_type,prefix=prefix, first_name=first_name,middle_initial=middle_initial,last_name=last_name,suffix=suffix)
    except Exception as e:
        pprint.pprint(registrant_dict)
        raise e
    db.session.add(registrant)
    return registrant


from app import app, db 

def run():
    with app.app_context():
        db = setup_db(app_db)
        for data_file in DATA_FILES:
            start_time = time.time()
            for row in get_rows(xml_to_dict(data_file)):
                process_lobbying_report(row, db)
            db.session.commit()
            end_time = time.time()
            print(f"Processing time for {data_file}: {end_time - start_time} seconds")

if __name__ == '__main__':
    run()
