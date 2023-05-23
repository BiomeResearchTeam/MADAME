from IDlist import GetIDlist
from Utilities import Color
from Project import Project
import time 
import csv
import os
from os import path
from rich import print as rich_print
from rich.panel import Panel
from rich.text import Text
from rich.console import Console

#QUERY ENA

def UserQueryENAInput(user_session):

    title = Panel(Text("QUERY ON ENA", style = "b magenta", justify="center"), style = "b magenta")
    rich_print(title)

    print("\nExamples of queries:\n"
            "1) skin microbiome ")
    print("2) monkeypox")
    print("\n >>> Your current session is " + Color.BOLD + Color.YELLOW +f"{user_session}" + Color.END + " <<<\n")
    print(" --- If you want to return to the METADATA RETRIEVEMENT MODULE menu digit: " 
            + Color.BOLD + Color.PURPLE + "back" + Color.END + " ---\n")   

    user_query_input = ''
    while user_query_input.strip() == '':
        user_query_input = str(input(">> Digit your query: "))
    

    return user_query_input


def UserDataTypeInput(user_query_input, user_data_type, user_session):

    console = Console()
    with console.status("\nFetching records from ENA browser API, please wait...") as status:
        listOfAccessionIDs = GetIDlist.Query(user_session, user_query_input, user_data_type)
    GetIDlist.QueryDetails(user_session, listOfAccessionIDs) 
    listOfAvailableProjects = Project.getAvailableAccessions(user_session, listOfAccessionIDs)
    Project.listOfAccessionIDsTSV(listOfAvailableProjects, user_session)
    if len(listOfAvailableProjects) == 0:
        print('Do you want to ' + Color.BOLD + 'try again?' + Color.END)
        input("Press " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")
    else:
        print("Now you can find the available accession IDs list here: MADAME/Downloads/" + Color.BOLD + Color.YELLOW + f"{user_session}" + Color.END + f"/{user_session}_listOfAccessionIDs.tsv")
        input("\n\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue.")
                
    return listOfAvailableProjects
        

#DIGIT ACCESSION CODES

def UserDigitCodesInput(user_session):
    # title = " DIGIT LIST OF ACCESSION CODES "
    # print(Color.BOLD + Color.GREEN + title.center(100, '-') + Color.END)
    title = Panel(Text("DIGIT LIST OF ACCESSION CODES", style = "b magenta", justify="center"), style = "b magenta")
    rich_print(title)

    print("\nDigit the accession codes you are interested in, separated by comma.")
    print("\nExamples of accession codes:\n", "1) PRJNA689547\n", "2) ERP107880, DRP004449, SRP187334") 
    print("\n >>> Your current session is " + Color.BOLD + Color.YELLOW +f"{user_session}" + Color.END + " <<<\n")
    print(" --- If you want to return to the METADATA RETRIEVEMENT MODULE menu digit: " + Color.BOLD + Color.PURPLE 
        + "back" + Color.END + " ---\n")
    
    user_query_input = ''
    while user_query_input.strip() == '':
        user_query_input = str(input(">> Digit your list: "))

    if user_query_input in ("back", "BACK", "Back"):
        return "back"

    # Clean user input
    user_query_input = user_query_input.replace(" ", "") # remove whitespaces
    user_query_input = list(user_query_input.split(",")) # split string with comma 
    user_query_input = list(dict.fromkeys(user_query_input)) # remove duplicates
    
    return user_query_input


def UserDigitCodesIDlist(user_query_input, user_session):

    # Check validity of accessions
    listOfAccessionIDs, dictionaryOfAccessionIDs = GetIDlist.IDlistFromUserInput(user_session, user_input = user_query_input)

    # Spinner for showing MADAME is working (this process can be lenghty)
    console = Console()
    with console.status("Fetching details of entered accessions, please wait...") as status:
        GetIDlist.IDlistFromUserInputDetails(dictionaryOfAccessionIDs)

    listOfAvailableAccessions = Project.getAvailableAccessions(user_session, listOfAccessionIDs)
    Project.listOfAccessionIDsTSV(listOfAvailableAccessions, user_session)

    if len(listOfAvailableAccessions) == 0:
        print('Do you want to ' + Color.BOLD + 'try again?' + Color.END)
        input("Press " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")
    else:
        print("Now you can find the available accession IDs list here: MADAME/Downloads/" + Color.BOLD + Color.YELLOW + f"{user_session}" + f"/{user_session}_listOfAccessionIDs.tsv" + Color.END)
        input("\n\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue.")

    return listOfAvailableAccessions


#FILE ACCESSION CODES

def UserFileCodesInput(user_session):
    
    title = Panel(Text("INPUT ACCESSION CODES FILE", style = "b magenta", justify="center"), style = "b magenta")
    rich_print(title)

    print("\n Load a file containing the accession codes you are interested in. File must have .csv or .tsv format.")
    print("\n >>> Your current session is " + Color.BOLD + Color.YELLOW +f"{user_session}" + Color.END + " <<<\n")
    print(" --- If you want to return to the METADATA RETRIEVEMENT MODULE menu digit: " + Color.BOLD + Color.PURPLE 
            + "back" + Color.END + " ---\n")
        
    csv_file_input = input(">> Enter your csv or tsv file path: ")
    csv_file_input = csv_file_input.strip()

    return csv_file_input


def UserFileCodesIDlist(csv_file_input):
    
    with open(csv_file_input, 'r') as r:
        csv_file_extension = os.path.splitext(csv_file_input)

        if csv_file_extension[1] not in ('.csv', '.tsv'):
            print(Color.BOLD + Color.RED + "File extension not .csv or .tsv" + Color.END, " please use the right format")
            return

        if csv_file_extension[1] == '.csv':
            csv_file_read = csv.reader(r, delimiter=',')
            list_accession_codes_csv_file = list(csv_file_read) 
            listOfProjectIDs = [item for sublist in list_accession_codes_csv_file for item in sublist]

        if csv_file_extension[1] == '.tsv':
            csv_file_read = csv.reader(r, delimiter='\t')
            list_accession_codes_csv_file = list(csv_file_read)
            listOfProjectIDs = [item for sublist in list_accession_codes_csv_file for item in sublist]

        return listOfProjectIDs


#TSV INPUT (_experiment_metadata.tsv & listO)

def CheckTSV(file_path):
    
    while True:
        if path.isfile(file_path) == False:
            print(Color.BOLD + Color.RED + "File not found." + Color.END, " Maybe a typo? Try again\n")
            time.sleep(3)
            continue
        else: 
            file_extension = os.path.splitext(file_path)
            return file_extension


