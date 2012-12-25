#! /usr/bin/env python
# -*- coding: utf-8 -*-

''' testing unique routes in entries and tags
'''

import unittest

from bugle import bugle, entry

class UniqueRoutesTest(unittest.TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_repeated_routes(self):
        source_path = 'bugle/tests/fixtures/nonunique-routes/'
        out_path = ''
        self.b = bugle.Bugle(source_path, out_path)

        entry_filepaths = self.b.discover_entries(self.b.entry_path)
        entries = [entry.Entry(f) for f in entry_filepaths]

        self.assertFalse(self.b.verify_unique_routes(entries))

    def test_unique_routes(self):
        source_path = 'bugle/tests/fixtures/unique-routes/'
        out_path = ''
        self.b = bugle.Bugle(source_path, out_path)

        entry_filepaths = self.b.discover_entries(self.b.entry_path)
        entries = [entry.Entry(f) for f in entry_filepaths]

        self.assertTrue(self.b.verify_unique_routes(entries))
