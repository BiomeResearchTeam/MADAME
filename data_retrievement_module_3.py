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
        title = Panel(Text("DATA RETRIEVEMENT MODULE", style = "b magenta", justify="center"), style = "b magenta")
        rich_print(title)
        
        print("\nDownload the data associated to the previously downloaded metadata.\n\nChoose one of the following options:")
        print(" 1 - Use '*_merged_experiments-metadata.tsv' file present the current session")
        print(" 2 - Use '*_merged_experiments-metadata.tsv' files present in any other location of your computer")
        print(" 3 - Input a file (tsv or csv format) with the list of accessions you want to download")
        print("\n >>> Your current session is " + Color.BOLD + Color.YELLOW +f"{user_session}" + Color.END + " <<<\n")
        print(" --- If you want to return to the main menu digit: " + Color.BOLD + Color.PURPLE + "main menu" + Color.END + " ---\n")
        data_download_choice = input("\n>> Enter your choice: ").strip().lower()

        if data_download_choice in ("main menu"):
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
                    enaBT_path = enaBT_download()
                    data_download_function(enaBT_path, data_user_session, files_found)
                
                # if data_download_choice == 3:
                #     data_download_CSV(user_session)


#check files
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
            

def data_user_local(user_session): #per la seconda opzione
    
    title = Panel(Text("DATA RETRIEVEMENT MODULE", style = "b magenta", justify="center"), style = "b magenta")
    rich_print(title)

    while True:
        Utilities.clear()
        print("Enter the path for '*_merged_experiments-metadata.tsv' file. \nData will be downloaded in the folder indicated.")
        print("\n >>> Your current session is " + Color.BOLD + Color.YELLOW +f"{user_session}" + Color.END + " <<<\n")
        print("--- If you want to return to the main menu digit: " + Color.BOLD + Color.PURPLE + "main menu" + Color.END + " ---\n") #verificare se è vero o se torna al report
        data_local_path = input("\n>> Digit the path: ").strip()

        if data_local_path.lower() in ("main menu"):
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
        

def enaBT_download():

    while True:
        Utilities.clear()
        title = Panel(Text("DATA RETRIEVEMENT MODULE", style = "b magenta", justify="center"), style = "b magenta")
        rich_print(title)
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

    while True:
        Utilities.clear()
        title = Panel(Text("DATA RETRIEVEMENT MODULE", style = "b magenta", justify="center"), style = "b magenta")
        rich_print(title)
        user_session = os.path.relpath(data_user_session, 'Downloads')
        print("\nWhat data format do you want to download?", Color.UNDERLINE + "fastq" + Color.END, ",", Color.UNDERLINE + "sra" + Color.END,", or", Color.UNDERLINE + "submitted" + Color.END)
        print("\n >>> Your current session is " + Color.BOLD + Color.YELLOW +f"{user_session}" + Color.END + " <<<")
        print(" --- If you want to return to the main menu digit: " + Color.BOLD + Color.PURPLE + "main menu" + Color.END + " ---\n")
        data_download_type = input("\n>> Enter your choice: ").strip().lower()
        if data_download_type in ("main menu"):
            return
            
        elif data_download_type in ("fastq", "sra", "submitted"):
            merged_experiments = files_found[0]
            e_df = pd.read_csv(os.path.join(data_user_session, merged_experiments), delimiter='\t', infer_datetime_format=True)
            print()  #riga vuota prima dell'output di enaBT
            SequencesDownload.runDownloadData(enaBT_path, user_session, e_df, file_type = data_download_type) #mettere op<ione per tornare indietro se uno non vuole scaricare. qui in sequence.download
            
        else:
            print(Color.BOLD + Color.RED +"\nWrong input " + Color.END, "Write <fastq>, <sra>, or <submitted> (without <>)\n")
            input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")
