# -*- coding: utf-8 -*-
''' bugle
a generator of static sites
'''
import errno
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
        self.template_path = os.path.join(source_path, 'templates')
        self.meta_path = os.path.join(source_path, 'meta')
        self.css_path = os.path.join(source_path, 'static/css')
        self.js_path = os.path.join(source_path, 'static/js')
        self.out_path = out_path


    def discover_files(self, directory):
        ''' recursively dig into a path, looking for entries
        this discovery allows authors to organize files however they'd like

        returns set('/notes/hola.md', 'bike.md')
        '''
        filepaths = []
        for root, subdirectories, filenames in os.walk(directory):
            for filename in filenames:
                filepaths.append(os.path.join(root, filename))

            for subdirectory in subdirectories:
                self.discover_files(subdirectory)

        return set(filepaths)


    def compile_tags(self, entries):
        ''' find all unique tags among the specified entries
        counts entries belonging to that tag
        sorts based on the count

        returns [{'tag': 'python', 'count': 8}, {'tag': 'twilio', 'count': 4}]
        '''
        tags = []
        for entry in entries:
            tags.extend(entry.config['tags'])

        # de-duplicate
        tags = list(set(tags))

        # count entries associated with each tag
        counted_tags = []
        for tag in tags:
            count = 0
            for entry in entries:
                if tag in entry.config['tags']:
                    count += 1
            counted_tags.append({'name': tag, 'count': count})

        # sort by count attr
        counted_tags.sort(key=lambda t: t['count'], reverse=True)

        return counted_tags


    def verify_unique_routes(self, entries, meta_files):
        ''' routes generated from entries, tags and meta files should be unique
        '''
        tags = self.compile_tags(entries)
        tag_slugs = [tag['name'].replace(' ', '-') for tag in tags]

        entry_slugs = [e.slug for e in entries]
        meta_slugs = [m.slug for m in meta_files]

        all_slugs = []
        all_slugs.extend(tag_slugs)
        all_slugs.extend(entry_slugs)
        all_slugs.extend(meta_slugs)

        # creating a set will eliminate duplicates
        if len(all_slugs) != len(set(all_slugs)):
            return False
        else:
            return True

    def ensure_path_exists(self, path):
        # from http://stackoverflow.com/a/5032238/232638
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
