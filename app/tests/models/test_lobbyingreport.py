import unittest
from app.models import LobbyingReport, LobbyingReportStatus, LobbyingReportType
from app import app, db
from datetime import date

class TestLobbyingReport(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app_context = app.app_context()
        cls.app_context.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        with cls.app_context():
            db.drop_all()

    def test_smnumber_is_string(self):
        with self.assertRaises(ValueError):
            LobbyingReport(smnumber=12345)

    def test_smnumber_starts_with_SM(self):
        with self.assertRaises(ValueError):
            LobbyingReport(smnumber='ABC12345')

    def test_smnumber_has_5_digits_after_SM(self):
        with self.assertRaises(ValueError):
            LobbyingReport(smnumber='SM123')

    def test_smnumber_valid(self):
        report = LobbyingReport(smnumber='SM12345')
        self.assertEqual(report.smnumber, 'SM12345')

    def test_status_invalid(self):
        with self.assertRaises(ValueError):
            LobbyingReport(status='Invalid')

    def test_status_valid(self):        
        report = LobbyingReport(status=LobbyingReportStatus.ACTIVE)
        self.assertEqual(report.status, LobbyingReportStatus.ACTIVE)

        report = LobbyingReport(status=LobbyingReportStatus.CLOSED)
        self.assertEqual(report.status, LobbyingReportStatus.CLOSED)

        report = LobbyingReport(status=LobbyingReportStatus.CLOSED_BY_LRO)
        self.assertEqual(report.status, LobbyingReportStatus.CLOSED_BY_LRO)
    
    def test_type_invalid(self):
        with self.assertRaises(ValueError):
            LobbyingReport(type='Invalid')

    def test_type_valid(self):
        report = LobbyingReport(type=LobbyingReportType.CONSULTANT)
        self.assertEqual(report.type, LobbyingReportType.CONSULTANT)
    
        report = LobbyingReport(type=LobbyingReportType.IN_HOUSE)
        self.assertEqual(report.type, LobbyingReportType.IN_HOUSE)

        report = LobbyingReport(type=LobbyingReportType.VOLUNTARY)
        self.assertEqual(report.type, LobbyingReportType.VOLUNTARY)

    def test_proposed_start_date_relationship(self):
        report = LobbyingReport(
            proposed_start_date=date(2023, 6, 1),
            proposed_end_date=date(2023, 6, 30),
            initial_approval_date=date(2023, 6, 2),
            effective_date=date(2023, 6, 3)
        )
        with self.app_context:
            db.session.add(report)
            db.session.commit()

            with self.assertRaises(ValueError):
                report.proposed_start_date = date(2023, 7, 1)
            
            report.proposed_start_date = date(2023, 6, 1)
            db.session.commit()

    def test_proposed_end_date_relationship(self):
        report = LobbyingReport(
            proposed_start_date=date(2023, 6, 1),
            proposed_end_date=date(2023, 6, 30),
            initial_approval_date=date(2023, 6, 2),
            effective_date=date(2023, 6, 3)
        )
        with self.app_context:
            db.session.add(report)
            db.session.commit()

            with self.assertRaises(ValueError):
                report.proposed_end_date = date(2023, 5, 31)

            report.proposed_end_date = date(2023, 6, 30)
            db.session.commit()

    def test_initial_approval_date_relationship(self):
        report = LobbyingReport(
            proposed_start_date=date(2023, 6, 1),
            proposed_end_date=date(2023, 6, 30),
            initial_approval_date=date(2023, 6, 2),
            effective_date=date(2023, 6, 3)
        )
        with self.app_context:
            db.session.add(report)
            db.session.commit()

            with self.assertRaises(ValueError):
                report.initial_approval_date = date(2023, 6, 4)

            report.initial_approval_date = date(2023, 6, 2)
            db.session.commit()

    def test_effective_date_relationship(self):
        report = LobbyingReport(
            proposed_start_date=date(2023, 6, 1),
            proposed_end_date=date(2023, 6, 30),
            initial_approval_date=date(2023, 6, 2),
            effective_date=date(2023, 6, 3)
        )
        with self.app_context:
            db.session.add(report)
            db.session.commit()
            
            with self.assertRaises(ValueError):
                report.effective_date = date(2023, 6, 1)

            report.effective_date = date(2023, 6, 3)
            db.session.commit()

if __name__ == '__main__':
    unittest.main()