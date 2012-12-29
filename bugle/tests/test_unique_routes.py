#! /usr/bin/env python
# -*- coding: utf-8 -*-

''' testing unique routes in entries and tags
'''

import unittest

from bugle import bugle, entry, meta

class UniqueRoutesTest(unittest.TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_repeated_routes(self):
        # in this source, tags and entry titles overlap -- should fail
        source_path = 'bugle/tests/fixtures/nonunique-routes/'
        out_path = ''
        self.b = bugle.Bugle(source_path, out_path)

        entry_filepaths = self.b.discover_files(self.b.entry_path)
        entries = [entry.Entry(f) for f in entry_filepaths]

        meta_filepaths = self.b.discover_files(self.b.meta_path)
        meta_files = [meta.Meta(f) for f in meta_filepaths]

        self.assertFalse(self.b.verify_unique_routes(entries, meta_files))

    def test_repeated_meta_and_entry_routes(self):
        # a meta file and an entry share a title -- should fail
        source_path = 'bugle/tests/fixtures/nonunique-routes-meta/'
        out_path = ''
        self.b = bugle.Bugle(source_path, out_path)

        entry_filepaths = self.b.discover_files(self.b.entry_path)
        entries = [entry.Entry(f) for f in entry_filepaths]

        meta_filepaths = self.b.discover_files(self.b.meta_path)
        meta_files = [meta.Meta(f) for f in meta_filepaths]

        self.assertFalse(self.b.verify_unique_routes(entries, meta_files))

    def test_unique_routes(self):
        source_path = 'bugle/tests/fixtures/unique-routes/'
        out_path = ''
        self.b = bugle.Bugle(source_path, out_path)

        entry_filepaths = self.b.discover_files(self.b.entry_path)
        entries = [entry.Entry(f) for f in entry_filepaths]

        meta_filepaths = self.b.discover_files(self.b.meta_path)
        meta_files = [meta.Meta(f) for f in meta_filepaths]

        self.assertTrue(self.b.verify_unique_routes(entries, meta_files))
