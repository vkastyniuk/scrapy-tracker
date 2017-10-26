# -*- coding: utf-8 -*-

import hashlib
import json
from datetime import datetime, date
from enum import Enum

import scrapy


class cached_property(object):
    """
    Decorator that converts a method with a single self argument into a
    property cached on the instance.

    Optional ``name`` argument allows you to make cached properties of other
    methods. (e.g.  url = cached_property(get_absolute_url, name='url') )
    """

    def __init__(self, func, name=None):
        self.func = func
        self.__doc__ = getattr(func, '__doc__')
        self.name = name or func.__name__

    def __get__(self, instance, cls=None):
        if instance is None:
            return self

        res = instance.__dict__[self.name] = self.func(instance)
        return res


class UpdateStrategy(Enum):
    APPEND_UPDATES = 1
    SKIP_UPDATES = 2


class TrackableItem(scrapy.Item):
    update_strategy = UpdateStrategy.APPEND_UPDATES

    @classmethod
    def get_key_fields(cls):
        return [k for k, v in cls.fields.items()
                if 'track_key' in v and v['track_key']]

    @classmethod
    def get_tracked_fields(cls):
        return [k for k, v in cls.fields.items()
                if 'track_field' not in v or v['track_field']]

    @cached_property
    def key(self):
        key_fields = self.get_key_fields()
        if not key_fields:
            raise AssertionError('At least one field should be in track key.')

        values = {k: v for k, v in self._values.items() if k in key_fields}
        values['item_type'] = type(self).__name__

        return self._md5(values)

    @cached_property
    def checksum(self):
        tracked_fields = self.get_tracked_fields()
        values = {k: v for k, v in self._values.items() if k in tracked_fields}

        return self._md5(values)

    @staticmethod
    def _md5(values):
        def _default(obj):
            if isinstance(obj, date):
                epoch = datetime.utcfromtimestamp(0).date()
                return (obj - epoch).days
            raise TypeError('Can\'t serialize %s' % obj)

        data = json.dumps(values, sort_keys=True, ensure_ascii=False, default=_default).encode('utf-8')
        return hashlib.md5(data).hexdigest()
