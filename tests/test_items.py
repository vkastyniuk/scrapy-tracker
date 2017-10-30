# -*- coding: utf-8 -*-

from unittest import TestCase

from scrapy import Field

from scrapy_tracker.items import TrackableItem
from tests import TestItem, TEST_CHECKSUM, TEST_KEY, TEST_ITEM


class TestTrackableItem(TestCase):

    def test_get_key_fields(self):
        self.assertListEqual(['category', 'name'], sorted(TEST_ITEM.get_key_fields()))

    def test_get_tracked_fields(self):
        self.assertListEqual(['address', 'category', 'name', 'phone'], sorted(TEST_ITEM.get_tracked_fields()))

    def test_key(self):
        self.assertEqual(TEST_KEY, TEST_ITEM.key)

        item = TestItem(TEST_ITEM)
        item['name'] = 'Updated'
        self.assertEqual(TEST_KEY, TEST_ITEM.key)

    def test_key_error(self):
        class ItemWithoutKey(TrackableItem):
            name = Field()

        item = ItemWithoutKey()
        with self.assertRaises(AssertionError):
            item.key()

    def test_checksum(self):
        self.assertEqual(TEST_CHECKSUM, TEST_ITEM.checksum)

        item = TestItem(TEST_ITEM)
        item['phone'] = 'Updated'
        self.assertEqual(TEST_CHECKSUM, TEST_ITEM.checksum)
