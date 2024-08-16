import unittest
import re
import logging
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import SubjectMatter

class TestSubjectMatterData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up database connection
        engine = create_engine('sqlite:///lobbyist_registry.db')
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

    def test_sm_number_format(self):
        subject_matters = self.session.query(SubjectMatter).all()
        for sm in subject_matters:
            with self.subTest(sm_number=sm.sm_number):
                self.assertTrue(re.match(r'^SM\d{5}$', sm.sm_number),
                                f"Invalid sm_number format: {sm.sm_number}")

    def test_status_values(self):
        valid_statuses = ['Closed by LRO','Closed','Active']
        status_counts = {}
        subject_matters = self.session.query(SubjectMatter).all()
        for sm in subject_matters:
            with self.subTest(status=sm.status):
                self.assertIn(sm.status, valid_statuses,
                              f"Invalid status: {sm.status}")
                status_counts[sm.status] = status_counts.get(sm.status, 0) + 1
        
        for status, expected_count in valid_statuses:
            actual_count = status_counts.get(status, 0)
            self.assertEqual(actual_count, expected_count,
                             f"Expected {expected_count} {status} subject matters, but found {actual_count}")

    def test_type_values(self):
        valid_types = ['Consultant','In-house', 'Voluntary']
        type_counts = {}
        subject_matters = self.session.query(SubjectMatter).all()
        for sm in subject_matters:
            with self.subTest(type=sm.type):
                self.assertIn(sm.type, valid_types,
                              f"Invalid type: {sm.type}")
                type_counts[sm.type] = type_counts.get(sm.type, 0) + 1
        
        for sm_type, expected_count in valid_types:
            actual_count = type_counts.get(sm_type, 0)
            self.assertEqual(actual_count, expected_count,
                             f"Expected {expected_count} {sm_type} subject matters, but found {actual_count}")

    def test_date_formats(self):
        subject_matters = self.session.query(SubjectMatter).all()
        for sm in subject_matters:
            with self.subTest(sm_number=sm.sm_number):
                for date_field in ['initial_approval_date', 'effective_date']:
                    date_value = getattr(sm, date_field)
                    if date_value:
                        try:
                            datetime.strptime(date_value, '%Y-%m-%d')
                        except ValueError:
                            self.fail(f"Invalid {date_field} format for SM {sm.sm_number}: {date_value}")
                
                for date_field in ['proposed_start_date', 'proposed_end_date']:
                    date_value = getattr(sm, date_field)
                    if date_value:
                        try:
                            datetime.strptime(date_value, '%Y-%m-%d')
                        except ValueError:
                            self.fail(f"Invalid {date_field} format for SM {sm.sm_number}: {date_value}")

    def test_registrant_id_not_empty(self):
        subject_matters = self.session.query(SubjectMatter).all()
        for sm in subject_matters:
            with self.subTest(sm_number=sm.sm_number):
                self.assertIsNotNone(sm.registrant_id, f"Registrant ID is empty for SM {sm.sm_number}")

if __name__ == '__main__':
    unittest.main()