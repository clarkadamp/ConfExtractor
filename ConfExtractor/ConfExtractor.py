'''
Created on 16 Dec 2014

@author: aclark
'''
import logging
import re

from .ConfigList import ConfigList

logger = logging.getLogger(__name__)

class ConfExtractor(ConfigList):

    def fromString(self, s):
        # Read raw data from string
        s_sanitised = self._sanitise(s)
        self.extend(self.stringToList(s_sanitised))

    def fromFile(self, path):
        # Read raw data into list
        with open(path, 'r') as f:
            logger.debug('Opening file located at: {}'.format(path))
            s_sanitised = self._sanitise(f.read())

        self.extend(self.stringToList(s_sanitised))

    def _sanitise(self, s):
        # Nothing as of yet
        # I am looking to add code to clean up " --More-- " prompts
        return s

    def stringToList(self, s, sepre=r'[\n\r]+'):
        # Split raw data into list based on regular expression
        return re.compile(sepre).split(s)
