# -*- coding: utf-8 -*-
import calendar
import hashlib
import json
from datetime import date


def dict_md5(value):
    def _default(obj):
        if isinstance(obj, date):
            return calendar.timegm(obj.timetuple())

        raise TypeError('Can\'t serialize %s' % obj)

    data = json.dumps(value, sort_keys=True, ensure_ascii=False, default=_default).encode('utf-8')
    return hashlib.md5(data).hexdigest()
