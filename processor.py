from typing import List,Dict
import os
import xmltodict
import time
import pprint
from app import db as app_db
from app.models import LobbyingReport, LobbyingReportStatus, LobbyingReportType

DATA_PATH = 'data'
DATA_FILES = ['lobbyactivity-active.xml','lobbyactivity-closed.xml']



def xml_to_dict(data_file: str) -> Dict:
    with open(os.path.join(DATA_PATH, data_file)) as fd:
        return xmltodict.parse(fd.read())

def setup_db(db):
    db.drop_all()  # Delete all tables in the database
    db.create_all()  # Create all tables in the database
    return db

def process_file(file_dict: Dict)->List[Dict]:
    rows = [val['SMXML']['SM'] for val in  file_dict['ROWSET']['ROW']]
    return rows

def process_row(row: Dict, db):
    smnumber = row['SMNumber']
    status = LobbyingReportStatus(row['Status'])
    _type = LobbyingReportType(row['Type'])
    subject_matter = row['SubjectMatter']
    report = LobbyingReport(smnumber=smnumber, status=status, type=_type,subject_matter=subject_matter)
    db.session.add(report)
    if ";" in row['SubjectMatter']:
        return row['SubjectMatter'].split(';')
    else:
        return [row['SubjectMatter']]


from app import app, db  # Import the Flask and SQLAlchemy instances

def run():
    subject_matters = list()
    with app.app_context():
        db = setup_db(app_db)
        for data_file in DATA_FILES:
            start_time = time.time()
            D = xml_to_dict(data_file)
            rows = process_file(D)
            for row in rows:
                subject_matters += process_row(row, db)
                process_row(row, db)
            db.session.commit()
            end_time = time.time()
            print(f"Processing time for {data_file}: {end_time - start_time} seconds")
        for val in sorted(list(set(subject_matters))):
            print(val)


if __name__ == '__main__':
    run()
