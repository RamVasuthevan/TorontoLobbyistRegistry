from typing import List, Dict
import os
import shutil
import xmltodict
import time
import zipfile
import pprint
import cProfile
import pstats

from app import db as app_db
from app.models.models import (
    LobbyingReport,
    Address,
    Grassroot,
    Beneficiary,
    Firm,
    GovernmentFunding,
    PrivateFunding,
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
)
from app.models.enums import DataSource
from build.raw import create_raw_tables
from build.lobbying_reports import create_lobbying_reports
from build.grassroots import create_grassroots
from build.beneficiaries import create_beneficiaries

from dataclasses import dataclass
from sqlalchemy import delete


DATA_PATH = "data"


@dataclass
class Data:
    data_value: str
    source: DataSource


def xml_to_dict(data_source: DataSource) -> Dict:
    with open(os.path.join(DATA_PATH, data_source.value)) as fd:
        return xmltodict.parse(fd.read())


def setup_db(db):
    db.drop_all()
    db.create_all()
    return db


def get_data_rows(file_dict: Dict, data_source: DataSource) -> List[Data]:
    data_rows = []
    for val in file_dict["ROWSET"]["ROW"]:
        row = val["SMXML"]["SM"]
        data_rows.append(Data(data_value=row, source=data_source))

    return data_rows


def extract_files_from_zip():
    zip_file = os.path.join(DATA_PATH, "lobbyactivity.zip")
    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        for member in zip_ref.namelist():
            filename = os.path.basename(member)
            source = zip_ref.open(member)
            target = open(os.path.join(DATA_PATH, filename), "wb")
            with source, target:
                shutil.copyfileobj(source, target)


def delete_all_data(db, models):
    for model in models:
        db.session.execute(delete(model))


def create_data_rows(db):
    data_rows = []
    for data_source in DataSource:
        start_time = time.time()
        data_rows += get_data_rows(xml_to_dict(data_source), data_source)
        end_time = time.time()
        print(f"Parse {data_source.value}: {end_time - start_time} seconds")

    start_time = time.time()
    create_raw_tables(db, data_rows)
    end_time = time.time()
    print(f"Create all Raw Tables: {end_time - start_time} seconds")


def create_models(db, raw_models, create_functions):
    for raw_model, create_function in zip(raw_models, create_functions):
        start_time = time.time()
        create_function(db, raw_model.query.all())
        end_time = time.time()
        print(f"Create all {raw_model.__name__}: {end_time - start_time} seconds")


from app import app, db


def run():
    with app.app_context():
        extract_files_from_zip()

        db = setup_db(app_db)

        delete_all_data(
            db,
            [
                LobbyingReport,
            ],
        )
        create_data_rows(db)
        create_models(db,[RawLobbyingReport],[create_lobbying_reports])

        db.session.commit()


if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()
    run()
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumtime')  # sort by cumulative time spent in function
    stats.print_stats()
