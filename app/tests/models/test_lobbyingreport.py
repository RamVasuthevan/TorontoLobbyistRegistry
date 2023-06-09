import unittest
from app.models import LobbyingReport

class TestLobbyingReport(unittest.TestCase):
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
        report = LobbyingReport(status='Active')
        self.assertEqual(report.status, 'Active')

        report = LobbyingReport(status='Closed')
        self.assertEqual(report.status, 'Closed')

        report = LobbyingReport(status='Closed by LRO')
        self.assertEqual(report.status, 'Closed by LRO')

if __name__ == '__main__':
    unittest.main()
