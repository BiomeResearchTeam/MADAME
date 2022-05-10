

import os
import logging
import subprocess
import sys


class DataCheck:
    def __init__(self, name):
        self.name = name

    def runDataCheck(self, logger, listOfRetrievedData, listOfProjectFiles):
        list_of_warnings = [] # anche una lista di oggetti...
        listOfRetData = listOfRetrievedData
        listOfPrFiles = listOfProjectFiles
        logger.info('[RETRIEVED-DATA] Module 2: ' + str(listOfRetData))
        logger.info('[PROJECT-FILES] Module 2: ' + str(listOfPrFiles))
        # ...
        return list_of_warnings


