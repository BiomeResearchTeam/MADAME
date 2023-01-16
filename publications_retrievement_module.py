from GetPublications import GetPublications
from Utilities import Color
from functions_modules import CheckTSV
import os
import pandas as pd


def publications_retrievement(user_session):
    
    while True:
        #clear() 
        title = " PUBLICATIONS RETRIEVEMENT MODULE "
        print(Color.BOLD + Color.PURPLE + title.center(100, '-') + Color.END)
        print("\nDigit the path to the", Color.BOLD + "'_listOfAccessionIDs.tsv'" + Color.END, "previously created with this tool ")
        
        print("\n --- If you want to return to the main menu digit: " 
        + Color.BOLD + Color.PURPLE + "main menu" + Color.END + " ---\n")

        listOfProjectIDs_abs_path = str(input("\n>> Now please enter the path to your _listOfAccessionIDs.tsv: "))

        if listOfProjectIDs_abs_path in ("main menu", "MAIN MENU", "Main menu"):
            return

        else: 
            file_extension = CheckTSV(listOfProjectIDs_abs_path)

            if file_extension[1] not in ('.tsv'):
                print(Color.BOLD + Color.RED + "File extension is not .tsv" + Color.END, " Please enter the absolute path of the file (file included)")
                return

            else: 
                #listOfProjectIDs_path = os.sep.join(os.path.normpath(listOfProjectIDs_abs_path).split(os.sep)[-2:])
                #  with open(listOfProjectIDs_path, 'r') as r:
                #     listOfProjectIDs_reader = csv.reader(r, delimiter='\t')
                #     listOfProjectIDs_list = list(listOfProjectIDs_reader)
                #     listOfProjectIDs = [item for sublist in listOfProjectIDs_list for item in sublist]
                #     GetPublications.runGetPublications(listOfProjectIDs)
                
                # TEMPORANEO, DA SISTEMARE
                e_df = pd.read_csv(listOfProjectIDs_abs_path, delimiter='\t', infer_datetime_format=True)
                listOfProjectIDs = e_df["study_accession"].unique().tolist()
                GetPublications.runGetPublications(listOfProjectIDs, user_session)


# da strutturare come data retrievement module..
# checkTSV entra in un loop di file not found    
