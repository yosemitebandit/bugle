# -*- coding: utf-8 -*-
''' meta
one of the meta docs
'''
import re

import markdown
from unidecode import unidecode
import yaml


class Meta(object):
    ''' stores raw dta
    validates
    generates a slug
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


    def __repr__(self):
        return 'Meta %s' % self.filepath


    def validate(self):
        ''' checks that things are properly formatted
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
        required_params = ['title']
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
        creates a 'last_updated' param based on 'created' and 'updated'

        returns None
        '''
        data = self.raw.split(self.separator)
        self.config = yaml.load(data.pop(0))
        # in case the separator was in the markdown, use it in the rejoin
        self.markdown = self.separator.join(data)
        self.rendered_markdown = markdown.markdown(self.markdown)


    def generate_slug(self):
        ''' generate a slug
        technique from http://flask.pocoo.org/snippets/5/

        returns None
        '''
        if 'route' in self.config.keys():
            route = self.config['route']
        else:
            route = self.config['title']

        if route == '':
            self.slug = ''
            return

        punctuation = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
        result = []
        for word in punctuation.split(route.lower()):
            result.extend(unidecode(word).split())

        self.slug = unicode(u'-'.join(result))
