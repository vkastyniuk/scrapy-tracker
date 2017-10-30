# -*- coding: utf-8 -*-

from datetime import date
from unittest import TestCase

from scrapy_tracker import utils


class TestUtils(TestCase):

    def test_dict_md5(self):
        md5 = utils.dict_md5({
            'string': 'str',
            'none': None,
            'unicode': u'абв',
            'date': date.today(),
            'dict': {
                'key': 'value'
            }
        })
        self.assertIsNotNone(md5)

        self.assertEqual(md5, utils.dict_md5({
            'date': date.today(),
            'unicode': u'абв',
            'none': None,
            'dict': {
                'key': 'value'
            },
            'string': 'str',
        }))

    def test_dict_md5_error(self):
        with self.assertRaises(TypeError):
            utils.dict_md5({'unknown': TestCase})
