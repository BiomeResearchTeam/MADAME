import os
import logging
from os.path import exists
from webbrowser import get

from IDlist import GetIDlist
from ExperimentMetadataDownload import Exp_Proj_MetadataDownload
from SampleMetadataDownload import SampleMetadataDownload
from Utilities import Directory
from SampleMetadataParser import SampleMetadataParser
from Project import Project
from ProjectManager import ProjectManager
from GetPublications import GetPublications


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

       
        listOfProjectIDs = [os.path.splitext(filename)[0] for filename in os.listdir("/mnt/c/Users/conog/Desktop/DF3_METADATA_ALL")]


        setDirectory = Directory("CreateDirectory")
        ########
        #SET YOUR PREFERRED DOWNLOAD DIRECTORY HERE IF YOU'RE TRYING THE SCRIPT!
        ########
        setDirectory.setMADAMEdirectory("/mnt/c/Users/conog/Desktop/df3")
        
        print("⬇️   Downloading available project and experiments metadata...")
        MetadataDownload = Exp_Proj_MetadataDownload("MetadataDownload")
        MetadataDownload.runDownloadMetadata(listOfProjectIDs)
        print("\n✅   All done!")


        print("⬇️   Downloading available samples metadata...")
        MetadataDownload = SampleMetadataDownload("MetadataDownload")
        MetadataDownload.runDownloadMetadata(listOfProjectIDs)
        print("\n✅   All done!")

        print("------------------------")
        print("✨   Parsing...\n")
        MetadataParsing = SampleMetadataParser("MetadataParsing")
        MetadataParsing.runParseMetadata(listOfProjectIDs)

        




if __name__ == "__main__":
    main()

