from IDlist import GetIDlist
from Utilities import Color, Utilities
from Project import Project
from ExperimentMetadataDownload import Exp_Proj_MetadataDownload
from SampleMetadataDownload import SampleMetadataDownload
from SampleMetadataParser import SampleMetadataParser
import time #sara
import csv
import os
from os import path


#QUERY ENA

def UserQueryENAInput():

    title = " QUERY ON ENA "
    print(Color.BOLD + Color.GREEN + title.center(100, '-') + Color.END)
    print("\nExamples of queries:\n"
            "1) skin microbiome ")
    print("2) monkeypox")
    print("\n --- If you want to return to the main menu digit: " 
            + Color.BOLD + Color.PURPLE + "main menu" + Color.END + " ---\n")    
    user_query_input = str(input(">> Digit your query: "))
    
    return user_query_input


def UserDataTypeInput(user_query_input, user_data_type, user_session):

    logger = Utilities.log()
    listOfProjectIDs = GetIDlist.Query(logger, user_session, user_query = user_query_input, data_type = user_data_type)
    QueryDetails = GetIDlist.QueryDetails(listOfProjectIDs)
    print("\nChecking for their availability...") 
    listOfAvailableProjects = Project.getAvailableProjects(listOfProjectIDs) 
                
    return listOfAvailableProjects
        

#DIGIT ACCESSION CODES

def UserDigitCodesInput():
    title = " DIGIT LIST OF ACCESSION CODES "
    print(Color.BOLD + Color.GREEN + title.center(100, '-') + Color.END)
    print("\n Digit the accession codes you are interested in, separated by comma.")
    print("\nExamples of accession codes:\n", "1) PRJNA689547\n", "2) ERP107880, DRP004449, SRP187334") 
    print("\n --- If you want to return to the main menu digit: " + Color.BOLD + Color.PURPLE 
        + "main menu" + Color.END + " ---\n")
    user_query_input = str(input(">> Digit your query: "))
    
    return user_query_input


def UserDigitCodesIDlist(user_query_input):
    logger = Utilities.log()
    listOfProjectIDs = GetIDlist.AccessionCodesFromUserInput(logger, user_input = user_query_input)
    listOfAccessionCodes = GetIDlist.IDlistFromUserInput(logger, listOfProjectIDs)
    results = GetIDlist.IDlistFromUserInputDetails(listOfAccessionCodes)
    listOfProjectIDs = GetIDlist.ShowResults(results) #qui

    return listOfProjectIDs


#FILE ACCESSION CODES

def UserFileCodesInput():
    
    title = " INPUT ACCESSION CODES FILE "
    print(Color.BOLD + Color.GREEN + title.center(100, '-') + Color.END)
    print("\n Load a file containing the accession codes you are interested in. File must have .csv or .tsv format.")
    print("\n --- If you want to return to the main menu digit: " + Color.BOLD + Color.PURPLE 
            + "main menu" + Color.END + " ---\n")
        
    csv_file_input = input(">> Enter your csv or tsv file path: ")
    csv_file_input = csv_file_input.strip() #remove possible initial and final empty spaces

    return csv_file_input


def UserFileCodesIDlist(csv_file_input):
    
    with open(csv_file_input, 'r') as r:
        csv_file_extension = os.path.splitext(csv_file_input)

        if csv_file_extension[1] not in ('.csv', '.tsv'):
            print(Color.BOLD + Color.RED + "File extension not .csv or .tsv" + Color.END, " please use the right format")
            return

        if csv_file_extension[1] == '.csv':
            csv_file_read = csv.reader(r, delimiter=',')
            list_accession_codes_csv_file = list(csv_file_read) 
            listOfProjectIDs = [item for sublist in list_accession_codes_csv_file for item in sublist]

        if csv_file_extension[1] == '.tsv':
            csv_file_read = csv.reader(r, delimiter='\t')
            list_accession_codes_csv_file = list(csv_file_read)
            listOfProjectIDs = [item for sublist in list_accession_codes_csv_file for item in sublist]

            return listOfProjectIDs


#TSV INPUT (_experiment_metadata.tsv & listO)

def CheckTSV(file_path):
    
    while True:
        if path.isfile(file_path) == False:
            print(Color.BOLD + Color.RED + "File not found." + Color.END, " Maybe a typo? Try again\n")
            time.sleep(3)
            continue
        else: 
            file_extension = os.path.splitext(file_path)
            return file_extension


#FOLDER CREATED BY USER INPUT

def user_directory():

    print("\nHow do you want to call the new folder in which the metadata files will be downloaded?")
    user_folder_name = input(">> Enter your choice: ")
    new_directory = os.path.join(os.getcwd(),'Downloads', user_folder_name)

    return new_directory