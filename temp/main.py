import os
import logging
import unittest
from datetime import datetime
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from sqlite_utils import Database
from models import Base
from parse_xml_file import parse_xml_file
from test_database import TestDatabase
from test_registrants import TestRegistrantData
from test_subject_matters import TestSubjectMatterData
from data_cleaning import run_data_cleaning  

# Set up logging
def setup_logging():
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_filename = f"{log_dir}/lobbyist_registry_{timestamp}.log"
    
    # File handler for logging all levels
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.INFO)
    
    # Stream handler for logging only errors
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[file_handler, console_handler]
    )
    
    return log_filename

# Database setup
db_file = 'lobbyist_registry.db'
engine = create_engine(f'sqlite:///{db_file}')
Session = sessionmaker(bind=engine)

def delete_existing_db():
    logging.info(f"Deleting existing database file: {db_file}")
    if os.path.exists(db_file):
        os.remove(db_file)
        logging.info(f"Deleted existing database file: {db_file}")

def create_tables():
    logging.info("Creating new database tables")
    Base.metadata.create_all(engine)
    logging.info("Created new database tables")

def enable_fts():
    logging.info("Enabling Full Text Search for all tables")
    db = Database(db_file)
    inspector = inspect(engine)

    for table_name in inspector.get_table_names():
        if not table_name.endswith('_fts'):
            columns = [column['name'] for column in inspector.get_columns(table_name)]
            db[table_name].enable_fts(columns, create_triggers=True)
    
    logging.info("Enabled Full Text Search for all tables")

def run_unit_tests():
    logging.info("Running unit tests")
    
    # Create a test suite
    suite = unittest.TestSuite()
    
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDatabase))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestRegistrantData))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestSubjectMatterData))
    # Run the tests
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    
    if result.wasSuccessful():
        logging.info("All unit tests passed")
    else:
        logging.error("Some unit tests failed")
        logging.error(f"Failures: {len(result.failures)}, Errors: {len(result.errors)}")
        for failure in result.failures:
            logging.error(f"Test failed: {failure[0]}")
            logging.error(f"Error message: {failure[1]}")
        for error in result.errors:
            logging.error(f"Test error: {error[0]}")
            logging.error(f"Error message: {error[1]}")


if __name__ == "__main__":
    log_filename = setup_logging()
    logging.info(f"Logging to file: {log_filename}")

    delete_existing_db()
    create_tables()
    
    session = Session()
    
    xml_files = ['lobbyactivity-active.xml', 'lobbyactivity-closed.xml']
    for xml_file in xml_files:
        logging.info(f"Starting to parse {xml_file}")
        parse_xml_file(xml_file, session)
        logging.info(f"Finished parsing {xml_file}")
    
    session.close()

    enable_fts()
    logging.info("Database population completed with Full Text Search enabled")

    run_data_cleaning(session)

    run_unit_tests()