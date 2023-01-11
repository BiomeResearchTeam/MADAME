from GetPublications import GetPublications
from Utilities import Color
from functions_modules import CheckTSV
import os
import csv


def publications_retrievement():
    
    while True:
        #clear() 
        title = " PUBLICATIONS RETRIVEMENT MODULE "
        print(Color.BOLD + Color.PURPLE + title.center(100, '-') + Color.END)
        print("\nDigit the path to the", Color.BOLD + "'_listOfProjectIDs.tsv'" + Color.END, "previously created with this tool ")
        
        print("\n --- If you want to return to the main menu digit: " 
        + Color.BOLD + Color.PURPLE + "main menu" + Color.END + " ---\n")

        listOfProjectIDs_abs_path = str(input("\n>> Now please enter the path to your _listOfProjectIDs.tsv: "))

        if listOfProjectIDs_abs_path in ("main menu", "MAIN MENU", "Main menu"):
            return

        else: 
            file_extension = CheckTSV(listOfProjectIDs_abs_path)

            if file_extension[1] not in ('.tsv'):
                print(Color.BOLD + Color.RED + "File extension is not .tsv" + Color.END, " Please enter the absolute path of the file (file included)")
                return

            else: 
                listOfProjectIDs_path = os.sep.join(os.path.normpath(listOfProjectIDs_abs_path).split(os.sep)[-2:])
                with open(listOfProjectIDs_path, 'r') as r:
                    listOfProjectIDs_reader = csv.reader(r, delimiter='\t')
                    listOfProjectIDs_list = list(listOfProjectIDs_reader)
                    listOfProjectIDs = [item for sublist in listOfProjectIDs_list for item in sublist]
                    GetPublications.runGetPublications(listOfProjectIDs)