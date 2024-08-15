import unittest
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker
from models import Base

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///lobbyist_registry.db')
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.inspector = inspect(self.engine)

    def tearDown(self):
        self.session.close()

    def test_all_tables_have_rows(self):
        for table_name in self.inspector.get_table_names():
            if not table_name.endswith('_fts'):  # Exclude FTS tables
                query = text(f"SELECT COUNT(*) FROM {table_name}")
                row_count = self.session.execute(query).scalar()
                self.assertGreater(row_count, 0, f"Table '{table_name}' has no rows")

if __name__ == '__main__':
    unittest.main()