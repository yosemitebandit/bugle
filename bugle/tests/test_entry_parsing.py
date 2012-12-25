#! /usr/bin/env python
# -*- coding: utf-8 -*-

''' testing entry validation
'''

import unittest

from bugle import bugle, entry

class ParsingTest(unittest.TestCase):
    
    def setUp(self):
        source_path = 'bugle/tests/fixtures/parsing/'
        out_path = ''
        self.b = bugle.Bugle(source_path, out_path)

    def tearDown(self):
        pass

    
    def test_vanilla_entry_yaml(self):
        # confirm that yaml has been captured and is a dict
        filepath = '%s/vanilla.md' % self.b.entry_path
        e = entry.Entry(filepath)
        self.assertEqual(type(e.config), type({}))

    def test_vanilla_entry_markdown(self):
        filepath = '%s/vanilla.md' % self.b.entry_path
        e = entry.Entry(filepath)
        expected_markdown = ("\n\n### oh, memory\n\n"
            "it's a fickle thing.\n"
            "we should try to make it better..\n"
            "with *texts*.\n")
        self.assertEqual(expected_markdown, e.markdown)

    def test_multiple_separators(self):
        # separators ('---') in the markdown should be allowed
        filepath = '%s/multiple-separators.md' % self.b.entry_path
        e = entry.Entry(filepath)
        expected_markdown = ("\n\n### oh, memory\n\n"
            "it's a fickle thing.\n"
            "we should try to make it better..\n"
            "with *texts*.\n"
            "---\n"
            "or maybe emails!\n")
        self.assertEqual(expected_markdown, e.markdown)

    def test_markdown_rendering(self):
        filepath = '%s/vanilla.md' % self.b.entry_path
        e = entry.Entry(filepath)
        self.assertIn('<h3>', e.rendered_markdown)
