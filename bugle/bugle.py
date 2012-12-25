# -*- coding: utf-8 -*-
''' bugle
a generator of static sites
'''
import os


class Bugle(object):
    ''' finding source files (entries)
    validating these files
    compiles tags
    generates slugs
    creates indices for each tag
    injects rendered data into templates
    sets up css and js
    saves the lot in an appropriate folder structure
    '''

    def __init__(self, source_path, out_path):
        self.source_path = source_path
        self.entry_path = os.path.join(source_path, 'entries')
        self.out_path = out_path


    def discover_entries(self, directory):
        ''' recursively dig into a path, looking for entries
        this discovery allows authors to organize files however they'd like

        returns set('/notes/hola.md', 'bike.md')
        '''
        filepaths = []
        for root, subdirectories, filenames in os.walk(directory):
            for filename in filenames:
                filepaths.append(os.path.join(root, filename))

            for subdirectory in subdirectories:
                self.discover_entries(subdirectory)

        return set(filepaths)


    def compile_tags(self, entries):
        ''' find all unique tags among the specified entries

        returns set('python', 'twilio')
        '''
        tags = []
        for entry in entries:
            tags.extend(entry.config['tags'])

        return set(tags)


    def verify_unique_routes(self, entries):
        ''' checks that all tags and all entries are uniquely routed
        '''
        tags = self.compile_tags(entries)
        tag_slugs = [tag.replace(' ', '-') for tag in tags]

        entry_slugs = [e.slug for e in entries]

        all_slugs = []
        all_slugs.extend(tag_slugs)
        all_slugs.extend(entry_slugs)

        # creating a set will eliminate duplicates
        if len(all_slugs) != len(set(all_slugs)):
            return False
        else:
            return True

