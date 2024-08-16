import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Beneficiary 

class TestBeneficiaryData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        engine = create_engine('sqlite:///lobbyist_registry.db')
        Session = sessionmaker(bind=engine)
        cls.session = Session()

    @classmethod
    def tearDownClass(cls):
        cls.session.close()

    def test_type_values(self):
        valid_types = [
            'Client',
            'Other',
            'Parent company',
            'Subsidiary company',
            'Controlling interest holder',
            'Coalition member',
            'Controlling Interest',
            'Coalition Member',
            'Person with Significant Control'
        ]
        beneficiaries = self.session.query(Beneficiary).all()
        for beneficiary in beneficiaries:
            with self.subTest(type=beneficiary.type):
                self.assertIn(beneficiary.type, valid_types,
                              f"Invalid type: {beneficiary.type}")

    def test_name_not_empty(self):
        beneficiaries = self.session.query(Beneficiary).all()
        for beneficiary in beneficiaries:
            with self.subTest(name=beneficiary.name):
                self.assertTrue(beneficiary.name.strip(),
                                f"Name should not be empty for type: {beneficiary.type}")

if __name__ == '__main__':
    unittest.main()
