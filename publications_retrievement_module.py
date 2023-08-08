from GetPublications import GetPublications
from Utilities import Color, Utilities, LoggerManager
from functions_modules import CheckTSV
import os
from os import path
import pandas as pd
from rich import print as rich_print
from rich.panel import Panel
from rich.text import Text
import json


def publications_retrievement(user_session):
    
    while True:
        Utilities.clear()
        original_user_session = user_session

        box = Panel(Text.assemble("Retrieve the publications that include the projects of your interest.\n\nChoose one of the following options:\n\n1 - Use '*_merged_experiments-metadata.tsv' file present in the current session\n2 - Use '*_merged_experiments-metadata.tsv' file present in any other location of your computer\n\n>>> Your current session is ", (f"{user_session}", "rgb(255,255,0)"), " <<<\n\n--- If you want to return to the main menu digit: ", ("back", "rgb(255,0,255)")," ---", style = None, justify="left"), title=Text.assemble((" ◊", "rgb(0,255,0)"), " PUBLICATIONS RETRIEVEMENT MODULE ", ("◊ ", "rgb(0,255,0)")), border_style= "rgb(255,0,255)", padding= (0,1))
        rich_print(box)

        user_publication_input = input("\n  >> Enter your choice: ").strip()
        
        if user_publication_input.lower() in "back":
            return

        elif user_publication_input.isnumeric() == False:
            print(Color.BOLD + Color.RED + "Wrong input" + Color.END, "expected a numeric input or <back> (without <>)\n")
            input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")

        elif user_publication_input.isnumeric() == True:
            user_publication_input = int(user_publication_input)
            if user_publication_input not in (1,2):
                print(Color.BOLD + Color.RED +"Error" + Color.END,"enter a valid choice!")
                input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")

            else:
                logger = LoggerManager.log(user_session)
                logger.debug(f"[INITIALIZED]")
                if user_publication_input == (1):
                    user_session = os.path.join("Downloads", user_session)
                    logger.debug(f"[OPTION-1]: use 'merged_experiments-metadata.tsv' file present in the current session")
                elif user_publication_input == (2):
                    user_session = user_report_local(user_session)

                if user_session != None:
                    files_found = check_files(user_session)
                    file_count = files_found[-1]
                    if file_count == 0:
                        logger.debug(f"[ERROR]: found 0 file")
                        print(Color.BOLD + Color.RED + "\nError" + Color.END, "found 0 file. Is it the correct folder? Note that the file names must end with '_merged_experiments-metadata.tsv'\n")
                        input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")

                    if file_count == 1:
                        merged_experiments = files_found[0]
                        logger.debug(f"Found {merged_experiments}")
                        e_df = read_experiments(user_session, merged_experiments)
                        publications(e_df, user_session)
                        input("\nPress " + Color.BOLD + Color.PURPLE + "ENTER" + Color.END + " to return to the main menu ")
                        return 

                    if file_count >= 2:
                        logger.debug(f"[ERROR]: found more than 1 file")
                        print(Color.BOLD + Color.RED + "\nError" + Color.END, "found too many files. Please choose a folder containing only 1 '*_merged_experiments-metadata.tsv'")
                        input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")
                else:
                    user_session = original_user_session
                

def user_report_local(user_session):
    Utilities.clear()
    while True:

        box = Panel(Text.assemble("Enter the path for '*_merged_experiments-metadata.tsv' file.\n\nThe '_merged_publications-metadata.tsv' will be downloaded in the folder indicated.\n\n>>> Your current session is ", (f"{user_session}", "rgb(255,255,0)"), " <<<\n\n--- If you want to return to the PUBLICATIONS RETRIEVEMENT menu digit: ", ("back", "rgb(255,0,255)")," ---", style = None, justify="left"), title=Text.assemble((" ◊", "rgb(0,255,0)"), " PUBLICATIONS RETRIEVEMENT MODULE ", ("◊ ", "rgb(0,255,0)")), border_style= "rgb(255,0,255)", padding= (0,1))
        rich_print(box)
        
        user_report_local_path = input("\n  >> Digit the path: ").strip()

        if user_report_local_path.lower() in "back":
            return
        
        logger = LoggerManager.log(user_session)
        logger.debug(f"[OPTION-2]: use 'merged_experiments-metadata.tsv' file present in any other location of your computer")
        logger.debug(f"[PATH-SUBMITTED]: {user_report_local_path}")

        elements = user_report_local_path.split(os.sep)
        if "merged_experiments-metadata.tsv" in elements[-1]:
            folders = elements[:-1]
            user_report_local_path = os.sep.join(folders)

        if path.isdir(user_report_local_path) == True:
            if path.isfile(user_report_local_path) == True:
                return user_report_local_path
        else:
            print(Color.BOLD + Color.RED + "Folder not found." + Color.END, " Maybe a typo? Try again\n")
            input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue")
            return

            

#check files
def check_files(user_session):
    files_found = []
    count = 0
    for file in os.listdir(user_session):
        if file.endswith(("_merged_experiments-metadata.tsv")):
            print(Color.BOLD + Color.GREEN + "Found" + Color.END, f"{file}")
            count += 1
            files_found.append(file)
    files_found.append(count)
    return files_found

#open tsv
def read_experiments(user_session, merged_experiments):
    path = os.path.join(user_session, merged_experiments)
    e_df = pd.read_csv(path, delimiter='\t', infer_datetime_format=True)
    return e_df

def publications(e_df, user_session):
    e_df_project = e_df[["study_accession", "secondary_study_accession"]]
    d = e_df_project.T.to_dict(orient='list')
    
    study_accession = []
    for values in d.values():
        if pd.isnull(values[0]):
            study_accession.append(values[1])
        if not pd.isnull(values[0]):
            study_accession.append(values[0])
    
    listOfProjectIDs = list(set(study_accession))
    GetPublications.runGetPublications(listOfProjectIDs, user_session)
    GetPublications.mergePublicationsMetadata(user_session)
    logger = Utilities.log("publications_retrievement_module", user_session)
    
    if os.path.isfile(os.path.join(user_session, f'{study_accession}_merged_publications-metadata.tsv')):
        print("\n>>>"+ Color.BOLD + Color.GREEN + " DOWNLOAD PUBLICATIONS METADATA COMPLETED! " + Color.END + "<<<")
        print('You can find the', Color.UNDERLINE + f'{os.path.basename(user_session)}_merged_publications-metadata.tsv' + Color.END, 
    'here:', Color.BOLD + Color.YELLOW + f'{user_session}' + Color.END)
        logger.debug(f"{os.path.basename(user_session)}_merged_publications-metadata.tsv created")