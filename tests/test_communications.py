import unittest
import re
import logging
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Communication

class TestCommunicationData(unittest.TestCase):
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

    def test_communication_date_format(self):
        communications = self.session.query(Communication).all()
        for communication in communications:
            with self.subTest(communication_id=communication.id):
                date_value = communication.communication_date
                if date_value:
                    try:
                        datetime.strptime(date_value, '%Y-%m-%d')
                    except ValueError:
                        self.fail(f"Invalid communication_date format for communication ID {communication.id}: {date_value}")

    def test_poh_type_values(self):
        valid_poh_types = [
            'Member of Council',
            'Staff of Member of Council',
            'Employee of the City',
            'Employee of Local Board',
            'Member of Local Board',
            'Staff of Member of Local Board',
            'Member of Advisory Body',
            None
        ]
        poh_type_counts = {}
        communications = self.session.query(Communication).all()
        for communication in communications:
            with self.subTest(poh_type=communication.poh_type):
                self.assertIn(communication.poh_type, valid_poh_types,
                              f"Invalid poh_type: {communication.poh_type}")
                poh_type_counts[communication.poh_type] = poh_type_counts.get(communication.poh_type, 0) + 1

    def test_lobbyist_type_values(self):
        valid_lobbyist_types = ['In-House Lobbyist', 'Sr. Officer',None]
        lobbyist_type_counts = {}
        communications = self.session.query(Communication).all()
        for communication in communications:
            with self.subTest(lobbyist_type=communication.lobbyist_type):
                self.assertIn(communication.lobbyist_type, valid_lobbyist_types,
                              f"Invalid lobbyist_type: {communication.lobbyist_type}")
                lobbyist_type_counts[communication.lobbyist_type] = lobbyist_type_counts.get(communication.lobbyist_type, 0) + 1

    def test_lobbyist_previous_public_office_holder_values(self):
        valid_values = ['No', 'Yes', None]
        lobbyist_previous_public_office_holder_counts = {}
        communications = self.session.query(Communication).all()
        for communication in communications:
            with self.subTest(lobbyist_previous_public_office_holder=communication.lobbyist_previous_public_office_holder):
                self.assertIn(communication.lobbyist_previous_public_office_holder, valid_values,
                              f"Invalid lobbyist_previous_public_office_holder: {communication.lobbyist_previous_public_office_holder}")
                lobbyist_previous_public_office_holder_counts[communication.lobbyist_previous_public_office_holder] = lobbyist_previous_public_office_holder_counts.get(communication.lobbyist_previous_public_office_holder, 0) + 1

if __name__ == '__main__':
    unittest.main()
