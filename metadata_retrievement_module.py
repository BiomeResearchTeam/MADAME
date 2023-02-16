from IDlist import GetIDlist
from Utilities import Color, Utilities
from Project import Project
from ExperimentMetadataDownload import Exp_Proj_MetadataDownload
from SampleMetadataDownload import SampleMetadataDownload
from SampleMetadataParser import SampleMetadataParser
from functions_modules import *
import time 
from os import path
from rich import print as rich_print
from rich.panel import Panel
from rich.text import Text

def metadata_retrievement(user_session):
    while True:
        Utilities.clear() 
        # title = " METADATA RETRIEVEMENT MODULE "
        # print(Color.BOLD + Color.PURPLE + title.center(100, '-') + Color.END)
        title = Panel(Text("METADATA RETRIEVEMENT MODULE", style = "b magenta", justify="center"), style = "b magenta")
        rich_print(title)

        print("\nHow do you want to retrieve metadata? Choose one of the following options: \n ")
        print(" 1 - Doing a query on ENA ")
        print(" 2 - Digit the list of accession codes (of projects, runs, studies, and samples) separated by comma")
        print(" 3 - Load a file input (tsv or csv) containing list of accession codes, created by the user")
        print("\n >>> Your current session is " + Color.BOLD + Color.YELLOW +f"{user_session}" + Color.END + " <<<\n")
        print(" --- If you want to return to the main menu digit: " 
        + Color.BOLD + Color.PURPLE + "main menu" + Color.END + " ---\n")

        metadata_retrievement_choice = input("\n>> Enter your choice: ")
        if metadata_retrievement_choice in ("main menu", "MAIN MENU", "Main menu"):
            return
        elif metadata_retrievement_choice.isnumeric():
            metadata_retrievement_choice = int(metadata_retrievement_choice)
            if metadata_retrievement_choice not in (1,2,3):
                print(Color.BOLD + Color.RED + "Error" + Color.END, "enter a valid choice!\n")
                input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")
            else:
                if metadata_retrievement_choice == 1:
                    metadata_retrievement_query(user_session)
                    

                if metadata_retrievement_choice == 2:
                    metadata_retrievement_digit(user_session)
                    

                if metadata_retrievement_choice == 3:
                    metadata_retrievement_file(user_session)
        else:
            print(Color.BOLD + Color.RED + "Error" + Color.END, "enter a valid choice!\n")
            input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")
                    


def metadata_retrievement_query(user_session):
    
    while True:
        Utilities.clear()
        user_query_input = UserQueryENAInput(user_session)
        
        if user_query_input in ("back", "BACK", "Back"):
            return

        else:
            user_data_type = str(input(">> Do you want to search for projects, runs, experiments, samples, or studies? Enter your choice: "))
            if user_data_type not in ("projects", "runs", "experiments", "samples", "studies"):
                print(Color.BOLD + Color.RED + "\nWrong input." + Color.END, "Write <projects>, <experiments>, <runs>, <samples>, or <studies> (without <>)\n")
                input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")
                continue

            else:
                listOfAccessionIDs = UserDataTypeInput(user_query_input, user_data_type, user_session)

                if len(listOfAccessionIDs) == 0:
                    print('Do you want to ' + Color.BOLD + 'try again?\n' + Color.END)
                    input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")
                    continue
                    
                else:
                    metadata_download(listOfAccessionIDs, user_session)
                    return
                    


def metadata_retrievement_digit(user_session):
    
    while True:
        Utilities.clear()
        user_query_input = UserDigitCodesInput(user_session)

        if user_query_input == "back":
            return

        else:
            listOfAccessionIDs = UserDigitCodesIDlist(user_query_input, user_session)

            if len(listOfAccessionIDs) == 0:
                print('Do you want to ' + Color.BOLD + 'try again?\n' + Color.END)
                input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")
                continue

            else:  
                metadata_download(listOfAccessionIDs, user_session)
                return


def metadata_retrievement_file(user_session):
    
    while True:
        Utilities.clear()
        csv_file_input = UserFileCodesInput(user_session)
        
        if csv_file_input in ("back", "BACK", "Back"):
            return

        else:
            if path.isfile(csv_file_input) == False:
                print(Color.BOLD + Color.RED + "File not found." + Color.END, " Maybe a typo? Try again\n")
                input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")
                continue
            else: 
                listOfAccessionIDs = UserFileCodesIDlist(csv_file_input)
                if len(listOfAccessionIDs) == 0:
                    print(Color.BOLD + Color.RED + "Error, file is empty. " + Color.END, "Try again\n")
                    input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")
                    continue
                else: 
                    metadata_download(listOfAccessionIDs, user_session)
                    return
        
       
def metadata_download(listOfAvailableAccessions, user_session):

    Utilities.clear()
    # title = " DOWNLOAD METADATA "
    # print(Color.BOLD + Color.GREEN + title.center(100, '-') + Color.END)
    title = Panel(Text("DOWNLOAD METADATA", style = "b magenta", justify="center"), style = "b magenta")
    rich_print(title)

    print("\nChoose one of the following options: \n ")
    print(" 1 - Download Project and Experiment metadata, and download and parse Sample metadata of the available projects (recommended option)")
    print(" 2 - Download Project and Experiment metadata of the available projects")
    print("\n >>> Your current session is " + Color.BOLD + Color.YELLOW +f"{user_session}" + Color.END + " <<<\n")
    print(" --- If you want to return to the METADATA RETRIEVEMENT MODULE menu digit: " + Color.BOLD + Color.PURPLE + "back" + Color.END + " ---\n")
    user_metadata_input = input("\n>> Enter your choice: ")
        
    if user_metadata_input in ("back", "BACK", "Back"):
        return

    elif user_metadata_input.isnumeric():
        user_metadata_input = int(user_metadata_input)

        if user_metadata_input not in (1,2):
            print("Error, enter a valid choice!\n")
            return

        else:
            if user_metadata_input == 1:

                # Exp_Proj_MetadataDownload needs a list of available accessions, this can also be a mixed
                # accessions list; SampleMetadataDownload and Parser need the corresponding list of projects

                listOfProjectIDs = Exp_Proj_MetadataDownload.runDownloadMetadata(listOfAvailableAccessions, user_session)
                SampleMetadataDownload.runDownloadMetadata(listOfProjectIDs, user_session)
                SampleMetadataParser.runParseMetadata(listOfProjectIDs, user_session)
                final_screen(user_session)
                

            elif user_metadata_input == 2:
                
                Exp_Proj_MetadataDownload.runDownloadMetadata(listOfAvailableAccessions, user_session)
                final_screen(user_session)


def final_screen(user_session):
    print("\nDOWNLOAD METADATA completed!")
    print("Now you can find the metadata files divided by projects inside the folder: MADAME/Downloads/" + Color.BOLD + Color.YELLOW + f"{user_session}" + Color.END)
    input("\nPress " + Color.BOLD + Color.PURPLE + "ENTER" + Color.END + " to return to the main menu ")
    return
