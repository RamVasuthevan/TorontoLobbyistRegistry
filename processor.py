from typing import List,Dict
import os
import xmltodict
import time
import pprint
from app import db as app_db
from app.models import LobbyingReport, LobbyingReportStatus, LobbyingReportType, RegistrantSeniorOfficer, RegistrantStatus, RegistrantType, get_enum_error_message, PersonPrefix, Person, Address, AddressCountry, DataSource
from app.processor_models import TempRawRegistrant,RawAddress, RawRegistrant,RawCommunications
from app.processor_models import RawLobbyingReport

from datetime import datetime, date
from enum import Enum
from dataclasses import dataclass
from sqlalchemy.orm import joinedload,sessionmaker
from sqlalchemy import delete
from sqlalchemy.orm.session import make_transient
from sqlalchemy import update




DATA_PATH = 'data'

@dataclass
class Data:
    data_value: str
    source: DataSource

def xml_to_dict(data_source:DataSource) -> Dict:
    with open(os.path.join(DATA_PATH, data_source.value)) as fd:
        return xmltodict.parse(fd.read())

def setup_db(db):
    db.drop_all()  # Delete all tables in the database
    db.create_all()  # Create all tables in the database
    return db

def get_data_rows(file_dict: Dict,data_source:DataSource)->List[Data]:
    data_rows = []
    for val in file_dict['ROWSET']['ROW']:
        row = val['SMXML']['SM']
        data_rows.append(Data(data_value=row,source=data_source))

    return data_rows

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
    registrant = Registrant.query.filter_by(registration_number=row['Registrant']['RegistrationNUmberWithSoNum']).one_or_none()

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
    
    db.session.add(report)

def process_prefix(raw_prefix: str) -> PersonPrefix:
    if raw_prefix is None or raw_prefix in ['M','M.','Aubrey Dan','matt kosoy','4252222','5874595','Rakr']:
        return None
    elif raw_prefix in ["Mr.M","MrM."]:
        prefix = "mr"
    else:
        prefix = raw_prefix.strip().lower().replace('.', '').replace(',', '')

    try:
        return PersonPrefix[prefix.upper()]
    except KeyError: 
        raise ValueError(get_enum_error_message("raw_prefix", PersonPrefix, raw_prefix))
    #return PersonPrefix.ERROR
    
def process_person(raw_prefix:str, first_name:str, middle_initial:str, last_name:str, suffix:str,position_title:str)->Person:
    prefix = process_prefix(raw_prefix)

    person = Person.query.filter_by(
        prefix=prefix, 
        first_name=first_name, 
        middle_initial=middle_initial, 
        last_name=last_name, 
        suffix=suffix
    ).one_or_none()

    if person is not None:
        if position_title not in person.position_titles: # ToDo Clean up O(N) operation
            person.position_titles.append(position_title)
    else:
        try:
            person = Person(
                prefix=prefix, 
                first_name=first_name, 
                middle_initial=middle_initial, 
                last_name=last_name, 
                suffix=suffix,
                position_titles=[position_title]
            )
        except ValueError as e:
            raise e
        db.session.add(person)

    return person

def process_address_country(raw_country: str) -> AddressCountry:
    country_mapping = {e.value: e for e in AddressCountry}

    raw_country = raw_country.lower()
    if raw_country in ["canadá","canda","can","canad","ca"]:
        return country_mapping["Canada"]
    elif raw_country in ["United States","united-states","usa","us","u.s.a.","united states of america"]:
        return country_mapping["United States"]
    elif raw_country in ["nederland", "the netherlands"]:
        return country_mapping["Netherlands"]
    else:
        for key, value in country_mapping.items():
            if key.lower() == raw_country:
                return value
    
    if raw_country in ['toronto']:
        return AddressCountry.Error

    raise ValueError(get_enum_error_message("country",AddressCountry,raw_country))

def process_address(address_dict, db):
    address_line1 = address_dict['AddressLine1']
    address_line2 = address_dict['AddressLine2']
    city = address_dict['City']
    province = address_dict['Province']
    country = process_address_country(address_dict['Country'])
    postal_code = address_dict['PostalCode']
    phone = address_dict['Phone']

    address = db.session.query(Address).filter_by(
        address_line1=address_line1,
        address_line2=address_line2,
        city=city,
        province=province,
        country=country,
        postal_code=postal_code,
        phone=phone
    ).one_or_none()

    if address:
        return address
    else:
        try:
            address = Address(
                address_line1=address_line1,
                address_line2=address_line2,
                city=city,
                province=province,
                country=country,
                postal_code=postal_code,
                phone=phone
            )
        except ValueError as e:
            print(address_dict)
            raise e

        db.session.add(address)
        db.session.commit()

        return address

def process_registrant_old(registrant_dict, db):
    REGISTRANT_WITH_INCONSISTENT = {
        "25883S", "19633S", "11191S", "16466S", "12186S", "16806S", "25611S", "21295S",
        "19441S", "33945S", "12077S", "12322S", "11382S", "10877S", "12889S", "13289S",
        "23257S", "12642S", "17586S", "24174S", "11215S", "13476S", "14775S", "12021S"
    }

    if registrant_dict['RegistrationNUmber'] in REGISTRANT_WITH_INCONSISTENT:
        return None

    registration_number = registrant_dict['RegistrationNUmber']
    registration_number_with_senior_officer_number = registrant_dict['RegistrationNUmberWithSoNum']
    status = RegistrantStatus(registrant_dict['Status'])
    effective_date = datetime.strptime(registrant_dict['EffectiveDate'], '%Y-%m-%d').date() \
        if registrant_dict.get('EffectiveDate', None) is not None else None
    _type = RegistrantType(registrant_dict['Type'])
    
    

    prefix = registrant_dict['Prefix']
    first_name = registrant_dict['FirstName']
    middle_initial = registrant_dict['MiddleInitials']
    last_name = registrant_dict['LastName']
    suffix = registrant_dict['Suffix']
    position_title = registrant_dict['PositionTitle']
    person = process_person(prefix, first_name, middle_initial, last_name, suffix,position_title)

    address = process_address(registrant_dict['BusinessAddress'],db)

    registrant = Registrant.query.filter_by(
        registration_number=registration_number,
        registration_number_with_senior_officer_number=registration_number_with_senior_officer_number, address=address
    ).one_or_none()
    #print(address)
    #if registrant is not None and registrant.address.id == address.id:
    #    raise ValueError("registrant address unexpected")
    #registrant = None
    if registrant is None:
        try:
            registrant = Registrant(registration_number=registration_number,
                                    registration_number_with_senior_officer_number=registration_number_with_senior_officer_number,
                                    status=status, effective_date=effective_date, type=_type, person=person, address=address)
        except ValueError as e:
            raise e

        db.session.add(registrant)

    return registrant


def process_registrants(data_registrants: list[Data], db):
    for data_registrant in data_registrants:
        raw_registrant_dict = data_registrant.data_value
        raw_registrant = TempRawRegistrant(
            RegistrationNUmber=raw_registrant_dict['RegistrationNUmber'],
            RegistrationNUmberWithSoNum=raw_registrant_dict['RegistrationNUmberWithSoNum'],
            Status=raw_registrant_dict['Status'],
            EffectiveDate=raw_registrant_dict['EffectiveDate'],
            Type=raw_registrant_dict['Type'],
            Prefix=raw_registrant_dict['Prefix'],
            FirstName=raw_registrant_dict['FirstName'],
            MiddleInitials=raw_registrant_dict['MiddleInitials'],
            LastName=raw_registrant_dict['LastName'],
            Suffix=raw_registrant_dict['Suffix'],
            PositionTitle=raw_registrant_dict['PositionTitle'],
            PreviousPublicOfficeHolder=raw_registrant_dict['PreviousPublicOfficeHolder'],
            PreviousPublicOfficeHoldPosition=raw_registrant_dict['PreviousPublicOfficeHoldPosition'],
            PreviousPublicOfficePositionProgramName=raw_registrant_dict['PreviousPublicOfficePositionProgramName'],
            PreviousPublicOfficeHoldLastDate=raw_registrant_dict['PreviousPublicOfficeHoldLastDate'],
            DataSource = data_registrant.source 
        )
    
        if process_prefix(raw_registrant.Prefix) is not None:
            raw_registrant.Prefix = process_prefix(raw_registrant.Prefix).value
        else:
            raw_registrant.Prefix = None
        
        if raw_registrant.PreviousPublicOfficeHolder == 'no':
            raw_registrant.PreviousPublicOfficeHolder = 'No'
        elif raw_registrant.PreviousPublicOfficeHolder == 'yes':
            raw_registrant.PreviousPublicOfficeHolder = 'Yes'

        if raw_registrant.PreviousPublicOfficeHolder == 'No' and raw_registrant.PreviousPublicOfficeHoldPosition is not None:
            raw_registrant.PreviousPublicOfficeHolder = 'Yes'
            
        if raw_registrant.RegistrationNUmberWithSoNum == '33003C': raw_registrant.FirstName = 'Bradley' # Sometimes FirstName == Brad Nickname?
        if raw_registrant.RegistrationNUmberWithSoNum == '29745S-1': raw_registrant.LastName = 'Fatehi' # Sometimes LastName == Fatehi Somee IDK
        if raw_registrant.RegistrationNUmberWithSoNum == '17769C': raw_registrant.LastName = 'Tomasella' # Sometimes LastName == Loiacono Married?
        if raw_registrant.RegistrationNUmberWithSoNum == '19772C':  raw_registrant.MiddleInitials = 'C' # Once MiddleInitials == M Typo?
        if raw_registrant.RegistrationNUmberWithSoNum == '18590C':  raw_registrant.LastName = 'Bassani' # Sometimes LastName == Chien Married?
        if raw_registrant.RegistrationNUmberWithSoNum == '12126C':  raw_registrant.FirstName = 'Leslie' # Sometimes FirstName == Leslie M  Typo?

        if raw_registrant.RegistrationNUmberWithSoNum == '14409C': # Sometimes PreviousPublicOfficeHolder == 'No'
            raw_registrant.PreviousPublicOfficeHolder = 'Yes'
            raw_registrant.PreviousPublicOfficeHoldPosition = 'Commissioner'
            raw_registrant.PreviousPublicOfficePositionProgramName = 'Toronto Transit Commission'
            raw_registrant.PreviousPublicOfficeHoldLastDate = '2014-03-06'
        db.session.add(raw_registrant)
    db.session.commit()

    # Get all unique RegistrationNUmberWithSoNum where Prefix is not null
    registrants_with_prefix = db.session.query(TempRawRegistrant.RegistrationNUmberWithSoNum).filter(TempRawRegistrant.Prefix.isnot(None)).distinct().all()

    # For each unique RegistrationNUmberWithSoNum, update Prefix
    for registrant in registrants_with_prefix:
        non_null_prefixes = db.session.query(TempRawRegistrant.Prefix).filter(TempRawRegistrant.RegistrationNUmberWithSoNum==registrant.RegistrationNUmberWithSoNum, TempRawRegistrant.Prefix.isnot(None)).distinct().all()

        if len(non_null_prefixes) > 1:
            raise ValueError(f"Multiple non-null prefixes found for RegistrationNUmberWithSoNum: {registrant.RegistrationNUmberWithSoNum}")

        elif non_null_prefixes:
            db.session.query(TempRawRegistrant).filter(TempRawRegistrant.RegistrationNUmberWithSoNum==registrant.RegistrationNUmberWithSoNum).update({TempRawRegistrant.Prefix: non_null_prefixes[0][0]})
    db.session.commit()

    # Handle PositionTitle

    


def get_non_superseded_registrants(rows:List[Dict]):
    return [row['Registrant'] for row in rows if row['Registrant']['Status'] != "Superseded"]

def get_data_registrants(data_rows:List[Data])->List[Data]:
    data_registrants = []
    for data_row in data_rows:
        data_registrants.append(Data(data_value=data_row.data_value['Registrant'],source=data_row.source))
    return data_registrants


def create_raw_tables(data_rows: List[Data]):
    for data_row in data_rows:
        data_value = data_row.data_value
        print(data_value['SMNumber'])

        registrant_data = data_value['Registrant']
        registrant_address_data = registrant_data['BusinessAddress']

        address = RawAddress(
            DataSource = data_row.source,
            address_line_1 = registrant_address_data['AddressLine1'],
            address_line_2 = registrant_address_data.get('AddressLine2'),
            city = registrant_address_data['City'],
            country = registrant_address_data['Country'],
            phone = registrant_address_data['Phone'],
            postal_code = registrant_address_data['PostalCode'],
            province = registrant_address_data['Province']
        )

        db.session.add(address)
        db.session.commit()

        raw_registrant = RawRegistrant(
            DataSource = data_row.source,
            RegistrationNUmber = registrant_data['RegistrationNUmber'],
            RegistrationNUmberWithSoNum = registrant_data['RegistrationNUmberWithSoNum'],
            Status = registrant_data['Status'],
            EffectiveDate = registrant_data['EffectiveDate'],
            Type = registrant_data['Type'],
            Prefix = registrant_data['Prefix'],
            FirstName = registrant_data['FirstName'],
            MiddleInitials = registrant_data['MiddleInitials'],
            LastName = registrant_data['LastName'],
            Suffix = registrant_data['Suffix'],
            PositionTitle = registrant_data['PositionTitle'],
            PreviousPublicOfficeHolder = registrant_data['PreviousPublicOfficeHolder'],
            PreviousPublicOfficeHoldPosition = registrant_data['PreviousPublicOfficeHoldPosition'],
            PreviousPublicOfficePositionProgramName = registrant_data['PreviousPublicOfficePositionProgramName'],
            PreviousPublicOfficeHoldLastDate = registrant_data['PreviousPublicOfficeHoldLastDate'],
        )

        db.session.add(raw_registrant)
        db.session.commit()

        raw_lobbying_report = RawLobbyingReport(
            DataSource = data_row.source,
            SMNumber = data_value['SMNumber'],
            Status = data_value['Status'],
            Type = data_value['Type'],
            SubjectMatter = data_value['SubjectMatter'],
            Particulars = data_value['Particulars'],
            InitialApprovalDate = data_value['InitialApprovalDate'],
            EffectiveDate = data_value['EffectiveDate'],
            ProposedStartDate = data_value['ProposedStartDate'],
            ProposedEndDate = data_value['ProposedEndDate']
        )

        db.session.add(raw_lobbying_report)
        db.session.commit()

        if 'Communications' in data_value:
            if type(data_value['Communications']['Communication'])==dict:
                raw_communications = [data_value['Communications']['Communication']]
            else:
                raw_communications = data_value['Communications']['Communication']

            for communication_data in raw_communications:
                try:
                    raw_communication = RawCommunications(
                        DataSource = data_row.source,
                        POH_Office = communication_data['POH_Office'],
                        POH_Type = communication_data['POH_Type'],
                        POH_Position = communication_data['POH_Position'],
                        POH_Name = communication_data['POH_Name'],
                        CommunicationsMethod = communication_data['CommunicationMethod'],
                        CommunicationDate = communication_data['CommunicationDate'],
                        CommunicationGroupId = communication_data['CommunicationGroupId'],
                        LobbyistNumber = communication_data['LobbyistNumber'],
                        LobbyistType = communication_data['LobbyistType'],
                        LobbyistPrefix = communication_data['LobbyistPrefix'],
                        LobbyistFirstName = communication_data['LobbyistFirstName'],
                        LobbyistMiddleInitials = communication_data['LobbyistMiddleInitials'],
                        LobbyistLastName = communication_data['LobbyistLastName'],
                        LobbyistSuffix = communication_data['LobbyistSuffix'],
                        LobbyistBusiness = communication_data['LobbyistBusiness'],
                        LobbyistPositionTitle = communication_data['LobbyistPositionTitle'],
                        PreviousPublicOfficeHolder = communication_data['PreviousPublicOfficeHolder'],
                        PreviousPublicOfficePositionProgramName = communication_data['PreviousPublicOfficePositionProgramName'],
                        PreviousPublicOfficeHoldLastDate = communication_data['PreviousPublicOfficeHoldLastDate'],
                        report_id = raw_lobbying_report.id
                    )
                except Exception as e:
                    pprint.pprint(communication_data)
                    raise e
                db.session.add(raw_communication)
                db.session.commit()
    db.session.commit()



from app import app, db 

def run():
    with app.app_context():
        db = setup_db(app_db)
        data_rows = []
        for data_source in DataSource:
            start_time = time.time()
            data_rows += get_data_rows(xml_to_dict(data_source), data_source)
            end_time = time.time()
            print(f"Parse {data_source.value}: {end_time - start_time} seconds")
            
        start_time = time.time()
        create_raw_tables(data_rows)
        end_time = time.time()
        print(f"Create all Raw Tables: {end_time - start_time} seconds")
        
        #start_time = time.time()
        #process_registrants(get_data_registrants(data_rows),db)
        #db.session.commit()
        #end_time = time.time()
        #print(f"Create all Registrant: {end_time - start_time} seconds")

        
        #start_time = time.time()
        #for registrant_dict in get_non_superseded_registrants(rows):
        #    process_registrant(registrant_dict,db)
        #db.session.commit()
        #end_time = time.time()
        #print(f"Create all Registrant: {end_time - start_time} seconds")

        #start_time = time.time()
        #for row_dict in rows:
        #    process_lobbying_report(row_dict,db)
        #db.session.commit()
        #end_time = time.time()
        #print(f"Create all Lobbying Reports: {end_time - start_time} seconds")

if __name__ == '__main__':
    run()
