import logging

from scrapy.exceptions import DropItem
from scrapy.utils.misc import load_object

from scrapy_tracker.items import UpdateStrategy, TrackableItem

logger = logging.getLogger(__name__)


def simple_key_builder(item, spider):
    return '%s_%s' % (spider.name, item.key)


def spider_aware_key_builder(item, spider):
    return '%s_%s' % (spider.name, item.key)


class ItemTrackerPipeline(object):

    def __init__(self, crawler):
        self.crawler = crawler

        engine = crawler.settings.get('TRACKER_STORAGE_ENGINE', 'scrapy_tracker.storage.memory.MemoryStorage')
        self.storage = load_object(engine)(crawler.settings)

        builder = crawler.settings.get('TRACKER_ITEM_KEY_BUILDER', 'scrapy_tracker.pipelines.simple_key_builder')
        self.key_builder = load_object(builder)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_item(self, item, spider):
        if isinstance(item, TrackableItem):
            item_type = type(item).__name__.lower()

            self.crawler.stats.inc_value('tracker/%s/total_items_count' % item_type)
            item_key = self.key_builder(spider, item)

            old_checksum = self.storage.getset(item_key, item.checksum)
            if old_checksum:
                if old_checksum.decode('utf-8') == item.checksum:
                    # skip item duplicate
                    return DropItem('Skip item duplicate: %s' % item)

                self.crawler.stats.inc_value('tracker/%s/item_updates_count' % item_type)
                if item.update_strategy is UpdateStrategy.SKIP_UPDATES:
                    # skip item update
                    return DropItem('Skip item update: %s' % item)

                # process item update
                return item
            else:
                # process new item
                self.crawler.stats.inc_value('tracker/%s/new_items_count' % item_type)
                return item
