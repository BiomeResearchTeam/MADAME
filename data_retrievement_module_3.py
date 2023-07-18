from Utilities import Color, Utilities
from SequencesDownload import SequencesDownload
from os import path
import os
import pandas as pd
from functions_modules import *
from rich import print as rich_print
from rich.panel import Panel
from rich.text import Text

def data_retrievement(user_session):

    while True:
        Utilities.clear() 

        box = Panel(Text.assemble("Download the data associated to the previously downloaded metadata.\n\nChoose one of the following options:\n\n1 - Use '*_merged_experiments-metadata.tsv' file present the current session\n2 - Use '*_merged_experiments-metadata.tsv' files present in any other location of your computer\n3 - Input a file (tsv or csv format) with the list of accessions you want to download\n\n>>> Your current session is ", (f"{user_session}", "rgb(255,255,0)"), " <<<\n\n--- If you want to return to the main menu digit: ", ("back", "rgb(255,0,255)")," ---", style = None, justify="left"), title=Text.assemble((" ◊", "rgb(0,255,0)"), " DATA RETRIEVEMENT MODULE ", ("◊ ", "rgb(0,255,0)")), border_style= "rgb(255,0,255)", padding= (0,1))
        rich_print(box)

        data_download_choice = input("\n  >> Enter your choice: ").strip()

        if data_download_choice.lower() in ("back"):
            return
        
        elif data_download_choice.isnumeric() == False:
            print(Color.BOLD + Color.RED + "Error" + Color.END, "enter a valid choice!\n")
            input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")
        
        elif data_download_choice.isnumeric() == True:
            data_download_choice = int(data_download_choice)
            if data_download_choice not in (1,2,3):
                print(Color.BOLD + Color.RED + "Error" + Color.END, "enter a valid choice!\n")
                input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")

            else:
                if data_download_choice in (1, 2):
                    if data_download_choice == 1:
                        data_user_session = os.path.join("Downloads", user_session)
                    if data_download_choice == 2:
                        data_user_session = data_user_local(user_session)
                    files_found = data_download_MADAME(data_user_session)
                          
                if data_download_choice == 3:
                    data_user_session = check_CSV(user_session)
                    files_found = check_IDs_CSV(data_user_session, user_session)
                
                enaBT_path = enaBT_download(files_found)
                data_download_function(enaBT_path, data_user_session, files_found)
                    


def check_files(data_user_session):
    files_found = []
    count = 0
    for file in os.listdir(data_user_session):
        if file.endswith(("_merged_experiments-metadata.tsv")):
            print(Color.BOLD + Color.GREEN + "Found" + Color.END, f"{file}")
            count += 1
            files_found.append(file)
    files_found.append(count)
    return files_found


def data_download_MADAME(data_user_session):
    while True: 
        files_found = check_files(data_user_session)
        print(files_found)
        file_count = files_found[-1]
        
        if file_count == 0:
            print(Color.BOLD + Color.RED + "\nError" + Color.END, "found 0 file. Are you sure the file is called '*_merged_experiments-metadata.tsv'? If not, please rename it\n")
        elif file_count > 1:
            print(Color.BOLD + Color.RED + "\nError" + Color.END, "found too many files. Please choose a folder containing only 1 '*_merged_experiments-metadata.tsv'")
        else:
            return files_found
            

def data_user_local(user_session):
    title = Panel(Text("DATA RETRIEVEMENT MODULE", style = "b magenta", justify="center"), style = "b magenta")
    rich_print(title)

    while True:
        Utilities.clear()

        box = Panel(Text.assemble("Enter the path for '*_merged_experiments-metadata.tsv' file.\n\nData will be downloaded in the folder indicated.\n\n>>> Your current session is ", (f"{user_session}", "rgb(255,255,0)"), " <<<\n\n--- If you want to return to the DATA RETRIEVEMENT menu digit: ", ("back", "rgb(255,0,255)")," ---", style = None, justify="left"), title=Text.assemble((" ◊", "rgb(0,255,0)"), " DATA RETRIEVEMENT MODULE ", ("◊ ", "rgb(0,255,0)")), border_style= "rgb(255,0,255)", padding= (0,1))
        rich_print(box)

        data_local_path = input("\n  >> Digit the path: ").strip()

        if data_local_path.lower() in ("back"):
            return
                            
        if path.isdir(data_local_path) == False:
            if path.isfile(data_local_path) == True:
                print(Color.BOLD + Color.RED + "\nError." + Color.END, "Please digit the path for the folder containing '*_merged_experiments-metadata.tsv' file\n\n")
                input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")

            else:
                print(Color.BOLD + Color.RED + "\nFolder not found." + Color.END, " Maybe a typo? Try again\n\n")
                input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")
                
        else:
            return data_local_path
        
#DATA FROM USER FILE
def check_CSV(user_session):

    user_csv = UserFileCodesInput(user_session)
    if user_csv.lower() == "back":
        return

    elif path.isfile(user_csv) == False:
        print(Color.BOLD + Color.RED + "File not found." + Color.END, " Maybe a typo? Try again\n")
        input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")
        return
    else: 
        return user_csv
        
def check_IDs_CSV(user_csv, user_session):
    if user_csv is not None:
        listOfProjectIDs = UserFileCodesIDlist(user_csv)
        if len(listOfProjectIDs) == 0:
            print(Color.BOLD + Color.RED + "Error, file is empty. " + Color.END, "Try again\n")
            input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")
            return
        else: 
            listOfAvailableAccessions = UserDigitCodesIDlist(user_csv, user_session)
            if listOfAvailableAccessions is None:
                print(Color.BOLD + Color.RED + "No accessions available or valid. " + Color.END, "Try again\n")
                return
            else:
                files_found = os.path.basename(user_csv)
                return files_found

def enaBT_download(files_found):
    print(files_found)
    print(type(files_found))
    if files_found is not None:
        while True:

            enaBT_txt = open("enaBT_path.txt","r+")
            enaBT_read = enaBT_txt.readline().split(':')[1].strip()
            enaBT_path = os.path.join(enaBT_read, 'enaDataGet')
            if os.path.isfile(os.path.normpath(enaBT_path)):
                print(Color.BOLD + Color.GREEN + '\nenaDataGet found' + Color.END)
                return enaBT_path
            else: 
                if len(enaBT_read) == 0:
                    print('It seems that', Color.BOLD + Color.RED + 'enaBT_path.txt is empty.' + Color.END, 'Remember to', Color.UNDERLINE + 'compile it' + Color.END, 'in order to download data!')
                    input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")
                    return
                else:
                    print(Color.BOLD + Color.RED + "\nenaDataGet not found." + Color.END, "Maybe a typo in enaBT_path.txt? Remember to", Color.UNDERLINE + "compile it" + Color.END, "correctly in order to download data!\n")
                    input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")
                    return
    

def data_download_function(enaBT_path, data_user_session, files_found):
    if files_found is not None:
        while True:
            Utilities.clear()
            user_session = os.path.relpath(data_user_session, 'Downloads')

            box = Panel(Text.assemble("What data format do you want to download? ", ("fastq", "u"), " , ", ("sra", "u"), " , or ", ("submitted", "u"), "\n\n>>> Your current session is ", (f"{user_session}", "rgb(255,255,0)"), " <<<\n\n--- If you want to return to the DATA RETRIEVEMENT menu digit: ", ("back", "rgb(255,0,255)")," ---", style = None, justify="left"), title=Text.assemble((" ◊", "rgb(0,255,0)"), " DATA RETRIEVEMENT MODULE ", ("◊ ", "rgb(0,255,0)")), border_style= "rgb(255,0,255)", padding= (0,1))
            rich_print(box)
    
            data_download_type = input("\n  >> Enter your choice: ").strip().lower()
            if data_download_type in ("back"):
                return
                
            elif data_download_type in ("fastq", "sra", "submitted"):
                merged_experiments = files_found[0]
                if merged_experiments.endswith('.tsv'):
                    e_df = pd.read_csv(os.path.join(data_user_session, merged_experiments), delimiter='\t', infer_datetime_format=True)
                if merged_experiments.endswith('.csv'):
                    e_df = pd.read_csv(os.path.join(data_user_session, merged_experiments), infer_datetime_format=True)
                print() 
                SequencesDownload.runDownloadData(enaBT_path, user_session, e_df, file_type = data_download_type) #mettere op<ione per tornare indietro se uno non vuole scaricare. qui in sequence.download
                
            else:
                print(Color.BOLD + Color.RED +"\nWrong input " + Color.END, "Digit <fastq>, <sra>, <submitted>, or digit <back> to go back (without <>).\n")
                input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")
