import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from parse_xml_file import parse_xml_file

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Database setup
db_file = 'lobbyist_registry.db'
engine = create_engine(f'sqlite:///{db_file}')
Session = sessionmaker(bind=engine)

def delete_existing_db():
    if os.path.exists(db_file):
        os.remove(db_file)
        logging.info(f"Deleted existing database file: {db_file}")

def create_tables():
    Base.metadata.create_all(engine)
    logging.info("Created new database tables")

if __name__ == "__main__":
    delete_existing_db()
    create_tables()
    
    session = Session()
    parse_xml_file('lobbyactivity-active.xml', session)
    parse_xml_file('lobbyactivity-closed.xml', session)
    session.close()