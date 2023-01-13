from IDlist import GetIDlist
from Utilities import Color, Utilities
from Project import Project
from ExperimentMetadataDownload import Exp_Proj_MetadataDownload
from SampleMetadataDownload import SampleMetadataDownload
from SampleMetadataParser import SampleMetadataParser
from GetPublications import GetPublications #modulo 3
from SequencesDownload import SequencesDownload #modulo 2
from functions_modules import *
import time #sara
from report_module import report_module
from os import path
import os

def metadata_retrievement():
    while True:
        #clear() 
        title = " METADATA RETRIEVEMENT MODULE "
        print(Color.BOLD + Color.PURPLE + title.center(100, '-') + Color.END)
        print("\nHow do you want to retrieve metadata? Choose one of the following options: \n ")
        print(" 1 - Doing a query on ENA ")
        print(" 2 - Digit the list of accession codes (of projects, runs, studies, and samples) separated by comma")
        print(" 3 - Load a file input (tsv or csv) containing list of accession codes, created by the user")
        print("\n --- If you want to return to the main menu digit: " 
        + Color.BOLD + Color.PURPLE + "main menu" + Color.END + " ---\n")

        metadata_retrievement_choice = input("\n>> Enter your choice: ")
        if metadata_retrievement_choice in ("main menu", "MAIN MENU", "Main menu"):
            return
        elif metadata_retrievement_choice.isnumeric():
            metadata_retrievement_choice = int(metadata_retrievement_choice)
            if metadata_retrievement_choice not in (1,2,3):
                print("Error, enter a valid choice!\n")
                return
            else:
                if metadata_retrievement_choice == 1:
                    metadata_retrievement_query()
                    #report_module()
                    break

                if metadata_retrievement_choice == 2:
                    metadata_retrievement_digit()
                    break

                if metadata_retrievement_choice == 3:
                    metadata_retrievement_file()
                    break


def metadata_retrievement_query():
    Utilities.clear()
    while True:
        #clear()
        user_query_input = UserQueryENAInput()
        
        if user_query_input in ("main menu", "MAIN MENU", "Main menu"):
            return

        else:
            user_data_type = str(input(">> Do you want to search for projects, runs, samples, or studies? Enter your choice: "))
            if user_data_type not in ("projects", "runs", "samples", "studies"):
                print(Color.BOLD + Color.RED + "\nWrong input." + Color.END, "Write <projects>, <runs>, <samples>, or <studies> (without <>)\n")
                time.sleep(3)
                continue

            else:
                listOfProjectIDs = UserDataTypeInput(user_query_input, user_data_type, user_session)

                if len(listOfProjectIDs) == 0:
                    print('Do you want to ' + Color.BOLD + 'try again?\n' + Color.END)
                    time.sleep(2)
                    continue
                    
                else:
                    metadata_download(listOfProjectIDs)
                    time.sleep(3)
                    #report

    
            

#         #logger.info('STEP 2: Query on ENA')


def metadata_retrievement_digit():
    Utilities.clear()
    while True:
        # clear()
        user_query_input = UserDigitCodesInput()

        if user_query_input in ("main menu", "MAIN MENU", "Main menu"):
            return

        else:
            listOfProjectIDs = UserDigitCodesIDlist(user_query_input)

            if len(listOfProjectIDs) == 0:
                print('Do you want to ' + Color.BOLD + 'try again?\n' + Color.END)
                time.sleep(2)
                continue

            else:  
                metadata_download(listOfProjectIDs)
                time.sleep(3)
                #report


def metadata_retrievement_file():
    Utilities.clear()
    while True:
        #clear()
        csv_file_input = UserFileCodesInput()
        
        if csv_file_input in ("main menu", "MAIN MENU", "Main menu"):
            return

        else:
            if path.isfile(csv_file_input) == False:
                print(Color.BOLD + Color.RED + "File not found." + Color.END, " Maybe a typo? Try again\n")
                time.sleep(3)
                continue
            else: 
                listOfProjectIDs = UserFileCodesIDlist(csv_file_input)
                if len(listOfProjectIDs) == 0:
                    print(Color.BOLD + Color.RED + "Error, file is empty. " + Color.END, "Try again\n")
                    time.sleep(2)
                    continue
                else: 
                    metadata_download(listOfProjectIDs)
                    time.sleep(3)
                        #report
        
       
def metadata_download(listOfAvailableProjects):
    
    title = " DOWNLOAD METADATA "
    print(Color.BOLD + Color.GREEN + title.center(100, '-') + Color.END)
    print("\nChoose one of the following options: \n ")
    print(" 1 - Download Project and Experiment metadata, and download and parse Sample metadata of the available projects (recommended option)")
    print(" 2 - Download Project and Experiment metadata of the available projects")
    print("\n --- If you want to return to the main metadata menu digit: " + Color.BOLD + Color.PURPLE + "main menu" + Color.END + " ---\n")
    user_metadata_input = input("\n>> Enter your choice: ")
        
    if user_metadata_input in ("main menu", "MAIN MENU", "Main menu"):
        return

    elif user_metadata_input.isnumeric():
        user_metadata_input = int(user_metadata_input)

        if user_metadata_input not in (1,2):
            print("Error, enter a valid choice!\n")
            return

        else:
            if user_metadata_input == 1:
                #Project.listOfProjectIDsTSV(listOfAvailableProjects)
                new_directory = user_directory()
                #Directory.createDirectory(new_directory)
                print(Color.BOLD + Color.GREEN + '\nNew folder created.' + Color.END, ' At the end of the download you will find the metadata files right there.\n')
                Exp_Proj_MetadataDownload.runDownloadMetadata(listOfAvailableProjects, new_directory)
                SampleMetadataDownload.runDownloadMetadata(listOfAvailableProjects)
                SampleMetadataParser.runParseMetadata(listOfAvailableProjects)

                print("\nWhat data format do you want to download? fastq, sra, or submitted")
                user_file_type = input(">> Enter your choice: ")
                #os.chdir('..') #tornare nella cartella main (che diventerà la cartella con il nome a scelta dello user)
                #ATTENZIONE NON USARE QUESTO METODO PERCHé SE NON SCARICA NIENTE DI NUOVO NON ENTRA NEANCHE NELLE CARTELLE 
                #E QUINDI ESCE DALLA MASTER
                SequencesDownload.runDownloadData(listOfAvailableProjects, file_type = user_file_type)

            elif user_metadata_input == 2:
                #Project.listOfProjectIDsTSV(listOfAvailableProjects)
                new_directory = user_directory()
                #Directory.createDirectory(new_directory)
                print(Color.BOLD + Color.GREEN + '\nNew folder created.' + Color.END, ' At the end of the download you will find the metadata files right there.\n')
                Exp_Proj_MetadataDownload.runDownloadMetadata(listOfAvailableProjects, new_directory)