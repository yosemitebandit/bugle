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

    def test_multiple_separators(self):
        # we should only look for the first instance of the separator
        # so multiple separators should be allowed
        filepath = '%s/multiple-separators.md' % self.b.source_path
        with open(filepath, 'r') as f:
            result = self.b.validate_entry(f)
            self.assertEqual(True, result[0])

    def test_bad_yaml(self):
        filepath = '%s/bad_yaml.md' % self.b.source_path
        with open(filepath, 'r') as f:
            result = self.b.validate_entry(f)
            self.assertEqual(False, result[0])


    ''' valid entries should ..validate
    '''
    def test_valid_entry(self):
        filepath = '%s/uno.md' % self.b.source_path
        with open(filepath, 'r') as f:
            result = self.b.validate_entry(f)
            self.assertEqual(True, result[0])


    ''' config files that lack required params
    '''
    def test_missing_title(self):
        filepath = '%s/missing-title.md' % self.b.source_path
        with open(filepath, 'r') as f:
            result = self.b.validate_entry(f)
            self.assertEqual(False, result[0])

    def test_missing_blurb(self):
        filepath = '%s/missing-blurb.md' % self.b.source_path
        with open(filepath, 'r') as f:
            result = self.b.validate_entry(f)
            self.assertEqual(False, result[0])

    def test_missing_tags(self):
        filepath = '%s/missing-tags.md' % self.b.source_path
        with open(filepath, 'r') as f:
            result = self.b.validate_entry(f)
            self.assertEqual(False, result[0])

    def test_missing_creation_time(self):
        filepath = '%s/missing-creation-time.md' % self.b.source_path
        with open(filepath, 'r') as f:
            result = self.b.validate_entry(f)
            self.assertEqual(False, result[0])


    ''' config files with empty required params
    '''
    def test_empty_title(self):
        filepath = '%s/empty-title.md' % self.b.source_path
        with open(filepath, 'r') as f:
            result = self.b.validate_entry(f)
            self.assertEqual(False, result[0])

    def test_empty_blurb(self):
        filepath = '%s/empty-blurb.md' % self.b.source_path
        with open(filepath, 'r') as f:
            result = self.b.validate_entry(f)
            self.assertEqual(False, result[0])

    def test_empty_tags(self):
        filepath = '%s/empty-tags.md' % self.b.source_path
        with open(filepath, 'r') as f:
            result = self.b.validate_entry(f)
            self.assertEqual(False, result[0])

    def test_empty_creation_time(self):
        filepath = '%s/empty-creation-time.md' % self.b.source_path
        with open(filepath, 'r') as f:
            result = self.b.validate_entry(f)
            self.assertEqual(False, result[0])
