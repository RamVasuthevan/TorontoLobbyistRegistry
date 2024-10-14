import os
import logging
import unittest
import requests
import zipfile
from io import BytesIO
from datetime import datetime
from sqlalchemy import create_engine, inspect, Index
from sqlalchemy.orm import sessionmaker
from sqlite_utils import Database
from models import Base
from parse_xml_file import parse_xml_file
from data_cleaning import run_data_cleaning

# Set up logging
def setup_logging():
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"{log_dir}/lobbyist_registry_{timestamp}.log"

    # File handler for logging all levels
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.INFO)

    # Stream handler for logging only errors
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[file_handler, console_handler],
    )

    return log_filename

# Database setup
db_file = "lobbyist_registry.db"

def get_temp_db_file_name():
    temp_db_file_name = f"{db_file}.tmp"
    return temp_db_file_name

def create_engine_and_session(db_path):
    engine = create_engine(f"sqlite:///{db_path}")
    Session = sessionmaker(bind=engine)
    return engine, Session

def replace_db_with_temp():
    temp_db_file_name = get_temp_db_file_name()
    if os.path.exists(temp_db_file_name):
        if os.path.exists(db_file):
            os.remove(db_file)
            os.rename(temp_db_file_name, db_file)
            logging.info(f"Replaced old database with new one: {db_file}")
        else:
            os.rename(temp_db_file_name, db_file)
    else:
        logging.error(f"Temporary database({temp_db_file_name}) not found. No changes made.")

def create_tables(engine):
    logging.info("Creating new database tables")
    Base.metadata.create_all(engine)
    logging.info("Created new database tables")

def create_indexes_for_foreign_keys_sqlalchemy(base, engine):
    metadata = base.metadata
    for table in metadata.tables.values():
        for column in table.columns:
            if column.foreign_keys and not column.index:
                # Dynamically create and bind the index
                index = Index(f'idx_{table.name}_{column.name}', column)
                logging.info(f"Creating index: idx_{table.name}_{column.name}")
                index.create(bind=engine)

def enable_fts(db_path):
    logging.info("Enabling Full Text Search for all tables")
    db = Database(db_path)
    engine = create_engine(f"sqlite:///{db_path}")
    inspector = inspect(engine)

    for table_name in inspector.get_table_names():
        if not table_name.endswith("_fts"):
            columns = [column["name"] for column in inspector.get_columns(table_name)]
            db[table_name].enable_fts(columns, create_triggers=True)

    logging.info("Enabled Full Text Search for all tables")

def run_unit_tests():
    logging.info("Running unit tests")

    loader = unittest.TestLoader()
    suite = loader.discover(start_dir='tests')

    logging.info("Test files to be run:")
    for test_group in suite:
        for test_suite in test_group:
            for test_case in test_suite:
                logging.info(f"Running tests from: {test_case.__module__}")

    result = unittest.TextTestRunner(verbosity=2).run(suite)

    if result.wasSuccessful():
        logging.info("All unit tests passed")
        return True
    else:
        logging.error("Some unit tests failed")
        logging.error(f"Failures: {len(result.failures)}, Errors: {len(result.errors)}")
        for failure in result.failures:
            logging.error(f"Test failed: {failure[0]}")
            logging.error(f"Error message: {failure[1]}")
        for error in result.errors:
            logging.error(f"Test error: {error[0]}")
            logging.error(f"Error message: {error[1]}")
        return False

def download_and_unzip(url, extract_to='data'):
    logging.info(f"Downloading file from {url}")
    response = requests.get(url)
    if response.status_code == 200:
        logging.info("Download successful. Extracting files...")
        with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(extract_to)
        logging.info(f"Files extracted to {extract_to}")
    else:
        logging.error(f"Failed to download file. Status code: {response.status_code}")

if __name__ == "__main__":
    log_filename = setup_logging()
    logging.info(f"Logging to file: {log_filename}")

    # Download and extract the ZIP file
    github_url = "https://github.com/RamVasuthevan/TorontoLobbyistRegistryData/raw/main/Lobbyist%20Registry%20Activity.zip"
    download_and_unzip(github_url)

    # Use a temporary database file
    temp_db_file_name = get_temp_db_file_name()
    if os.path.exists(temp_db_file_name):
        os.remove(temp_db_file_name)
        
    engine, Session = create_engine_and_session(temp_db_file_name)

    create_tables(engine)

    session = Session()
    
    data_folder = 'data'
    xml_files = [f for f in os.listdir(data_folder) if f.endswith('.xml')]

    for xml_file in xml_files:
        file_path = os.path.join(data_folder, xml_file)
        logging.info(f"Starting to parse {file_path}")
        parse_xml_file(file_path, session)
        logging.info(f"Finished parsing {file_path}")
    
    session.close()

    create_indexes_for_foreign_keys_sqlalchemy(Base, engine)
    logging.info("Indexes for all foreign keys added")

    run_data_cleaning(Session())

    enable_fts(temp_db_file_name)
    logging.info("Database population completed with Full Text Search enabled")
    
    # Run unit tests
    test_result = run_unit_tests()
    
    if test_result:
        # If tests pass, replace the old database with the new one
        replace_db_with_temp()
        logging.info("Database update completed successfully")
    else:
        logging.error("Tests failed. New database not applied.")
        if os.path.exists(temp_db_file_name):
            os.remove(temp_db_file_name)
            logging.info("Temporary database file removed")
