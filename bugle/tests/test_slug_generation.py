#! /usr/bin/env python
# -*- coding: utf-8 -*-

''' testing the creation of slugs for entries
'''

import unittest

from bugle import bugle

class SlugGenerationTest(unittest.TestCase):
    
    def setUp(self):
        source_path = 'bugle/tests/fixtures/slug-generation/'
        out_path = ''
        self.b = bugle.Bugle(source_path, out_path)

    def tearDown(self):
        pass

    def test_basic_slug(self):
        filepath = self.b.source_path + 'basic.md'
        with open(filepath, 'r') as f:
            slug = self.b.generate_slug(f)
        self.assertEqual(slug, 'sms-time-capsule')

    def test_slug_with_punctuation(self):
        filepath = self.b.source_path + 'punctuation.md'
        with open(filepath, 'r') as f:
            slug = self.b.generate_slug(f)
        self.assertEqual(slug, 'never-an-sms-time-capsule')

    def test_slug_override(self):
        filepath = self.b.source_path + 'override.md'
        with open(filepath, 'r') as f:
            slug = self.b.generate_slug(f)
        self.assertEqual(slug, 'never-the-sms-time-capsule')

    def test_slug_with_maths(self):
        filepath = self.b.source_path + 'maths.md'
        with open(filepath, 'r') as f:
            slug = self.b.generate_slug(f)
        self.assertEqual(slug, 'lambda-is-difficult')

    def test_slug_with_khmer(self):
        filepath = self.b.source_path + 'khmer.md'
        with open(filepath, 'r') as f:
            slug = self.b.generate_slug(f)
        self.assertEqual(slug, 'khemrbhaasaa')
