# -*- coding: utf-8 -*-
''' bugle
a generator of static sites
'''
import yaml


class Bugle(object):
    ''' validating source files
    complies tags and sections
    creates indices
    generates slugs
    injects rendered data into templates
    sets up css and js
    saves the lot in an appropriate folder structure
    '''

    def __init__(self, source_dir, out_dir):
        self.source_dir = source_dir
        self.out_dir = out_dir

    
    def validate_entry(self, file_handler):
        ''' checks that an entry is properly formatted
        returns (False, 'rationale')
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


