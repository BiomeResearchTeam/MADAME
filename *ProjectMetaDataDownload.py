

import os
import logging
import subprocess
import sys


class ProjectMetaDataDownload:
    def __init__(self, name):
        self.name = name

    def runProjectMetaDataDownload(self, logger, sequencingPlatform, librarySelection, studyTitle):
        list_of_tsv_metadata = [] # anche una lista di oggetti...
        seqPlatform = sequencingPlatform
        listSel = librarySelection
        studyTitles = studyTitle

        logger.info('[SEQUENCING-PLATFORM] Module 3: ' + str(sequencingPlatform))
        logger.info('[LIBRARY-SELECTION] Module 3: ' + str(listSel))
        logger.info('[STUDY-TITLE] Module 3: ' + str(studyTitles))

        # ...
        return list_of_tsv_metadata

