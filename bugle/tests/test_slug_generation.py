#! /usr/bin/env python
# -*- coding: utf-8 -*-

''' testing the creation of slugs for entries
'''

import unittest

from bugle import bugle, entry, meta

class SlugGenerationTest(unittest.TestCase):
    
    def setUp(self):
        source_path = 'bugle/tests/fixtures/slug-generation/'
        out_path = ''
        self.b = bugle.Bugle(source_path, out_path)

    def tearDown(self):
        pass

    def test_meta_slug(self):
        filepath = self.b.meta_path + '/about.md'
        m = meta.Meta(filepath)
        self.assertEqual(m.slug, 'about')

    def test_meta_root_slug(self):
        filepath = self.b.meta_path + '/home.md'
        m = meta.Meta(filepath)
        self.assertEqual(m.slug, '')

    def test_basic_slug(self):
        filepath = self.b.entry_path + '/basic.md'
        e = entry.Entry(filepath)
        self.assertEqual(e.slug, 'sms-time-capsule')

    def test_slug_with_punctuation(self):
        filepath = self.b.entry_path + '/punctuation.md'
        e = entry.Entry(filepath)
        self.assertEqual(e.slug, 'never-an-sms-time-capsule')

    def test_slug_override(self):
        filepath = self.b.entry_path + '/override.md'
        e = entry.Entry(filepath)
        self.assertEqual(e.slug, 'never-the-sms-time-capsule')

    def test_slug_with_maths(self):
        filepath = self.b.entry_path + '/maths.md'
        e = entry.Entry(filepath)
        self.assertEqual(e.slug, 'lambda-is-difficult')

    def test_slug_with_khmer(self):
        filepath = self.b.entry_path + '/khmer.md'
        e = entry.Entry(filepath)
        self.assertEqual(e.slug, 'khemrbhaasaa')
