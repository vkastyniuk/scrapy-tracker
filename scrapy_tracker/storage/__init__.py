# -*- coding: utf-8 -*-

from abc import ABCMeta

import six


@six.add_metaclass(ABCMeta)
class Storage(object):
    """
    Base Key-Value storage class.
    """

    def getset(self, key, checksum):
        """
        Sets the value at key ``key`` to ``checksum``
        and returns the old value at key ``key``.
        """
        pass
