'''
Created on 11 Mar 2015

@author: aclark
'''
import re
import logging

class ConfigList(list):

    def __init__(self, l=[]):
        self.extend(l)
        self.logger = logging.getLogger('ConfExtractor.ConfigList')

    def _getIndexes(self, regex):
        return [ind for ind, l in enumerate(self) if re.search(regex, l)]

    def asGenerator(self):
        # Returns parts of the list, either line by line, or by blocks
        if self.startBlockRegex and self.endBlockRegex:
            startBlockIndexes = self._getIndexes(self.startBlockRegex)
            endBlockIndexes = self._getIndexes(self.endBlockRegex)
            for startIndex in startBlockIndexes:
                retList = ConfigList()
                endIndex = [i for i in endBlockIndexes if i > startIndex][0] + 1
                retList.extend(self[startIndex:endIndex])
                yield retList
        else:
            for line in self:
                yield line

    def asString(self, eol='\n'):
        return eol.join(self)

    def begin(self, regex):
        # Simulates Cisco IOS show | begin string
        # Also has the option of excluding based on regex e
        return ConfigList([x for x in self if not re.search(regex, x)])

    def configBlocks(self, startBlockRegex, endBlockRegex):
        self.startBlockRegex = startBlockRegex
        self.endBlockRegex = endBlockRegex

        retList = ConfigList()
        retList.startBlockRegex = startBlockRegex
        retList.endBlockRegex = endBlockRegex
        for l in self.asGenerator():
            retList.extend(l)
        return retList

    def exclude(self, regex):
        # Simulates Cisco IOS show | exclude string
        # Also has the option of excluding based on regex e
        return ConfigList([x for x in self if not re.search(regex, x)])

    def include(self, regex):
        # Simulates Cisco IOS show | include string
        # Also has the option of excluding based on regex e
        return ConfigList([x for x in self if re.search(regex, x)])
    def _getIndentLen(self, t):
        # Return count of leading whitespace
        return len(re.search(r'^(\s*)(.*?)$', t).groups('')[0])

    def _subSection(self, i):
        iLen = self._getIndentLen(self[i])
        # workout where the section ends, It is subsequent lines that are up
        # to the same indent level
        #
        # Identified by first in a list of subsequent lines offset by the
        # original index, plus 1
        secEnd = [i for i,t in list(enumerate(self[i+1:]))
                if self._getIndentLen(t) <= iLen][0] + i + 1
        # return a new list based on the section start and end
        l = ConfigList(self[i:secEnd])
        self.logger.debug('_subsection: Index {}: Lines {}'.format(i, len(l)))
        return l

    def section(self, regex):
            # Generate indexes for lines that match the regex
            idxs = [i for i, x in enumerate(self)
                              if re.search(regex, x)]

            retList = ConfigList()
            # Iterate through the idxs list that may be modified after each
            # index.  This tries to ensure that nested regex matches do not
            # create double entries in the overall section call
            while len(idxs):
                currIndex = idxs[0]
                self.logger.debug('section: Index {}: {}'.format(idxs[0],
                                                            self[idxs[0]]))
                l = self._subSection(currIndex)
                retList.extend(l)
                # Skip indexes that are after the current index and fall within
                # lines already contained in the last _subSection call
                idxs = [i for i in idxs if i >= currIndex + len(l)]

            return retList

    def __str__(self):
        # provide a string representation of the list
        return self.asString()
