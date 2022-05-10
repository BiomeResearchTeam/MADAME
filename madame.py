# coding=utf-8

# MADAME - MetADAta MicrobiomE
# Manuel Striani
# manuel.striani@uniupo.it
# University of Piemonte Orientale

import os
import logging
import subprocess
import sys
from os.path import exists


from IDlist import GetIDlist
from ExperimentMetadataDownload import ExperimentsAndProjectMetadataDownload
from ProjectManager import ProjectManager
from SampleMetadataDownload import SampleMetadataDownload
from DataCheck import DataCheck
from ProjectMetaDataDownload import ProjectMetaDataDownload
from Utilities import Utilities


def main():
    args = sys.argv[1:]
    print(f"Arguments count: {len(sys.argv)}")
    # print("XXXX: " + str(sys.argv[1]))
    fileInputPDF = str(sys.argv[1])

    if (exists('./madame_log.log')):
        os.system('rm ./madame_log.log')
    logger = logging.getLogger(__name__)

    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler('./madame_log.log')
    logger.setLevel(logging.DEBUG)
    c_handler.setLevel(logging.DEBUG)
    f_handler.setLevel(logging.INFO)

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    logger.info('MADAME - MetADAta MicrobiomE')

    # Module 0
    #   - ID list retrievement
    logger.info('STEP 0: [STARTING] Module 0:  ID list retrievement')

    IDlistRetrieve = GetIDlist("GetIDlist")
    listOfProjectIDs = IDlistRetrieve.Query(logger, user_query = "insert query here", data_type = "projects") #projects is default data type
    #OR
    listOfProjectIDs = IDlistRetrieve.IDlistFromUserInput(logger, "insert accessions separated by comma")["enaGroupGet"][2]
   
    

    #Printed details from ENA Browser API available for both methods:
    IDlistRetrieve.QueryDetails(listOfProjectIDs)
    #OR
    IDlistRetrieve.IDlistFromUserInputDetails(listOfProjectIDs)

    # Module 1
    #   - Experiment (project) metadata download
    logger.info('STEP 1: [STARTING] Module 1:  Experiment metadata download')

    #Create main folder and projects subfolders
    Utilities.setMADAMEdirectory(listOfProjectIDs, download_dir="/mnt/c/Users/conog/Desktop")

    metadataDownload = ExperimentsAndProjectMetadataDownload("ExperimentsAndProjectMetadataDownload")
    metadataDownload.runDownloadMetadata(logger, listOfProjectIDs)


######################   ARRIVATA QUA!!




    # Module 2
    # Data check
    # input:
    #   2.1 - List of retrieved data
    #   2.2 - List of project files
    # output: list of warnings (xml file or others...)
    listOfRetrievedData = []
    listOfProjectFiles = []
    logger.info('STEP 2: [STARTING] Module 2:  Sample metadata download')
    dataCheck = DataCheck('DataCheck')
    list_of_warnings = dataCheck.runDataCheck(logger, listOfRetrievedData, listOfProjectFiles)
    print(list_of_warnings)  # si possono salvare anche su disco, magari serializzandoli come oggetti xml
    # in un futuro, quando ci sarà un'interfaccia, è possibile visualizzarli tramite GUI, magari
    # selezionando il livello di granularità di warnings
    # (level 0 -> massimo liv di astrazione, level 1 -> warnings meno gravi, level 2 -> warings più gravi

    # Module 3
    # Project meta-data download
    # input:
    #   3.1 sequencing platform
    #   3.2 library selection
    #   3.3 study title
    #   3.4 other kinds of parameters...
    # output:
    #   metadata - which format?

    logger.info('STEP 3: [STARTING] Module 3:  Project meta-data download')

    sequencingPlatform = []
    librarySelection = []
    studyTitle = []
    metadataDownload = ProjectMetaDataDownload('ProjectMetaDataDownload')
    metadataDownload.runProjectMetaDataDownload(logger, sequencingPlatform, librarySelection, studyTitle)

    # create ProjectManager
    logger.info('STEP 4: [PROJECT-MANAGER] Module 4:  Create Project Manager')
    projectManager = ProjectManager('MyProjectManager')

    listOfProjectIDs = projectManager.getProjectIDs(logger)
    projectManager.createProjectFromListOfIDs(logger, listOfProjectIDs)

    # elenco oggetti Projects
    listOfProject = projectManager.getListOfProject()
    print(listOfProject)

    # creo il file xml del ProjectManager (scrivo tutti gli xml element ciascuno
    # relativo all'i-esimo project
    projectManager.setXMLName = "path.... " + str(projectManager.getProjectManagerName())
    projectManager.projectManagerToXML(logger)


if __name__ == "__main__":
    main()
