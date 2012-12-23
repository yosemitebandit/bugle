# -*- coding: utf-8 -*-
''' bugle
a generator of static sites
'''
import yaml


class Bugle(object):
    ''' validating source files
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


