from typing import List,Dict
import os
import xmltodict
import time
import pprint
from app import db as app_db
from app.models import LobbyingReport, LobbyingReportStatus, LobbyingReportType, Registrant, RegistrantStatus, RegistrantType, get_enum_error_message, PersonPrefix, Person, Address, AddressCountry, DataSource
from app.processor_models import RawRegistrant
from datetime import datetime, date
from enum import Enum
from dataclasses import dataclass

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
    if raw_prefix is None:
        return None

    prefix = raw_prefix.strip().lower().replace('.', '').replace(',', '')

    if prefix == "mrm": # Data Cleaning
        prefix = "mr"
    
    if prefix in ['m']: # Data Cleaning
        return None

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
        raw_registrant = RawRegistrant(
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
        
        db.session.add(raw_registrant)
        
    db.session.commit()

    # Select all raw_registrant records
    raw_registrants = RawRegistrant.query.all()
    
    # Add raw_registrant records to the Registrant table
    for raw_registrant in raw_registrants:
        registrant = Registrant(
            registration_number_with_senior_officer_number=raw_registrant.RegistrationNUmberWithSoNum,
            registration_number=raw_registrant.RegistrationNUmber
        )
        db.session.add(registrant)
    
    db.session.commit()


def get_non_superseded_registrants(rows:List[Dict]):
    return [row['Registrant'] for row in rows if row['Registrant']['Status'] != "Superseded"]

def get_data_registrants(data_rows:List[Data])->List[Data]:
    data_registrants = []
    for data_row in data_rows:
        data_registrants.append(Data(data_value=data_row.data_value['Registrant'],source=data_row.source))
    return data_registrants

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
        process_registrants(get_data_registrants(data_rows),db)
        db.session.commit()
        end_time = time.time()
        print(f"Create all Registrant: {end_time - start_time} seconds")

        
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
