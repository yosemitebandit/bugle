# -*- coding: utf-8 -*-
''' entry
one of the dynamic entries
'''
import re
from datetime import datetime

import markdown
from unidecode import unidecode
import yaml


class Entry(object):
    ''' stores file data
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

        # validates the config tags - letters, numbers and dashes only
        punctuation = re.compile(r'[\t!"#$%&\'()*\/<=>?@\[\\\]^_`{|},.]+')
        for tag in config['tags']:
            if len(punctuation.split(tag)) > 1:
                self.validation_message = 'tag %s is invalid' % tag
                self.valid = False
                return False


        # validates the formatting of "created" and "updated"
        # should be of the form "September, 2012" or "September 12, 2012"
        if not self._convert_to_datetime(config['created']):
            self.validation_message = 'invalid formatting on "created" param.'
            self.valid = False
            return False

        if ('updated' in config.keys()
                and not self._convert_to_datetime(config['updated'])):
            self.validation_message = 'invalid formatting on "updated" param.'
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

        # create a 'last_updated' param to be used for sorting
        if 'updated' in self.config.keys():
            self.config['last_update'] = self._convert_to_datetime(
                    self.config['updated'])
        else:
            self.config['last_update'] = self._convert_to_datetime(
                    self.config['created'])


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


    def _convert_to_datetime(self, param):
        ''' validates formatting of time params in the config
        should be 'September 19, 2012' or 'September, 2012'
        '''
        try:
            dt = datetime.strptime(param, '%B %d, %Y')
            return dt
        except ValueError:
            pass

        try:
            dt = datetime.strptime(param, '%B, %Y')
            return dt
        except ValueError:
            pass

        return False
