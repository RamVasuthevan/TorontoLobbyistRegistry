import unittest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Firm  # Assuming the Firm model is defined in models.py

class TestFirmData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up database connection
        engine = create_engine('sqlite:///lobbyist_registry.db')
        Session = sessionmaker(bind=engine)
        cls.session = Session()

    @classmethod
    def tearDownClass(cls):
        # Close the session
        cls.session.close()

    def test_business_type_values(self):
        valid_business_types = [
            'Corporation',
            'Business/ Industry/ Trade Association',
            'Sole Proprietor',
            'Partnership',
            'Professional/ Labour Association',
            'Not-for-profit grant applicant',
            None
        ]
        firms = self.session.query(Firm).all()
        for firm in firms:
            with self.subTest(business_type=firm.business_type):
                self.assertIn(firm.business_type, valid_business_types,
                              f"Invalid business_type: {firm.business_type}")

    def test_type_values(self):
        valid_types = [
            'Consultant',
            'In-house',
            'Other',
            'Parent',
            'Subsidiary'
        ]
        firms = self.session.query(Firm).all()
        for firm in firms:
            with self.subTest(type=firm.type):
                self.assertIn(firm.type, valid_types,
                              f"Invalid type: {firm.type}")

    def test_name_not_empty(self):
        firms = self.session.query(Firm).all()
        for firm in firms:
            with self.subTest(name=firm.name):
                self.assertTrue(firm.name.strip(),
                                f"Name should not be empty for firm: {firm.type}")

    def test_fiscal_dates_format(self):
        firms = self.session.query(Firm).all()
        for firm in firms:
            with self.subTest(firm=firm.name):
                if firm.fiscal_start:
                    try:
                        datetime.strptime(firm.fiscal_start, '%Y-%m-%d')
                    except ValueError:
                        self.fail(f"Invalid fiscal_start date format: {firm.fiscal_start}")

                if firm.fiscal_end:
                    try:
                        datetime.strptime(firm.fiscal_end, '%Y-%m-%d')
                    except ValueError:
                        self.fail(f"Invalid fiscal_end date format: {firm.fiscal_end}")

if __name__ == '__main__':
    unittest.main()
