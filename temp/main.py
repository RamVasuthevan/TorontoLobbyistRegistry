import os
import logging
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from parse_xml_file import parse_xml_file

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
    if os.path.exists(db_file):
        os.remove(db_file)
        logging.info(f"Deleted existing database file: {db_file}")

def create_tables():
    Base.metadata.create_all(engine)
    logging.info("Created new database tables")

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
    logging.info("Database population completed")