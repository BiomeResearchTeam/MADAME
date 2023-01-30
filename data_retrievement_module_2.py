from Utilities import Color, Utilities
from SequencesDownload import SequencesDownload
from functions_modules import CheckTSV
from os import path
import os
import pandas as pd

def data_retrievement(user_session):

    while True:
        #Utilities.clear() 
        title = " DATA RETRIEVEMENT MODULE "
        print(Color.BOLD + Color.PURPLE + title.center(100, '-') + Color.END)
        print("\nDownload the data associated to the previously downloaded metadata.\n\nChoose one of the following options:")
        print(" 1 - Use '*_merged_experiments-metadata.tsv' file present the current session")
        print(" 2 - Use '*_merged_experiments-metadata.tsv' files present in any other location of your computer")
        print("\n >>> Your current session is " + Color.BOLD + Color.YELLOW +f"{user_session}" + Color.END + " <<<\n")
        print(" --- If you want to return to the main menu digit: " + Color.BOLD + Color.PURPLE + "main menu" + Color.END + " ---\n")
        user_data_input = input("\n>> Enter your choice: ").strip()

        if user_data_input in ("main menu", "MAIN MENU", "Main menu"):
            return

        elif user_data_input.isnumeric() == False:
            print(Color.BOLD + Color.RED + "\nWrong input" + Color.END, "expected a numeric input or <main menu> (without <>)\n\n")

        elif user_data_input.isnumeric() == True:
            user_data_input = int(user_data_input)
            if user_data_input not in (1,2):
                print("Error, enter a valid choice!\n")
                return

            else:
                if user_data_input == (1):
                    data_user_session = os.path.join("Downloads", user_session)
                    file_count = check_files(data_user_session)
                    if file_count == 0:
                        print(Color.BOLD + Color.RED + "\nError" + Color.END, "found 0 file. Are you sure the file is called '*_merged_experiments-metadata.tsv'? If not, please rename it\n")

                    elif file_count > 1:
                        print(Color.BOLD + Color.RED + "\nError" + Color.END, "found too many files. Please choose a folder containing only 1 '*_merged_experiments-metadata.tsv'")

                    else:
                        print("\nWhat data format do you want to download? fastq, sra, or submitted")
                        user_file_type = input(">> Enter your choice: ").strip().lower()
                        if user_file_type in ("main menu"):
                            return
                        elif user_file_type not in ("fastq", "sra", "submitted", "main menu"):
                            print(Color.BOLD + Color.RED +"Wrong input " + Color.END, "Write <fastq>, <sra>, or <submitted> (without <>)\n")
                        else:
                            merged_experiments = check_file_experiments(data_user_session)
                            e_df = read_experiments(data_user_session, merged_experiments)
                            SequencesDownload.runDownloadData(user_session, e_df, file_type = user_file_type)
                                    
                if user_data_input == (2):
                    user_data_local(user_session)
                    file_count = check_files(user_session)
                    

                    if file_count == 0:
                        print(Color.BOLD + Color.RED + "\nError" + Color.END, "found 0 file. Are you sure the file is called '*_merged_experiments-metadata.tsv'? If not, please rename it\n")

                    elif file_count > 1:
                        print(Color.BOLD + Color.RED + "\nError" + Color.END, "found too many files. Please choose a folder containing only 1 '*_merged_experiments-metadata.tsv'")

                    else:
                        merged_experiments = check_file_experiments(user_session)
                        e_df = read_experiments(user_session, merged_experiments)
                        SequencesDownload.runDownloadData(user_session, e_df, file_type = user_file_type)
                        

def user_data_local(user_session):
    Utilities.clear()
    while True:
        print("Enter the path for '*_merged_experiments-metadata.tsv' file. \nData will be downloaded in the folder indicated.")
        print("\n --- If you want to return to the main menu digit: " + Color.BOLD + Color.PURPLE + "main menu" + Color.END + " ---\n") #verificare se è vero o se torna al report
        user_data_local_path = input("\n>> Digit the path: ").strip()

        if user_data_local_path in ("main menu", "MAIN MENU", "Main menu"):
            data_retrievement(user_session)
                            
        if path.isdir(user_data_local_path) == False:
            if path.isfile(user_data_local_path) == True:
                print(Color.BOLD + Color.RED + "Error. " + Color.END, "Please digit the path for the folder containing '*_merged_experiments-metadata.tsv' file\n\n")
                return
            else:
                print(Color.BOLD + Color.RED + "Folder not found." + Color.END, " Maybe a typo? Try again\n\n")
                return
        else:
            return user_data_local_path



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