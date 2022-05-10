import os
import logging
import subprocess
import sys


class Sample:
    def __init__(self, sampleID, sampleName, sampDescription):
        self.IDSample = sampleID
        self.sampleName = sampleName
        self.sampleDescription = sampDescription

    def getSampleDescription(self):
        return self.sampleDescription

    def getSampleName(self):
        return self.sampleName

    def getSampleID(self):
        return self.IDSample

    def toXMLSample(self, logger):
        # qui creo il singolo nodo xml per il sample corrente
        '''
        <samples>
            <sample>
                ....
            </sample>
        </samples>
        '''

        return
