#! /usr/bin/env python
# -*- coding: utf-8 -*-

''' testing the compilation of tags from several files
'''

import unittest

from bugle import bugle, entry

class CompilationTest(unittest.TestCase):
    
    def setUp(self):
        source_path = 'bugle/tests/fixtures/tag-compilation/'
        out_path = ''
        self.b = bugle.Bugle(source_path, out_path)

    def tearDown(self):
        pass

    def test_discover_tags(self):
        samples = ['uno.md', 'dos.md', 'tres.md']
        filepaths = ['%s%s' % (self.b.source_path, s) for s in samples]

        entries = []
        for filepath in filepaths:
            entries.append(entry.Entry(filepath))

        tags = self.b.compile_tags(entries)
        self.assertEqual(tags, set(['notes', 'projects', 'python', 'twilio']))
