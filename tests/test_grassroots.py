import unittest
from datetime import datetime
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Grassroots


class TestGrassrootsData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up database connection
        engine = create_engine('sqlite:///lobbyist_registry.db.tmp')
        Session = sessionmaker(bind=engine)
        cls.session = Session()
        
        # Set up logging
        logging.basicConfig(level=logging.WARNING)

    def setUp(self):
        # Create a logger for each test instance
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    @classmethod
    def tearDownClass(cls):
        # Close the session
        cls.session.close()

    def test_start_and_end_dates(self):
        grassroots_entries = self.session.query(Grassroots).all()
        for entry in grassroots_entries:
            with self.subTest(grassroots_id=entry.id):
                for date_field in ['start_date', 'end_date']:
                    date_value = getattr(entry, date_field)
                    if date_value:
                        try:
                            datetime.strptime(date_value, '%Y-%m-%d')
                        except ValueError:
                            self.fail(f"Invalid {date_field} format for Grassroots ID {entry.id}: {date_value}")

    def test_community_and_target_not_blank(self):
        grassroots_entries = self.session.query(Grassroots).all()
        for entry in grassroots_entries:
            with self.subTest(grassroots_id=entry.id):
                self.assertTrue(entry.community.strip(), f"Community is blank for Grassroots ID {entry.id}")
                self.assertTrue(entry.target.strip(), f"Target is blank for Grassroots ID {entry.id}")

if __name__ == '__main__':
    unittest.main()
