import os
import logging
import subprocess
import sys


class Experiment:
    def __init__(self, experimentID, expName, expDescription):
        self.IDExperiment = experimentID
        self.experimentName = expName
        self.experimentDescription = expDescription

    def getExperimentDescription(self):
        return self.experimentDescription

    def getExperimentName(self):
        return self.experimentName

    def getExperimentID(self):
        return self.IDExperiment

    '''
    <exp1>
        <samples> <sample> .... </sample> </samples> 
    </exp1>
    '''
    def toXMLExmperiment(self, logger):
        # qui creo il singolo nodo xml per l'experiment corrente
        return
