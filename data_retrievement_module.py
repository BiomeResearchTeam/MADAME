from Utilities import Color
from SequencesDownload import SequencesDownload
from functions_modules import CheckTSV
import csv
import time 
from os import path
import os

def data_retrievement():

    while True:
        #clear() 
        title = " DATA RETRIVEMENT MODULE "
        print(Color.BOLD + Color.PURPLE + title.center(100, '-') + Color.END)
        print("\nDigit the path to the", Color.BOLD + "'_experiments-metadata.tsv'" + Color.END, "previously created with this tool ")
        
        print("\n --- If you want to return to the main menu digit: " 
        + Color.BOLD + Color.PURPLE + "main menu" + Color.END + " ---\n")

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
                        SequencesDownload.runDownloadData(listOfProjectIDs, file_type = user_file_type) #boh dà errori 
                        time.sleep(2)