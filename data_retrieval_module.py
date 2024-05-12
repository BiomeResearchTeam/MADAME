from Utilities import Color, Utilities
from SequencesDownload_copy_copy import SequencesDownload 
from os import path
import os
import pandas as pd
from functions_modules import *
from rich import print as rich_print
from rich.panel import Panel
from rich.text import Text

def data_retrieval(user_session):

    while True:
        Utilities.clear() 
        original_user_session = user_session
        box = Panel(Text.assemble("Download the data associated to the previously downloaded metadata.\n\nChoose one of the following options:\n\n1 - Use '*_merged_experiments-metadata.tsv' file present the current session\n2 - Use '*_merged_experiments-metadata.tsv' files present in any other location of your computer\n\n>>> Your current session is ", (f"{user_session}", "rgb(255,255,0)"), " <<<\n\n--- If you want to return to the main menu digit: ", ("back", "rgb(255,0,255)")," ---", style = None, justify="left"), title=Text.assemble((" ◊", "rgb(0,255,0)"), " DATA retrieval MODULE ", ("◊ ", "rgb(0,255,0)")), border_style= "rgb(255,0,255)", padding= (0,1))
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
                if data_download_choice == 1:
                    logger = LoggerManager.log(user_session)
                    logger.debug(f"[OPTION-1] - use 'merged_experiments-metadata.tsv' file present in the current session")
                elif data_download_choice == 2:
                    logger = LoggerManager.log(user_session)
                    logger.debug(f"[OPTION-2] - use 'merged_experiments-metadata.tsv' file present in any other location of your computer")
                    user_session = data_user_local(user_session)
                if user_session != None:
                    files_found = check_files(user_session)
                    enaBT_path = enaBT_check(files_found, user_session)
                    data_download(enaBT_path, user_session, files_found)
                    user_session = original_user_session
                else:
                    user_session = original_user_session

    
def check_files(user_session):
    files_found = []
    for file in os.listdir(os.path.join("Downloads", user_session)):
        if file.endswith(("_merged_experiments-metadata.tsv")):
            files_found.append(file)
            print(Color.BOLD + Color.GREEN + "\nFound" + Color.END, f"{file}")
            logger = LoggerManager.log(user_session)
            logger.debug(f"Found {file}")

    while True: 
        if len(files_found) == 0:
            print(Color.BOLD + Color.RED + "\nError" + Color.END, "found 0 file. Are you sure the file is called '*_merged_experiments-metadata.tsv'? If not, please rename it\n")
            logger.debug(f"[ERROR]: found 0 file")
        elif len(files_found) > 1:
            print(Color.BOLD + Color.RED + "\nError" + Color.END, "found too many files. Please choose a folder containing only 1 '*_merged_experiments-metadata.tsv'")
            logger.debug(f"[ERROR]: found more than 1 file")
        else:
            return files_found
        

def enaBT_check(files_found, user_session):
    if files_found is not None:
        while True:
            with open("enaBT_path.txt","r+") as enaBT_txt:
                for line in enaBT_txt:
                    if "Path to enaBrowserTools:" in line:
                        enaBT_read = line.split(':')[1].strip()
                    else:
                        enaBT_read = line
            enaBT_path = os.path.join(enaBT_read, 'enaDataGet')
            if os.path.isfile(os.path.normpath(enaBT_path)):
                print(Color.BOLD + Color.GREEN + 'Found' + Color.END + " enaDataGet")
                logger = LoggerManager.log(user_session)
                logger.debug("Found enaDataGet")
                input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")
                return enaBT_path
            else: 
                if len(enaBT_read) == 0:
                    print('It seems that', Color.BOLD + Color.RED + 'enaBT_path.txt is empty.' + Color.END, 'Remember to', Color.UNDERLINE + 'compile it' + Color.END, 'in order to download data!')
                    logger = LoggerManager.log(user_session)
                    logger.debug(f"[ERROR]: enaBT_path.txt is empty")
                    input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")
                    return
                else:
                    print(Color.BOLD + Color.RED + "\nenaDataGet not found." + Color.END, "Maybe a typo in enaBT_path.txt? Remember to", Color.UNDERLINE + "compile it" + Color.END, "correctly in order to download data!\n")
                    logger = LoggerManager.log(user_session)
                    logger.debug(f"[ERROR]: enaBT_path.txt not found")
                    input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")
                    return


def data_download(enaBT_path, user_session, files_found):
    if files_found is not None:
        while True:
            Utilities.clear()

            box = Panel(Text.assemble("What data format do you want to download? ", ("fastq", "u"), " , ", ("sra", "u"), " , or ", ("submitted", "u"), "\n\n>>> Your current session is ", (f"{user_session}", "rgb(255,255,0)"), " <<<\n\n--- If you want to return to the DATA retrieval menu digit: ", ("back", "rgb(255,0,255)")," ---", style = None, justify="left"), title=Text.assemble((" ◊", "rgb(0,255,0)"), " DATA retrieval MODULE ", ("◊ ", "rgb(0,255,0)")), border_style= "rgb(255,0,255)", padding= (0,1))
            rich_print(box)
    
            data_download_type = input("\n  >> Enter your choice: ").strip().lower()
            if data_download_type in ("back"):
                return
                
            elif data_download_type in ("fastq", "sra", "submitted"):
                logger = LoggerManager.log(user_session)
                logger.debug(f"[DATA-TYPE-SELECTED]: {data_download_type}")
                merged_experiments = files_found[0]
                if merged_experiments.endswith('.tsv'):
                    e_df = pd.read_csv(os.path.join("Downloads", user_session, merged_experiments), delimiter='\t', infer_datetime_format=True, dtype=str)
                    if 'umbrella_project' in e_df.columns:
                        e_df = pd.read_csv(os.path.join("Downloads", user_session, merged_experiments), delimiter='\t', infer_datetime_format=True, dtype=str, keep_default_na=False)

                print() 
                SequencesDownload.runDownloadData(enaBT_path, user_session, e_df, file_type = data_download_type)
                
            else:
                print(Color.BOLD + Color.RED +"\nWrong input " + Color.END, "Digit <fastq>, <sra>, <submitted>, or digit <back> to go back (without <>).\n")
                input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")


#DATA FROM LOCAL PATH
def data_user_local(user_session):
    title = Panel(Text("DATA retrieval MODULE", style = "b magenta", justify="center"), style = "b magenta")
    rich_print(title)

    while True:
        Utilities.clear()

        box = Panel(Text.assemble("Enter the path for '*_merged_experiments-metadata.tsv' file.\n\nData will be downloaded in the folder indicated.\n\n>>> Your current session is ", (f"{user_session}", "rgb(255,255,0)"), " <<<\n\n--- If you want to return to the DATA retrieval menu digit: ", ("back", "rgb(255,0,255)")," ---", style = None, justify="left"), title=Text.assemble((" ◊", "rgb(0,255,0)"), " DATA retrieval MODULE ", ("◊ ", "rgb(0,255,0)")), border_style= "rgb(255,0,255)", padding= (0,1))
        rich_print(box)

        data_local_path = input("\n  >> Digit the path: ").strip()

        if data_local_path.lower() in ("back"):
            return
        
        elements = data_local_path.split(os.sep)
        if "merged_experiments-metadata.tsv" in elements[-1]:
            folders = elements[:-1]
            data_local_path = os.sep.join(folders)

        if path.isdir(data_local_path) == True:
            logger = LoggerManager.log(user_session)
            logger.debug(f"[PATH-SUBMITTED]: {data_local_path}")
            return data_local_path
        else:
            print(Color.BOLD + Color.RED + "Folder not found." + Color.END, " Maybe a typo? Try again\n")
            input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")
            return