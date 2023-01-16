from Utilities import Color, Utilities
from SequencesDownload import SequencesDownload
from functions_modules import CheckTSV
import csv
import time 
from os import path
import os

def data_retrievement(user_session):

    while True:
        Utilities.clear() 
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
            user_report_input = int(user_data_input)
            if user_data_input not in (1,2):
                print("Error, enter a valid choice!\n")
                return

            else:
                if user_data_input == (1):
                    user_data_input = os.path.join("Downloads", user_session)
                    file_count = check_files(user_session)


                if user_data_input == (2):
                    user_data_local_path = user_data_local()
                    file_count = check_files(user_session)




        listOfProjectIDs_abs_path = str(input("\n>> Enter the path to your _listOfProjectIDs.tsv: "))

        if listOfProjectIDs_abs_path in ("main menu", "MAIN MENU", "Main menu"):
            return

        else: 
            file_extension = CheckTSV(listOfProjectIDs_abs_path)
            
            if file_extension[1] not in ('.tsv'):
                print(Color.BOLD + Color.RED + "File extension is not .tsv" + Color.END, " Please enter the absolute path of the file (file included)")
                return
                
            else:
                print("\nWhat data format do you want to download? fastq, sra, or submitted")
                user_file_type = input(">> Enter your choice: ")
                user_file_type = user_file_type.strip()

                if user_file_type not in ("fastq", "sra", "submitted"):
                    print(Color.BOLD + Color.RED +"Wrong input " + Color.END, "Write <fastq>, <sra>, or <submitted> (without <>)\n")
                    
                else:
                    listOfProjectIDs_path = os.sep.join(os.path.normpath(listOfProjectIDs_abs_path).split(os.sep)[-2:])
                    print(listOfProjectIDs_path)
                    
                    with open(listOfProjectIDs_path, 'r') as r:
                        listOfProjectIDs_reader = csv.reader(r, delimiter='\t')
                        listOfProjectIDs_list = list(listOfProjectIDs_reader)
                        listOfProjectIDs = [item for sublist in listOfProjectIDs_list for item in sublist]
                        SequencesDownload.runDownloadData(listOfProjectIDs, file_type = user_file_type)
                        time.sleep(2)




def user_data_local():
    Utilities.clear()
    while True:
        print("Enter the path for '*_merged_experiments-metadata.tsv' file. \nData will be downloaded in the folder indicated.")
        print("\n --- If you want to return to the main menu digit: " + Color.BOLD + Color.PURPLE + "main menu" + Color.END + " ---\n") #verificare se è vero o se torna al report
        user_data_local_path = input("\n>> Digit the path: ").strip()
                            
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
def check_files(user_session):
    count = 0
    for file in os.listdir(user_session):
        if file.endswith(("_merged_experiments-metadata.tsv")):
            print(Color.BOLD + Color.GREEN + "Found" + Color.END, f"{file}")
            count += 1   
    return count    

def check_file_experiments(user_session):
    for file in os.listdir(user_session):
        if file.endswith("_merged_experiments-metadata.tsv"):
            return file