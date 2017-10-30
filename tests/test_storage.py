from unittest import TestCase
from unittest.mock import patch, MagicMock

from scrapy.settings import Settings

from scrapy_tracker.storage.memory import MemoryStorage
from scrapy_tracker.storage.redis import RedisStorage
from scrapy_tracker.storage.sqlalchemy import SqlAlchemyStorage
from tests import TEST_KEY, TEST_CHECKSUM


class TestMemoryStorage(TestCase):
    def setUp(self):
        self.storage = MemoryStorage(None)

    def test_getset(self):
        result = self.storage.getset(TEST_KEY, TEST_CHECKSUM)
        self.assertIsNone(result)

        found = self.storage.getset(TEST_KEY, 'new_checksum')
        self.assertEqual(TEST_CHECKSUM, found)

        found = self.storage.getset(TEST_KEY, TEST_CHECKSUM)
        self.assertEqual('new_checksum', found)

        result = self.storage.getset('new_key', TEST_CHECKSUM)
        self.assertIsNone(result)


class TestSqlAlchemyStorage(TestCase):
    def setUp(self):
        self.storage = SqlAlchemyStorage(Settings({
            'TRACKER_SQLALCHEMY_ENGINE': 'sqlite:///:memory:',
            'TRACKER_SQLALCHEMY_FLUSH_DB': True
        }))

    def test_getset(self):
        result = self.storage.getset(TEST_KEY, TEST_CHECKSUM)
        self.assertIsNone(result)

        found = self.storage.getset(TEST_KEY, 'new_checksum')
        self.assertEqual(TEST_CHECKSUM, found)

        found = self.storage.getset(TEST_KEY, TEST_CHECKSUM)
        self.assertEqual('new_checksum', found)

        result = self.storage.getset('new_key', TEST_CHECKSUM)
        self.assertIsNone(result)


class TestRedisStorage(TestCase):
    def setUp(self):
        with patch("scrapy_tracker.storage.redis.StrictRedis") as mock_redis:
            data = {}

            def getset(key, val):
                old_val = data.get(key)
                data[key] = val

                return old_val

            mock = MagicMock()
            mock.getset.side_effect = getset
            mock_redis.return_value = mock

            self.storage = RedisStorage(Settings({
                'TRACKER_RADIS_FLUSH_DB': True
            }))

    def test_getset(self):
        result = self.storage.getset(TEST_KEY, TEST_CHECKSUM)
        self.assertIsNone(result)

        found = self.storage.getset(TEST_KEY, 'new_checksum')
        self.assertEqual(TEST_CHECKSUM, found)

        found = self.storage.getset(TEST_KEY, TEST_CHECKSUM)
        self.assertEqual('new_checksum', found)

        result = self.storage.getset('new_key', TEST_CHECKSUM)
        self.assertIsNone(result)
