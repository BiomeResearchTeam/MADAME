import os
import logging
from os.path import exists

from IDlist import GetIDlist
from ExperimentMetadataDownload import Exp_Proj_MetadataDownload
from SampleMetadataDownload import SampleMetadataDownload
from Utilities import Directory
from SampleMetadataParser import SampleMetadataParser
from Project import Project


def main():

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

       

        ###########################################
        #########PROVE DA QUI:

        prova = GetIDlist("GetIDlist")

        print("✨   ID list from user input, contains also two invalid accessions")
        listOfProjectIDs = prova.IDlistFromUserInput(logger, "ERP107880,DRP004449,SRP187334,PRJNA505133,SRR8658062,SRR8658064,SRR45,123")
        #Printed details from ENA Browser API
        prova.IDlistFromUserInputDetails(listOfProjectIDs)

        print("------------------------")
        print("✨   (small) ID list from query:")
        listOfProjectIDs = prova.Query(logger, user_query = "pollen microbiome") #data type is optional, default is "projects"
        #Printed details from ENA Browser API
        prova.QueryDetails(listOfProjectIDs)

        print("------------------------")
        print("✨   trying a query with no results:")
        listOfProjectIDs_ = prova.Query(logger, user_query = "pippo")
        prova.QueryDetails(listOfProjectIDs_)

        #print("------------------------")
        #print("✨   trying a query with wrong data_type parameter:")
        #listOfProjectIDs_ = pippo.Query(logger, user_query = "pollen microbiome", data_type="pippo")

        print("------------------------")
        print("✨   obtaining a list of AVAILABLE projects:")
        listOfProjectIDs = prova.getAvailableProjects(logger, listOfProjectIDs)

        print("------------------------")
        print("✨   trying metadata download (project + experiments)\n")

        setDirectory = Directory("CreateDirectory")
        ########
        #SET YOUR PREFERRED DOWNLOAD DIRECTORY HERE IF YOU'RE TRYING THE SCRIPT!
        ########
        setDirectory.setMADAMEdirectory("/mnt/c/Users/conog/Desktop")
        
        print("⬇️   Downloading available project and experiments metadata...")
        MetadataDownload = Exp_Proj_MetadataDownload("MetadataDownload")
        MetadataDownload.runDownloadMetadata(listOfProjectIDs)
        print("\n✅   All done!")

        print("------------------------")
        print("✨   trying metadata download (samples)\n")

        print("⬇️   Downloading available samples metadata...")
        MetadataDownload = SampleMetadataDownload("MetadataDownload")
        MetadataDownload.runDownloadMetadata(listOfProjectIDs)
        print("\n✅   All done!")

        print("------------------------")
        print("✨   trying metadata parsing...\n")
        MetadataParsing = SampleMetadataParser("MetadataParsing")
        MetadataParsing.runParseMetadata(listOfProjectIDs)

        print("------------------------")
        print("✨   trying some functions of Project.py!\n")
        projectID = listOfProjectIDs[0]
        first = Project("first")
        print(f"📝 our first project in listOfProjectIDs: {projectID}")      
        print(f"📝 availability: {first.getProjectAvailability(projectID)}")
        print(f"📝 project size, sra: {first.getProjectSize(projectID, 'sra')}")
        print(f"📝 project size, fastq: {first.getProjectSize(projectID, 'fastq')}")
        print(f"📝 total runs: {len(first.getAllRuns(projectID))}")
        print(f"📝 available runs, sra: {len(first.getAvailableRuns(projectID, 'sra'))}")
        print(f"📝 unavailable runs, sra: {len(first.getUnavailableRuns(projectID, 'sra'))}")
        print(f"📝 available runs, fastq: {len(first.getAvailableRuns(projectID, 'fastq'))}")
        print(f"📝 unavailable runs, fastq: {len(first.getUnavailableRuns(projectID, 'fastq'))}")
        print(f"📝 project name: {first.getProjectName(projectID)}")
        print(f"📝 project title: {first.getProjectTitle(projectID)}")
        print(f"📝 project description: {first.getProjectDescription(projectID)}")
        
        




if __name__ == "__main__":
    main()

