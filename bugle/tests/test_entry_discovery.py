#! /usr/bin/env python
# -*- coding: utf-8 -*-

''' testing the discovery of entry on the source path
'''

import os
import unittest

from bugle import bugle

class DiscoveryTest(unittest.TestCase):
    
    def setUp(self):
        source_path = 'bugle/tests/fixtures/entry-discovery/'
        out_path = ''
        self.b = bugle.Bugle(source_path, out_path)

    def tearDown(self):
        pass

    def test_discover_files(self):
        entries = self.b.discover_files(self.b.entry_path)

        samples = ['uno.md', 'dos.md', 'ideas/2012/tres.md']
        expected_entries = set([os.path.join(self.b.entry_path, s) for s in 
            samples])

        self.assertEqual(entries, expected_entries)
