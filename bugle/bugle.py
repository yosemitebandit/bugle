# -*- coding: utf-8 -*-
''' bugle
a generator of static sites
'''
import yaml


class Bugle(object):
    ''' finding source files (entries)
    validating these files
    compiles tags
    creates indices
    generates slugs
    injects rendered data into templates
    sets up css and js
    saves the lot in an appropriate folder structure
    '''

    def __init__(self, source_path, out_path):
        self.source_path = source_path
        self.out_path = out_path


    def discover_entries(self):
        ''' recursively dig into source_path, looking for entries
        this discovery allows authors to organize files however they'd like

        returns set('/notes/hola.md', 'bike.md')
        '''

        # ..later
        pass

    
    def validate_entry(self, file_handler):
        ''' checks that an entry is properly formatted
        needs one separator in the file
        content before the separator needs to be yaml

        returns (True|False, 'rationale')
        '''
        separator = '---'
        data = file_handler.read().split(separator)
        # validate the presence of exactly one separator
        if len(data) != 2:
            message = ('the separator "%s" needs to appear exactly once' % 
                    separator)
            return (False, message)

        # validate the yaml
        try:
            yaml.load(data[0])
        except:
            message = 'invalid yaml header'
            return (False, message)

        return (True, 'valid.')


    def compile_tags(self, filepaths):
        ''' find all unique tags among the specified files

        returns set('python', 'twilio')
        '''
        tags = []
        for filepath in filepaths:
            with open(filepath, 'r') as f:
                config = yaml.load(f.read().split('---')[0])
                tags.extend(config['tags'])

        return set(tags)


