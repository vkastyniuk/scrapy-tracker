from abc import ABCMeta

import six


@six.add_metaclass(ABCMeta)
class Storage(object):

    def getset(self, key, checksum):
        pass
