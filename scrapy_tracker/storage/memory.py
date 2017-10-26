from scrapy_tracker.storage import Storage


class MemoryStorage(Storage):

    def __init__(self, _):
        self._values = {}

    def getset(self, key, checksum):
        old_checksum = self._values.get(key)
        self._values[key] = checksum

        return old_checksum
