# -*- coding: utf-8 -*-

from unittest import TestCase

from scrapy import Item
from scrapy.crawler import Crawler
from scrapy.exceptions import DropItem

from scrapy_tracker.items import UpdateStrategy
from scrapy_tracker.pipelines import ItemTrackerPipeline
from tests import TestItem, TestSpider, TEST_ITEM, mock


class SkipUpdatesItem(TestItem):
    update_strategy = UpdateStrategy.SKIP_UPDATES


class TestItemTrackerPipeline(TestCase):
    def setUp(self):
        self.spider = TestSpider()
        self.crawler = Crawler(TestSpider, {})

    def test_from_crawler(self):
        pipeline = ItemTrackerPipeline.from_crawler(Crawler(TestSpider, {
            'TRACKER_ITEM_KEY_BUILDER': 'scrapy_tracker.pipelines.spider_aware_key_builder'
        }))

        pipeline.storage = mock.Mock()
        pipeline.process_item(TEST_ITEM, self.spider)
        pipeline.storage.getset.assert_called_once_with(self.spider.name + '_' + TEST_ITEM.key, TEST_ITEM.checksum)

    def test_process_not_trackable(self):
        pipeline = ItemTrackerPipeline.from_crawler(self.crawler)
        pipeline.storage = mock.Mock()

        expected = Item()
        found = pipeline.process_item(expected, self.spider)
        self.assertEqual(expected, found)

        pipeline.storage.assert_not_called()

    def test_process_new_item(self):
        pipeline = ItemTrackerPipeline.from_crawler(self.crawler)
        pipeline.storage = mock.Mock()
        pipeline.storage.getset.return_value = None

        found = pipeline.process_item(TEST_ITEM, self.spider)
        self.assertEqual(TEST_ITEM, found)

        pipeline.storage.getset.assert_called_once_with(TEST_ITEM.key, TEST_ITEM.checksum)
        self.assertEqual(1, self.crawler.stats.get_value('tracker/testitem/total_items_count'))
        self.assertEqual(1, self.crawler.stats.get_value('tracker/testitem/new_items_count'))

    def test_process_update_append(self):
        pipeline = ItemTrackerPipeline.from_crawler(self.crawler)
        pipeline.storage = mock.Mock()
        pipeline.storage.getset.return_value = 'fake checksum'

        found = pipeline.process_item(TEST_ITEM, self.spider)
        self.assertEqual(TEST_ITEM, found)

        pipeline.storage.getset.assert_called_once_with(TEST_ITEM.key, TEST_ITEM.checksum)
        self.assertEqual(1, self.crawler.stats.get_value('tracker/testitem/total_items_count'))
        self.assertEqual(1, self.crawler.stats.get_value('tracker/testitem/item_updates_count'))

    def test_process_update_skip(self):
        pipeline = ItemTrackerPipeline.from_crawler(self.crawler)
        pipeline.storage = mock.Mock()
        pipeline.storage.getset.return_value = 'fake checksum'

        item = SkipUpdatesItem(TEST_ITEM)
        self.assertIsInstance(pipeline.process_item(item, self.spider), DropItem)
        pipeline.storage.getset.assert_called_once_with(item.key, item.checksum)
        self.assertEqual(None, self.crawler.stats.get_value('tracker/testitem/total_items_count'))

    def test_process_duplicate(self):
        pipeline = ItemTrackerPipeline.from_crawler(self.crawler)
        pipeline.storage = mock.Mock()
        pipeline.storage.getset.return_value = TEST_ITEM.checksum

        self.assertIsInstance(pipeline.process_item(TEST_ITEM, self.spider), DropItem)
        pipeline.storage.getset.assert_called_once_with(TEST_ITEM.key, TEST_ITEM.checksum)
        self.assertEqual(1, self.crawler.stats.get_value('tracker/testitem/total_items_count'))
        self.assertEqual(None, self.crawler.stats.get_value('tracker/testitem/item_updates_count'))
        self.assertEqual(None, self.crawler.stats.get_value('tracker/testitem/new_items_count'))
