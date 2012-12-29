#! /usr/bin/env python
# -*- coding: utf-8 -*-

''' testing meta file validation
'''

import unittest

from bugle import bugle, meta

class MetaValidationTest(unittest.TestCase):
    
    def setUp(self):
        source_path = 'bugle/tests/fixtures/meta-validation/'
        out_path = ''
        self.b = bugle.Bugle(source_path, out_path)

    def tearDown(self):
        pass

    def test_bad_separator(self):
        filepath = '%s/bad-separator.md' % self.b.meta_path
        m = meta.Meta(filepath)
        self.assertEqual(False, m.valid)

    def test_missing_title(self):
        filepath = '%s/missing-title.md' % self.b.meta_path
        m = meta.Meta(filepath)
        self.assertEqual(False, m.valid)

    ''' valid meta data should..validate
    '''
    def test_valid_meta(self):
        filepath = '%s/about.md' % self.b.meta_path
        m = meta.Meta(filepath)
        self.assertEqual(True, m.valid)
