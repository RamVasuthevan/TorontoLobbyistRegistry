from typing import List, Dict
import os
import xmltodict
import time
import zipfile
import pprint

from app import db as app_db
from app.models.models import (
    Address,
    CanadianAddress,
    AmericanAddress,
    OtherAddress,
    raw_address_address,
    LobbyingReport,
    Grassroot,
    Beneficiary,
    Firm,
    GovernmentFunding,
    PrivateFunding,
    Meeting,
    PublicOfficeHolder
)
from app.models.processor_models import (
    RawGrassroot,
    RawBeneficiary,
    RawFirm,
    RawPrivateFunding,
    RawGmtFunding,
    RawPrivateFunding,
    RawGmtFunding,
    RawLobbyingReport,
    RawAddress,
    RawMeeting,
    RawPOH
)
from app.models.enums import DataSource
from build.raw import create_raw_tables
from build.addresses import create_addresses_table
from build.lobbying_reports import create_lobbying_report_table
from build.grassroots import create_grassroots_table
from build.beneficiaries import create_beneficiaries_table
from build.firms import create_firms_table
from build.government_fundings import create_government_funding_table
from build.private_fundings import create_private_funding_table
from build.meetings import create_meeting_table
from build.public_office_holders import create_public_office_holder_table

from dataclasses import dataclass
from sqlalchemy import delete


DATA_PATH = "data"
DATA_ZIP = "lobbyactivity.zip"


@dataclass
class Data:
    data_value: str
    source: DataSource


def xml_to_dict(data_source: DataSource) -> Dict:
    with open(os.path.join(DATA_PATH, data_source.value)) as fd:
        return xmltodict.parse(fd.read())


def get_data_rows(file_dict: Dict, data_source: DataSource) -> List[Data]:
    data_rows = []
    for val in file_dict["ROWSET"]["ROW"]:
        row = val["SMXML"]["SM"]
        data_rows.append(Data(data_value=row, source=data_source))

    return data_rows


def extract_files_from_zip(file_name: str) -> None:
    zip_file = os.path.join(DATA_PATH, file_name)
    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        zip_ref.extractall(DATA_PATH)


def delete_all_data(db, models):
    for model in models:
        db.session.execute(delete(model))


def create_data_rows() -> List[Data]:
    data_rows = []
    for data_source in DataSource:
        start_time = time.time()
        data_rows += get_data_rows(xml_to_dict(data_source), data_source)
        end_time = time.time()
        print(f"Parse {data_source.value}: {end_time - start_time} seconds")
    return data_rows


def create_tables(db, raw_models, create_functions):
    for raw_model, create_function in zip(raw_models, create_functions):
        start_time = time.time()
        create_function(db.session, raw_model.query.all())
        end_time = time.time()
        print(f"Create all {raw_model.__name__}: {end_time - start_time} seconds")


from app import app, db


def run():
    with app.app_context():
        if True:
            
            start_time = time.time()
            extract_files_from_zip(DATA_ZIP)
            end_time = time.time()
            print(f"Extract files: {end_time - start_time} seconds")

            db.drop_all()
            db.create_all()

            start_time = time.time()
            data_rows = create_data_rows()
            end_time = time.time()
            print(f"Create data_rows : {end_time - start_time} seconds")

            start_time = time.time()
            create_raw_tables(db, data_rows)
            end_time = time.time()
            print(f"Create all Raw Tables: {end_time - start_time} seconds")

        Address.query.delete()
        CanadianAddress.query.delete()
        AmericanAddress.query.delete()
        OtherAddress.query.delete()
        raw_address_address.delete()
        LobbyingReport.query.delete()
        Grassroot.query.delete()
        GovernmentFunding.query.delete()
        PrivateFunding.query.delete()
        Beneficiary.query.delete()
        Firm.query.delete()
        Meeting.query.delete()
        PublicOfficeHolder.query.delete()

        create_tables(
            db,
            [RawAddress, RawLobbyingReport, RawGrassroot, RawGmtFunding, RawPrivateFunding,RawBeneficiary, RawFirm,RawMeeting,RawPOH],
            [
                create_addresses_table,
                create_lobbying_report_table,
                create_grassroots_table,
                create_government_funding_table,
                create_private_funding_table,
                create_beneficiaries_table,
                create_firms_table,
                create_meeting_table,
                create_public_office_holder_table
            ],
        )

        db.session.commit()

if __name__ == "__main__":
    run()
