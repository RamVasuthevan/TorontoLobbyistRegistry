from typing import List, Dict
import os
import xmltodict
import zipfile
import pprint

from app import db as app_db

from app.models.models import (
    Address,
    CanadianAddress,
    AmericanAddress,
    OtherAddress,
    raw_address_address,
    raw_lobbyist_lobbyist,
    LobbyingReport,
    Grassroot,
    Beneficiary,
    Firm,
    GovernmentFunding,
    PrivateFunding,
    Meeting,
    PublicOfficeHolder,
    Lobbyist,
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
    RawPOH,
    RawLobbyist,
)
from app.models.enums import DataSource
from build.raw import create_raw_tables
from build.addresses import create_addresses_table
from build.meetings import create_meeting_table


from build import grassroots
from build import private_fundings
from build import public_office_holders
from build import lobbying_reports
from build import government_fundings
from build import beneficiaries
from build import firms
from build import lobbyists

from dataclasses import dataclass
from sqlalchemy import delete
from utils.profiling import timer


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
        with timer(f"Get_data_rows {data_source.value}"):
            data_rows += get_data_rows(xml_to_dict(data_source), data_source)

    return data_rows


def create_tables(db):
    with timer("Create address table"):
        create_addresses_table(db.session, RawAddress.query.all())

    with timer("Create all lobbyist tables"):
        lobbyists.create_table(db.session)
        

    with timer("Create all lobbying report tables"):
        lobbying_reports.create_table(db.session)

    with timer("Create all grassroots tables"):
        grassroots.create_table(db.session)

    with timer("Create all government funding tables"):
        government_fundings.create_table(db.session)

    with timer("Create all private funding tables"):
        private_fundings.create_table(db.session)

    with timer("Create all beneficiaries tables"):
        beneficiaries.create_table(db.session)

    with timer("Create all firms tables"):
        firms.create_table(db.session)

    with timer("Create all meeting tables"):
        create_meeting_table(db.session, RawMeeting.query.all())

    with timer("Create all public office holder tables"):
        public_office_holders.create_table(db.session)


def delete_tables(db):
    Address.query.delete()
    CanadianAddress.query.delete()
    AmericanAddress.query.delete()
    OtherAddress.query.delete()
    LobbyingReport.query.delete()
    Grassroot.query.delete()
    GovernmentFunding.query.delete()
    PrivateFunding.query.delete()
    Beneficiary.query.delete()
    Firm.query.delete()
    Meeting.query.delete()
    PublicOfficeHolder.query.delete()
    Lobbyist.query.delete()


def delete_association_tables(db):
    db.session.query(raw_address_address).delete()
    db.session.query(raw_lobbyist_lobbyist).delete()


from app import app, db


def run():
    with app.app_context():
        if True:
            with timer("Extract files"):
                extract_files_from_zip(DATA_ZIP)

            db.drop_all()
            db.create_all()

            with timer("Create data_rows"):
                data_rows = create_data_rows()


            with timer("Create raw tables"):
                create_raw_tables(db, data_rows)


        with timer("Delete tables"):
            delete_tables(db)
            delete_association_tables(db)

        create_tables(db)

        db.session.commit()


if __name__ == "__main__":
    run()
