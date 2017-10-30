from scrapy import Field, Spider

from scrapy_tracker.items import TrackableItem


class TestSpider(Spider):
    name = 'test_spider'

    def parse(self, response):
        pass


class TestItem(TrackableItem):
    name = Field(track_key=True)
    category = Field(track_key=True)
    address = Field(track_field=True)
    phone = Field()
    url = Field(track_field=False)


TEST_KEY = 'c750effd2a15836d9b2cadd91435ba4b'
TEST_CHECKSUM = 'efe42d245bea74adac474214c5079327'
TEST_ITEM = TestItem({
    'name': 'Foo Bar',
    'category': 'company',
    'address': 'Hrodna, Belarus',
    'phone': '+375001112233',
    'url': 'http://foobar.com',
})
