# -*- coding: utf-8 -*-

from redis import StrictRedis

from scrapy_tracker.storage import Storage


class RedisStorage(Storage):

    def __init__(self, settings):
        host = settings.get('TRACKER_RADIS_HOST', 'localhost')
        port = settings.getint('TRACKER_RADIS_PORT', 6379)
        db = settings.getint('TRACKER_RADIS_DB', 0)
        password = settings.get('TRACKER_RADIS_PASSWORD', None)

        self._redis = StrictRedis(host, port, db, password=password)

        drop_all_keys = settings.getbool('TRACKER_RADIS_FLUSH_DB', False)
        if drop_all_keys:
            self._redis.flushdb()

    def getset(self, key, checksum):
        return self._redis.getset(key, checksum)
