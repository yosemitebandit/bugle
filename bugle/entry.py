# -*- coding: utf-8 -*-
''' entry
one of the dynamic entries
'''
import re

from unidecode import unidecode
import yaml


class Entry(object):
    ''' stores
    validating these files
    compiles tags
    generates slugs
    creates indices for each tag
    injects rendered data into templates
    sets up css and js
    saves the lot in an appropriate folder structure
    '''

    def __init__(self, filepath):
        # the separator between yaml and markdown
        self.separator = '---'

        self.filepath = filepath

        with open(filepath, 'r') as f:
            self.raw = f.read()

        if self.validate():
            # save the config and markdown
            self.parse()
            # save a slug based on title or route param
            self.generate_slug()
            # process the markdown
            #self.parse_markdown()


    def __repr__(self):
        return 'Entry %s' % self.filepath


    def validate(self):
        ''' checks that an entry is properly formatted
        needs one separator in the file
        content before the separator needs to be yaml

        returns (True|False, 'rationale')
        '''
        data = self.raw.split(self.separator)
        # validate the presence of a separator
        if len(data) < 2:
            self.validation_message = ('the separator "%s" needs to appear at'
                    ' least once' % self.separator)
            self.valid = False
            return False

        # validate the yaml
        try:
            config = yaml.load(data[0])
        except:
            self.validation_message = 'invalid yaml header'
            self.valid = False
            return False

        # validates that all required params are present and not empty
        required_params = ['title', 'blurb', 'tags', 'created']
        for param in required_params:
            if param not in config.keys():
                self.validation_message = ('yaml header is missing parameter'
                    ' "%s"' % param)
                self.valid = False
                return False

            if not config[param]:
                self.validation_message = ('yaml parameter "%s" is invalid' 
                        % param)
                self.valid = False
                return False

        self.validation_message = 'valid.'
        self.valid = True
        return True


    def parse(self):
        ''' saves config and markdown

        returns None
        '''
        data = self.raw.split(self.separator)
        self.config = yaml.load(data.pop(0))
        # in case the separator was in the markdown, use it in the rejoin
        self.markdown = self.separator.join(data)


    def generate_slug(self):
        ''' generate a slug for an entry
        technique from http://flask.pocoo.org/snippets/5/

        returns None
        '''
        if 'route' in self.config.keys():
            route = self.config['route']
        else:
            route = self.config['title']

        punctuation = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
        result = []
        for word in punctuation.split(route.lower()):
            result.extend(unidecode(word).split())

        self.slug = unicode(u'-'.join(result))