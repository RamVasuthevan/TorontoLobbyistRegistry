import unittest
import re
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Registrant

class TestRegistrantData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up database connection
        engine = create_engine('sqlite:///lobbyist_registry.db.tmp')
        Session = sessionmaker(bind=engine)
        cls.session = Session()

    @classmethod
    def tearDownClass(cls):
        # Close the sessionc
        cls.session.close()

    def test_registration_number_format(self):
        registrants = self.session.query(Registrant).all()
        for registrant in registrants:
            with self.subTest(registration_number=registrant.registration_number):
                self.assertTrue(re.match(r'^\d{5}[SCV]$', registrant.registration_number),
                                f"Invalid registration number format: {registrant.registration_number}")

    def test_status_values(self):
        valid_statuses = ['Superseded', 'Active', 'Not Accepted', 'Force Closed']
        registrants = self.session.query(Registrant).all()
        for registrant in registrants:
            with self.subTest(status=registrant.status):
                self.assertIn(registrant.status, valid_statuses,
                              f"Invalid status: {registrant.status}")

    def test_previous_public_office_holder_values(self):
        valid_values = ['Yes', 'No']
        registrants = self.session.query(Registrant).all()
        for registrant in registrants:
            with self.subTest(previous_public_office_holder=registrant.previous_public_office_holder):
                self.assertIn(registrant.previous_public_office_holder, valid_values,
                              f"Invalid previous_public_office_holder value: {registrant.previous_public_office_holder}")

    def test_effective_date_format(self):
        registrants = self.session.query(Registrant).all()
        for registrant in registrants:
            with self.subTest(effective_date=registrant.effective_date):
                if registrant.effective_date is not None:
                    try:
                        datetime.strptime(registrant.effective_date, '%Y-%m-%d')
                    except ValueError:
                        self.fail(f"Invalid effective_date format: {registrant.effective_date}")
                else:
                    # If effective_date is None, the test passes
                    pass

    def test_type_values(self):
        valid_types = ['Consultant', 'In-house']
        registrants = self.session.query(Registrant).all()
        for registrant in registrants:
            with self.subTest(type=registrant.type):
                self.assertIn(registrant.type, valid_types,
                              f"Invalid type: {registrant.type}")

    def test_previous_public_office_hold_last_date_format(self):
        registrants = self.session.query(Registrant).all()
        for registrant in registrants:
            with self.subTest(registration_number=registrant.registration_number):
                if registrant.previous_public_office_holder == 'Yes':
                    if registrant.previous_public_office_hold_last_date is not None:
                        try:
                            datetime.strptime(registrant.previous_public_office_hold_last_date, '%Y-%m-%d')
                        except ValueError:
                            self.fail(f"Invalid previous_public_office_hold_last_date format: {registrant.previous_public_office_hold_last_date}")

if __name__ == '__main__':
    unittest.main()