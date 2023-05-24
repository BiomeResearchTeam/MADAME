from GetPublications import GetPublications
from Utilities import Color, Utilities
from functions_modules import CheckTSV
import os
from os import path
import pandas as pd
from rich import print as rich_print
from rich.panel import Panel
from rich.text import Text


def publications_retrievement(user_session):
    
    while True:
        Utilities.clear() 
        title = Panel(Text("PUBLICATIONS RETRIEVEMENT MODULE", style = "b magenta", justify="center"), style = "b magenta")
        rich_print(title)

        print("\nRetrieve the publications that include the projects of your interest. \n\nChoose one of the following options:")
        print(" 1 - Use '*_merged_experiments-metadata.tsv' file present in the current session")
        print(" 2 - Use '*_merged_experiments-metadata.tsv' file present in any other location of your computer")
        print("\n >>> Your current session is " + Color.BOLD + Color.YELLOW +f"{user_session}" + Color.END + " <<<\n")
        print(" --- If you want to return to the main menu digit: " + Color.BOLD + Color.PURPLE + "main menu" + Color.END + " ---\n")
        user_publication_input = input("\n>> Enter your choice: ").strip()
        
        if user_publication_input in ("main menu", "MAIN MENU", "Main menu"):
            return

        elif user_publication_input.isnumeric() == False:
            print(Color.BOLD + Color.RED + "Wrong input" + Color.END, "expected a numeric input or <main menu> (without <>)\n")
            input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")

        elif user_publication_input.isnumeric() == True:
            user_publication_input = int(user_publication_input)
            if user_publication_input not in (1,2):
                print(Color.BOLD + Color.RED +"Error" + Color.END,"enter a valid choice!")
                input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")

            else:
                #ALTERNATIVA
                if user_publication_input == (1):
                    user_session = os.path.join("Downloads", user_session)
                elif user_publication_input == (2):
                    user_session = user_report_local(user_session)

                files_found = check_files(user_session)
                file_count = files_found[-1]
                if file_count == 0:
                    print(Color.BOLD + Color.RED + "\nError" + Color.END, "found 0 file. Is it the correct folder? Note that the file names must end with '_merged_experiments-metadata.tsv'\n")
                    input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")

                if file_count == 1:
                    merged_experiments = files_found[0]
                    e_df = read_experiments(user_session, merged_experiments)
                    publications(e_df, user_session)
                    input("\nPress " + Color.BOLD + Color.PURPLE + "ENTER" + Color.END + " to return to the main menu ")
                    return 

                if file_count >= 2:
                    print(Color.BOLD + Color.RED + "\nError" + Color.END, "found too many files. Please choose a folder containing only 1 '*_merged_experiments-metadata.tsv'")
                    input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")
                    publications(e_df, user_session)
                


                ########DA QUIIIIIIII  >>funziona<<
                # if user_publication_input == (1):
                #     user_session = os.path.join("Downloads", user_session)

                #     files_found = check_files(user_session)
                #     file_count = files_found[-1]
                #     if file_count == 0:
                #         print(Color.BOLD + Color.RED + "\nError" + Color.END, "found 0 file. Is it the correct folder? Note that the file names must end with '_merged_experiments-metadata.tsv'\n")
                #         input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")

                #     if file_count == 1:
                #         merged_experiments = files_found[0]
                #         e_df = read_experiments(user_session, merged_experiments)
                #         publications(e_df, user_session)
                #         input("\nPress " + Color.BOLD + Color.PURPLE + "ENTER" + Color.END + " to return to the main menu ")
                #         return 

                #     if file_count >= 2:
                #         print(Color.BOLD + Color.RED + "\nError" + Color.END, "found too many files. Please choose a folder containing only 1 '*_merged_experiments-metadata.tsv'")
                #         input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")
                #         publications(e_df, user_session)
                    

                # if user_publication_input == (2):
                #     user_report_local_path = user_report_local(user_session)

                #     files_found = check_files(user_report_local_path)
                #     file_count = files_found[-1]
                #     #serve a qualcosa? come fa un path a essere = 0?
                #     # if user_report_local_path == 0:
                #     #     break
                #     file_count = check_files(user_report_local_path)
                #     if file_count == 0:
                #         print(Color.BOLD + Color.RED + "\nError" + Color.END, "found 0 file. Is it the correct folder? Note that the file name must end with '_merged_experiments-metadata.tsv'\n")
                #         input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")

                #     if file_count == 1:
                #         merged_experiments = files_found[0]
                #         e_df = read_experiments(user_report_local_path, merged_experiments)
                #         publications(e_df, user_session)
                #         input("\nPress " + Color.BOLD + Color.PURPLE + "ENTER" + Color.END + " to return to the main menu ")
                #         return 

                #     if file_count >= 2:
                #         print(Color.BOLD + Color.RED + "\nError" + Color.END, "found too many files. Please choose a folder containing only 1 '*_merged_experiments-metadata.tsv'")
                #         input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")
                    
                    ########A QUIIIIII

def user_report_local(user_session):
    Utilities.clear()
    while True:
        title = Panel(Text("PUBLICATIONS RETRIEVEMENT MODULE", style = "b magenta", justify="center"), style = "b magenta")
        rich_print(title)
        
        print("\nEnter the path for '*_merged_experiments-metadata.tsv' file. \nThe '_merged_publications-metadata.tsv' will be downloaded in the folder indicated.")
        print("\n >>> Your current session is " + Color.BOLD + Color.YELLOW +f"{user_session}" + Color.END + " <<<\n")
        print(" --- If you want to return to the main menu digit: " + Color.BOLD + Color.PURPLE + "main menu" + Color.END + " ---\n") #verificare se è vero o se torna al report
        user_report_local_path = input("\n>> Digit the path: ").strip()

        if user_report_local_path in ("main menu", "MAIN MENU", "Main menu"):
            return 0
                            
        if path.isdir(user_report_local_path) == False:
            if path.isfile(user_report_local_path) == True:
                print(Color.BOLD + Color.RED + "Error" + Color.END, "Please digit the path for the folder containing '*_merged_experiments-metadata.tsv' file\n")
                input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue")
                return
            else:
                print(Color.BOLD + Color.RED + "Folder not found." + Color.END, " Maybe a typo? Try again\n")
                input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue")
                return
        else:
            return user_report_local_path

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
    study_accession = e_df["study_accession"].unique().tolist()
    listOfProjectIDs = [id for id in study_accession if id is not None]   
    GetPublications.runGetPublications(listOfProjectIDs, user_session)
    #e se non è stata trovata nessuna pubblicazione? 
    GetPublications.mergePublicationsMetadata(user_session)
    print(Color.BOLD + Color.GREEN + '\nPublications successfully retrieved.' + Color.END,'You can find the', Color.UNDERLINE + f'{os.path.basename(user_session)}_merged_publications-metadata.tsv' + Color.END, 
    'here:', Color.BOLD + Color.YELLOW + f'{user_session}' + Color.END)
     
