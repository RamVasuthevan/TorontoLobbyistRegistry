from typing import List,Dict
import os
import xmltodict
import time
import pprint
from app import db as app_db
from app.models import LobbyingReport

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

def process_row(row:Dict, db):
    smnumber = row['SMNumber']
    status = row['Status']   
    report = LobbyingReport(smnumber=smnumber, status=status)  
    db.session.add(report) 


from app import app, db  # Import the Flask and SQLAlchemy instances

def run():
    with app.app_context():
        db = setup_db(app_db)

        for data_file in DATA_FILES:
            start_time = time.time()
            D = xml_to_dict(data_file)
            rows = process_file(D)
            for row in rows:
                process_row(row, db)  # Pass row and db to process_row function
            db.session.commit()
            end_time = time.time()
            print(f"Processing time for {data_file}: {end_time - start_time} seconds")


if __name__ == '__main__':
    run()
