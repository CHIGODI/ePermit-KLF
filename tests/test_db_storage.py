import unittest
from unittest.mock import patch, MagicMock
from models.engine.db_storage import DBStorage

class TestDBStorage(unittest.TestCase):

    def setUp(self):
        """Set up test case environment"""
        self.db_storage = DBStorage()
        self.db_storage.reload()

    @patch('models.engine.db_storage.create_engine')
    def test_init(self, mock_create_engine):
        """Test initialization of DBStorage"""
        self.assertIsInstance(self.db_storage, DBStorage)
        self.assertIsNotNone(self.db_storage._DBStorage__engine)

    @patch('models.engine.db_storage.create_engine')
    def test_init_with_test_env(self, mock_create_engine):
        """Test initialization of DBStorage with 'test' environment"""
        with patch('os.getenv') as mock_getenv:
            mock_getenv.return_value = 'test'
            db_storage = DBStorage()
            self.assertIsInstance(db_storage, DBStorage)
            self.assertIsNotNone(db_storage._DBStorage__engine)

    @patch('models.engine.db_storage.create_engine')
    def test_new(self, mock_create_engine):
        """Test new method"""
        obj = MagicMock()
        self.db_storage.new(obj)
        self.assertIn(obj, self.db_storage._DBStorage__session)

    @patch('models.engine.db_storage.create_engine')
    def test_save(self, mock_create_engine):
        """Test save method"""
        self.db_storage._DBStorage__session.commit = MagicMock()
        self.db_storage.save()
        self.db_storage._DBStorage__session.commit.assert_called_once()

    @patch('models.engine.db_storage.create_engine')
    def test_delete(self, mock_create_engine):
        """Test delete method"""
        obj = MagicMock()
        self.db_storage.delete(obj)
        self.db_storage._DBStorage__session.delete.assert_called_once_with(obj)

    @patch('models.engine.db_storage.create_engine')
    def test_reload(self, mock_create_engine):
        """Test reload method"""
        self.db_storage._DBStorage__session.close = MagicMock()
        self.db_storage.reload()
        self.db_storage._DBStorage__session.close.assert_called_once()

    @patch('models.engine.db_storage.create_engine')
    def test_all(self, mock_create_engine):
        """Test all method"""
        result = self.db_storage.all()
        self.assertIsInstance(result, dict)

    @patch('models.engine.db_storage.create_engine')
    def test_count(self, mock_create_engine):
        """Test count method"""
        count = self.db_storage.count()
        self.assertIsInstance(count, int)

if __name__ == '__main__':
    unittest.main()
