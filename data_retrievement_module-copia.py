from Utilities import Color, Utilities
from SequencesDownload import SequencesDownload
from functions_modules import CheckTSV
from os import path
import os
import pandas as pd
from functions_modules import *
from rich import print as rich_print
from rich.panel import Panel
from rich.text import Text


def session_title():
    Utilities.clear()
    title = Panel(Text("DATA RETRIEVEMENT MODULE", style = "b magenta", justify="center"), style = "b magenta")
    rich_print(title)


def data_retrievement(user_session):
    while True:
        session_title()
        print("\nDownload the data associated to the previously downloaded metadata.\n\nChoose one of the following options:")
        print(" 1 - Use '*_merged_experiments-metadata.tsv' file present the current session")
        print(" 2 - Use '*_merged_experiments-metadata.tsv' files present in any other location of your computer")
        print(" 3 - Input a file (tsv or csv format) with the list of runs you want to download")
        print("\n >>> Your current session is " + Color.BOLD + Color.YELLOW +f"{user_session}" + Color.END + " <<<\n")
        print(" --- If you want to return to the main menu digit: " + Color.BOLD + Color.PURPLE + "main menu" + Color.END + " ---\n")
        data_download_choice = input("\n>> Enter your choice: ").strip().lower()

        if data_download_choice in ("main menu"):
            return
        elif data_download_choice.isnumeric():
            data_download_choice = int(data_download_choice)
            if data_download_choice not in (1,2,3):
                print(Color.BOLD + Color.RED + "Error" + Color.END, "enter a valid choice!\n")
                input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")

            else:
                if data_download_choice == 1:
                    session_title()
                    data_user_session = os.path.join("Downloads", user_session)
                    #data_download_MADAME(user_session)

                if data_download_choice == 2:
                    session_title()
                    data_user_local(user_session)
                    #data_download_path(user_session)
                
                if data_download_choice == 3:
                    session_title()
                    data_download_CSV(user_session)
        
        else:
            print(Color.BOLD + Color.RED + "Error" + Color.END, "enter a valid choice!\n")
            input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")


#check files
def check_files(data_user_session):
    count = 0
    for file in os.listdir(data_user_session):
        if file.endswith(("_merged_experiments-metadata.tsv")):
            print(Color.BOLD + Color.GREEN + "Found" + Color.END, f"{file}")
            count += 1   
    return count    

def check_file_experiments(data_user_session):
    for file in os.listdir(data_user_session):
        if file.endswith("_merged_experiments-metadata.tsv"):
            return file

def read_experiments(data_user_session, merged_experiments):
    path = os.path.join(data_user_session, merged_experiments)
    e_df = pd.read_csv(path, delimiter='\t', infer_datetime_format=True)
    return e_df






#DATA IN MADAME
def data_download_MADAME(user_session):
    # Utilities.clear()
    # title = Panel(Text("DATA RETRIEVEMENT MODULE", style = "b magenta", justify="center"), style = "b magenta")
    # rich_print(title)
    data_user_session = os.path.join("Downloads", user_session)
    while True: 
        file_count = check_files(data_user_session)
        
        if file_count == 0:
            print(Color.BOLD + Color.RED + "\nError" + Color.END, "found 0 file. Are you sure the file is called '*_merged_experiments-metadata.tsv'? If not, please rename it\n")

        elif file_count > 1:
            print(Color.BOLD + Color.RED + "\nError" + Color.END, "found too many files. Please choose a folder containing only 1 '*_merged_experiments-metadata.tsv'")

        else:
            enaBT_download(user_session, data_user_session)
            return



def download_loop(user_session, data_user_session):
    while True: 
        file_count = check_files(data_user_session)
        
        if file_count == 0:
            print(Color.BOLD + Color.RED + "\nError" + Color.END, "found 0 file. Are you sure the file is called '*_merged_experiments-metadata.tsv'? If not, please rename it\n")

        elif file_count > 1:
            print(Color.BOLD + Color.RED + "\nError" + Color.END, "found too many files. Please choose a folder containing only 1 '*_merged_experiments-metadata.tsv'")

        else:
            enaBT_download(user_session, data_user_session)
            return




# #DATA IN LOCAL PATH
# def data_download_path(EnaBT_path, user_session):
#     # Utilities.clear()
#     # title = Panel(Text("DATA RETRIEVEMENT MODULE", style = "b magenta", justify="center"), style = "b magenta")
#     # rich_print(title)

#     #data_user_session = data_user_local(user_session)
#     while True: 
#         file_count = check_files(data_user_session)
        
#         if file_count == 0:
#             print(Color.BOLD + Color.RED + "\nError" + Color.END, "found 0 file. Are you sure the file is called '*_merged_experiments-metadata.tsv'? If not, please rename it\n")

#         elif file_count > 1:
#             print(Color.BOLD + Color.RED + "\nError" + Color.END, "found too many files. Please choose a folder containing only 1 '*_merged_experiments-metadata.tsv'")

#         else:
#             enaBT_download(user_session, data_user_session)
#             return


def data_user_local(user_session):
    # Utilities.clear()
    # title = Panel(Text("DATA RETRIEVEMENT MODULE", style = "b magenta", justify="center"), style = "b magenta")
    # rich_print(title)

    while True:
        print("Enter the path for '*_merged_experiments-metadata.tsv' file. \nData will be downloaded in the folder indicated.")
        print("\n >>> Your current session is " + Color.BOLD + Color.YELLOW +f"{user_session}" + Color.END + " <<<\n")
        print("\ --- If you want to return to the main menu digit: " + Color.BOLD + Color.PURPLE + "main menu" + Color.END + " ---\n") #verificare se è vero o se torna al report
        data_local_path = input("\n>> Digit the path: ").strip()

        if data_local_path in ("main menu", "MAIN MENU", "Main menu"):
            return
                            
        if path.isdir(data_local_path) == False:
            if path.isfile(data_local_path) == True:
                print(Color.BOLD + Color.RED + "\nError. " + Color.END, "Please digit the path for the folder containing '*_merged_experiments-metadata.tsv' file\n\n")
                input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")

            else:
                print(Color.BOLD + Color.RED + "\nFolder not found." + Color.END, " Maybe a typo? Try again\n\n")
                input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")
                
        else:
            return data_local_path


#DATA FROM USER FILE
def data_download_CSV(user_session):
    
    while True:
        Utilities.clear()
        title = Panel(Text("DATA RETRIEVEMENT MODULE", style = "b magenta", justify="center"), style = "b magenta")
        rich_print(title)

        user_input_csv = UserFileCodesInput(user_session)
        if user_input_csv in ("back", "BACK", "Back"):
            return

        else:
            if path.isfile(user_input_csv) == False: #NON FUNZIONA QUIIIIIII##################################################################################
                print(Color.BOLD + Color.RED + "File not found." + Color.END, " Maybe a typo? Try again\n")
                input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")
                continue
            else: 
                listOfProjectIDs = UserFileCodesIDlist(user_input_csv)
                if len(listOfProjectIDs) == 0:
                    print(Color.BOLD + Color.RED + "Error, file is empty. " + Color.END, "Try again\n")
                    input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")
                    continue
                else: 
                    listOfProjectIDs = UserDigitCodesIDlist(user_input_csv, user_session)
                    print("\nWhat data format do you want to download? fastq, sra, or submitted")
                    print("\n >>> Your current session is " + Color.BOLD + Color.YELLOW +f"{user_session}" + Color.END + " <<<\n")
                    print(" --- If you want to return to the main menu digit: " + Color.BOLD + Color.PURPLE + "main menu" + Color.END + " ---\n")
                    data_download_type = input("\n\n>> Enter your choice: ").strip().lower()
                    if data_download_type in ("main menu"):
                        return
        
                    elif data_download_type in ("fastq", "sra", "submitted"):
                        path = os.path.dirname(user_input_csv)
                        filename, file_extension = os.path.splitext(user_input_csv)
                        if file_extension == '.tsv':
                            e_df = pd.read_csv(path, delimiter='\t', infer_datetime_format=True)
                            while True:
                                EnaBT_path = input(">> Digit the path to enaDataGet: ")
                                filename, file_extension = os.path.splitext(EnaBT_path)
                                if os.path.basename(os.path.normpath(EnaBT_path)) == 'enaDataGet':
                                    print()  #riga vuota prima dell'output di enaBT
                                    SequencesDownload.runDownloadData(user_session, e_df, file_type = data_download_type)

                                elif os.path.basename(os.path.normpath(EnaBT_path)) == 'python3':
                                    EnaBT_path = os.path.join(EnaBT_path, 'enaDataGet')
                                    print()  #riga vuota prima dell'output di enaBT
                                    SequencesDownload.runDownloadData(user_session, e_df, file_type = data_download_type)
                                    
                                else:
                                    print(Color.BOLD + Color.RED + "File not found." + Color.END, " Maybe a typo? Try again\n")
                                    input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")
                                    continue
                                
                        if file_extension == '.csv':
                            e_df = pd.read_csv(path, delimiter=',', infer_datetime_format=True)
                            while True:
                                EnaBT_path = input(">> Digit the path to enaDataGet: ")
                                filename, file_extension = os.path.splitext(EnaBT_path)
                                if os.path.basename(os.path.normpath(EnaBT_path)) == 'enaDataGet':
                                    print()  #riga vuota prima dell'output di enaBT
                                    SequencesDownload.runDownloadData(user_session, e_df, file_type = data_download_type)

                                elif os.path.basename(os.path.normpath(EnaBT_path)) == 'python3':
                                    EnaBT_path = os.path.join(EnaBT_path, 'enaDataGet')
                                    print()  #riga vuota prima dell'output di enaBT
                                    SequencesDownload.runDownloadData(user_session, e_df, file_type = data_download_type)
                                else:
                                    print(Color.BOLD + Color.RED + "File not found." + Color.END, " Maybe a typo? Try again\n")
                                    input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")
                                    continue


#ENABT PATH
def enaBT_download(user_session, data_user_session): #CI STO LAVORANDO SARA

    Utilities.clear()
    title = Panel(Text("DATA RETRIEVEMENT MODULE", style = "b magenta", justify="center"), style = "b magenta")
    rich_print(title)

    while True:
        
        enaBT_txt = open("enaBT_path.txt","r+")
        enaBT_read = enaBT_txt.readline().split(':')[1].strip()
        enaBT_path = os.path.join(enaBT_read, 'enaDataGet')
        if os.path.isfile(os.path.normpath(enaBT_path)):
            print(Color.BOLD + Color.GREEN + '\nenaDataGet found' + Color.END)
            data_download_function(enaBT_path, user_session, data_user_session)
        else: 
            if len(enaBT_read) == 0:
                print('It seems that', Color.BOLD + Color.RED + 'enaBT_path.txt is empty.' + Color.END, 'Remember to', Color.UNDERLINE + 'compile it' + Color.END, 'in order to download data!')
                input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")
                return
            else:
                print(Color.BOLD + Color.RED + "\nenaDataGet not found." + Color.END, "Maybe a typo in enaBT_path.txt? Remember to", Color.UNDERLINE + "compile it" + Color.END, "correctly in order to download data!\n")
                input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")
                return
              


#PRINCIPAL DOWNLOAD FUNCTION
def data_download_function(EnaBT_path, user_session, data_user_session):

        print("\nWhat data format do you want to download?", Color.UNDERLINE + "fastq" + Color.END, ",", Color.UNDERLINE + "sra" + Color.END,", or", Color.UNDERLINE + "submitted" + Color.END)
        print("\n >>> Your current session is " + Color.BOLD + Color.YELLOW +f"{user_session}" + Color.END + " <<<")
        print(" --- If you want to return to the main menu digit: " + Color.BOLD + Color.PURPLE + "main menu" + Color.END + " ---\n")
        data_download_type = input("\n>> Enter your choice: ").strip().lower()
        if data_download_type in ("main menu"):
            return
        
        elif data_download_type in ("fastq", "sra", "submitted"):
            merged_experiments = check_file_experiments(data_user_session)
            e_df = read_experiments(data_user_session, merged_experiments)
            print()  #riga vuota prima dell'output di enaBT
            SequencesDownload.runDownloadData(EnaBT_path, user_session, e_df, file_type = data_download_type)

        else:
            print(Color.BOLD + Color.RED +"\nWrong input " + Color.END, "Write <fastq>, <sra>, or <submitted> (without <>)\n")
            input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")

#FINAL SCREEN                  
def final_screen(user_session): #trovare dove metterla: penso dentro SequenceDownload
    print("\nDOWNLOAD DATA completed!")
    print("Now you can find the metadata files divided by projects inside the folder: MADAME/Downloads/" + Color.BOLD + Color.YELLOW + f"{user_session}" + Color.END)
    input("\nPress " + Color.BOLD + Color.PURPLE + "ENTER" + Color.END + " to return to the main menu ")
    return