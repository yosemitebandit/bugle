#! /usr/bin/env python
# -*- coding: utf-8 -*-

''' testing entry validation
'''

import unittest

from bugle import bugle

class ValidationTest(unittest.TestCase):
    
    def setUp(self):
        source_path = 'bugle/tests/fixtures/validation/'
        out_path = ''
        self.b = bugle.Bugle(source_path, out_path)

    def tearDown(self):
        pass

    def test_bad_separator(self):
        filepath = '%s/bad_separator.md' % self.b.source_path
        with open(filepath, 'r') as f:
            result = self.b.validate_entry(f)
            self.assertEqual(False, result[0])

    def test_no_separator(self):
        filepath = '%s/no_separator.md' % self.b.source_path
        with open(filepath, 'r') as f:
            result = self.b.validate_entry(f)
            self.assertEqual(False, result[0])

    def test_bad_yaml(self):
        filepath = '%s/bad_yaml.md' % self.b.source_path
        with open(filepath, 'r') as f:
            result = self.b.validate_entry(f)
            self.assertEqual(False, result[0])

    def test_valid_entry(self):
        filepath = '%s/uno.md' % self.b.source_path
        with open(filepath, 'r') as f:
            result = self.b.validate_entry(f)
            self.assertEqual(True, result[0])
