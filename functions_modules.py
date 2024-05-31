from IDlist import GetIDlist
from Utilities import Color, Utilities, LoggerManager
from Project import Project
import time 
import csv
import os
from os import path
from rich import print as rich_print
from rich.panel import Panel
from rich.text import Text
from rich.console import Console
import pandas as pd

#QUERY ENA

def UserQueryENAInput(user_session):

    box = Panel(Text.assemble("Examples of queries:\n\n1) skin microbiome\n2) monkeypox\n\n>>> Your current session is ", (f"{user_session}", "rgb(255,255,0)"), " <<<\n\n--- If you want to return to the METADATA retrieval MODULE menu digit: ", ("back", "rgb(255,0,255)")," ---", style = None, justify="left"), title=Text.assemble((" ◊", "rgb(0,255,0)"), " QUERY ON ENA ", ("◊ ", "rgb(0,255,0)")), border_style= "rgb(255,0,255)", padding= (0,1))
    rich_print(box)


    user_query_input = ''
    while user_query_input.strip() == '':
        user_query_input = str(input("  >> Digit your query: "))
    

    return user_query_input


def UserDataTypeInput(user_query_input, user_data_type, user_session):

    user_choice = False
    umbrella_projects = []
    listOfAvailableAccessions = []
    listOfUnvailableAccessions = []

    console = Console()
    # Spinner for showing MADAME is working (this process can be lenghty)
    with console.status("\n⍗ Fetching records from ENA browser API, please wait...") as status:
        listOfAccessionIDs = GetIDlist.Query(user_session, user_query_input, user_data_type)

    # Check if there's umbrella projects - only if user searched for projects
    if user_data_type == "projects" and len(listOfAccessionIDs) != 0:
        console = Console()

        # Spinner for showing MADAME is working (this process can be lenghty)
        with console.status("\n☂ Checking for Umbrella Projects, please wait...") as status:
            umbrella_projects, projects = Project.getCheckedUmbrellaList(listOfAccessionIDs)

        total_of_umbrella = len(umbrella_projects)
        total_umbrella_plus_projects = total_of_umbrella + len(projects)

        # If there's at least one umbrella project among the project IDs:
        if total_of_umbrella != 0:

            # logger
            logger = LoggerManager.log(user_session)
            logger.debug(f"[FOUND-UMBRELLA-PROJECTS]: {umbrella_projects}")

            # Print warning to console
            rich_print(f"\n[yellow]WARNING[/yellow] - Found [rgb(0,255,0)]{total_umbrella_plus_projects}[/rgb(0,255,0)] projects, but [rgb(0,255,0)]{total_of_umbrella}[/rgb(0,255,0)] of them are [yellow]UMBRELLA projects[/yellow]:")

            # Print details about each umbrella (read experiment metadata online).
            # → Project IDs are clickable

            components_dict = {}
            for projectID in umbrella_projects:

                # Spinner for showing MADAME is working (this process can be lenghty)
                with console.status("\n☂ Calculating the component projects, please wait...") as status:
                    component_projects = Project.getComponentProjects(projectID, "online", user_session)
                    components_dict[projectID] = component_projects
                
                if len(component_projects) == 1:
                    rich_print(f"[yellow]☂[/yellow] [link=https://www.ebi.ac.uk/ena/browser/view/{projectID}]{projectID}[/link] → [rgb(0,255,0)]{len(component_projects)}[/rgb(0,255,0)] component project")

                    # logger
                    logger = LoggerManager.log(user_session)
                    logger.debug(f"[UMBRELLA-PROJECT]: {projectID} → {len(component_projects)} component project")

                
                else:
                    rich_print(f"[yellow]☂[/yellow] [link=https://www.ebi.ac.uk/ena/browser/view/{projectID}]{projectID}[/link] → [rgb(0,255,0)]{len(component_projects)}[/rgb(0,255,0)] component projects")

                    # logger
                    logger = LoggerManager.log(user_session)
                    logger.debug(f"[UMBRELLA-PROJECT]: {projectID} → {len(component_projects)} component projects")

            component_projects_list = [component for components in list(components_dict.values()) for component in components]

            # Print info box and let the user decide how to proceed
            print()
            console = Console()
            box = console.print(Panel(("Instead of holding data, umbrella projects group together multiple component projects that are part of the same research motivation or collaboration.\n→ Each umbrella can contain [yellow]a few to thousands[/yellow] of other projects, and [yellow]not all of them[/yellow] may be related to your query.\nMore info on [link=https://ena-docs.readthedocs.io/en/latest/retrieval/ena-project.html]ENA's documentation[/link]."), title=(":umbrella: Umbrella Projects - Info Box"), border_style= "rgb(255,255,0)", padding= (0,1), title_align="left"))

            rich_print("\n  [rgb(255,0,255)]1[/rgb(255,0,255)] - Exclude umbrella projects\n  [rgb(255,0,255)]2[/rgb(255,0,255)] - Include umbrella projects")

            while True:
                    
                user_choice = input("\n  >> How do you want to proceed? Enter your option: ")
                if user_choice.isnumeric():
                    user_choice = int(user_choice)
                    if user_choice not in (1, 2):
                        rich_print("[bold red]Error[/bold red], enter a valid choice!")
                        continue
                    break
                else:
                    print("[bold red]Error[/bold red], expected a numeric input. Try again.\n")


            # Proceed excluding umbrella projects
            if user_choice == 1:            
                listOfAccessionIDs = projects

                # logger
                logger = LoggerManager.log(user_session)
                logger.debug(f"[OPTION-1]: - EXCLUDE UMBRELLA PROJECTS")

            # Proceed including umbrella projects  
            if user_choice == 2:            

                # logger
                logger = LoggerManager.log(user_session)
                logger.debug(f"[OPTION-2]: - INCLUDE UMBRELLA PROJECTS")

                # Check if some of the projects in the list are also component of the umbrella we are including. If they are, they will be removed to avoid duplicate files
                components_to_remove = []
                if component_projects_list:
                    for component in component_projects_list:
                        if component in projects:
                            components_to_remove.append(component)

                if components_to_remove:

                    logger.debug(f"[OPTION-2]: - WARNING: {len(components_to_remove)} projects are component projects of umbrella projects already present in your list of accession IDs. To avoid downloading duplicate files, these components will be removed from the list.\nYou will find their metadata and data in their respective umbrella project:")
                    
                    if len(components_to_remove) > 1:
                        rich_print(f"\n[yellow]WARNING[/yellow] - [rgb(0,255,0)]{len(components_to_remove)}[/rgb(0,255,0)] projects are component projects of [yellow]umbrella projects[/yellow] already present in your list of accession IDs. [u]To avoid downloading duplicate files[/u], these components will be [u]removed[/u] from the list.\nYou will find their metadata and data in their respective umbrella project:\n")
                    else:
                        rich_print(f"\n[yellow]WARNING[/yellow] - [rgb(0,255,0)]{len(components_to_remove)}[/rgb(0,255,0)] project is a component project of an [yellow]umbrella project[/yellow] already present in your list of accession IDs. [u]To avoid downloading duplicate files[/u], this component will be [u]removed[/u] from the list.\nYou will find its metadata and data in its umbrella project:\n")

                    for component in components_to_remove:
                        for key, value in components_dict.items():
                            if isinstance(value, list) and component in value:
                                projectID = key
                        rich_print(f"[link=https://www.ebi.ac.uk/ena/browser/view/{component}]{component}[/link] → [yellow]☂[/yellow] [link=https://www.ebi.ac.uk/ena/browser/view/{projectID}]{projectID}[/link]")
                        logger.debug(f"{component} → ☂ {projectID}")

                    #Give time to user to read the warning
                    input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")

                    listOfAccessionIDs = [x for x in projects if x not in components_to_remove] + umbrella_projects


                else:
                    listOfAccessionIDs = projects + umbrella_projects      

        # If none of the projects are umbrella
        else:
            listOfAccessionIDs = projects

    # Fetch and print query details
    if user_choice == False or user_choice == 1:
        total_of_accessions = GetIDlist.QueryDetails(user_session, listOfAccessionIDs) 
    if user_choice == 2: 
        total_of_accessions = GetIDlist.QueryDetails(user_session, listOfAccessionIDs, umbrella_projects)

    if total_of_accessions > 1:
        # Check Accession availability and print details, 
        listOfAvailableAccessions, listOfUnvailableAccessions = Project.getAvailableAccessions(user_session, listOfAccessionIDs)

        rich_print(f"\n  >> [rgb(0,255,0)]{len(listOfAvailableAccessions)}[/rgb(0,255,0)] out of [rgb(0,255,0)]{len(listOfAccessionIDs)}[/rgb(0,255,0)] accessions are available. Check the details below:\n")

    if len(listOfAvailableAccessions) > 0:
        # The loop prints each accession one next to each other, they can be clicked and the last item (else) is printed differently, without the comma. If it's a list of projects comprehensive of umbrella projects, they are printed in yellow and next to the "☂" character.
        rich_print(f"[rgb(255,0,255)]Available accessions → [/rgb(255,0,255)]", end="")
        for accession in listOfAvailableAccessions[:-1]:
            if accession in umbrella_projects:
                rich_print(f"[link=https://www.ebi.ac.uk/ena/browser/view/{accession}][yellow]☂ {accession}[/yellow][/link], ", end="")
            else:
                rich_print(f"[link=https://www.ebi.ac.uk/ena/browser/view/{accession}]{accession}[/link], ", end="")
        else:
            if listOfAvailableAccessions[-1] in umbrella_projects:
                rich_print(f"[link=https://www.ebi.ac.uk/ena/browser/view/{listOfAvailableAccessions[-1]}][yellow]☂ {listOfAvailableAccessions[-1]}[/yellow][/link].\n")
            else:
                rich_print(f"[link=https://www.ebi.ac.uk/ena/browser/view/{listOfAvailableAccessions[-1]}]{listOfAvailableAccessions[-1]}[/link].\n")

    if len(listOfUnvailableAccessions) > 0:

        rich_print(f"[rgb(255,0,255)]Unavailable accessions → [/rgb(255,0,255)]", end="")
        for accession in listOfUnvailableAccessions[:-1]:
            if accession in umbrella_projects:
                rich_print(f"[link=https://www.ebi.ac.uk/ena/browser/view/{accession}][yellow]☂ {accession}[/yellow][/link], ", end="")
            else:
                rich_print(f"[link=https://www.ebi.ac.uk/ena/browser/view/{accession}]{accession}[/link], ", end="")
        else:
            if listOfUnvailableAccessions[-1] in umbrella_projects:
                rich_print(f"[link=https://www.ebi.ac.uk/ena/browser/view/{listOfUnvailableAccessions[-1]}][yellow]☂ {listOfUnvailableAccessions[-1]}[/yellow][/link].\n")
            else:
                rich_print(f"[link=https://www.ebi.ac.uk/ena/browser/view/{listOfUnvailableAccessions[-1]}]{listOfUnvailableAccessions[-1]}[/link].\n")

    # Create listOfAccessionIDs.tsv 
    Project.listOfAccessionIDsTSV(listOfAvailableAccessions, user_session)

    # Update listOfAccessionIDs.tsv with the new column umbrella (True/False) if user chose to include them
    if user_choice == 2:
        
        check_umbrella = []

        for projectID in listOfAvailableAccessions:
            if projectID in projects:
                check_umbrella.append(False)
            if projectID in umbrella_projects:
                check_umbrella.append(True)

        listOfAccessionIDs_file = (os.path.join("Downloads", user_session, f'{user_session}_listOfAccessionIDs.tsv'))
        df = pd.read_csv(listOfAccessionIDs_file, sep='\t', dtype=str)
        df['umbrella'] = check_umbrella
        df.to_csv(listOfAccessionIDs_file, sep="\t", index=False)

        # logger
        logger = LoggerManager.log(user_session)
        logger.debug(f"{user_session}_listOfAccessionIDs.tsv UPDATED WITH UMBRELLA COLUMN")


    # Print warning if there is no available accession
    if len(listOfAvailableAccessions) == 0 or total_of_accessions == 0:
        print('Do you want to ' + Color.BOLD + 'try again?' + Color.END)
        input("Press " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")
    else:
        logger = LoggerManager.log(user_session)
        logger.debug(f"{user_session}_listOfAccessionIDs.tsv CREATED")
        print("Now you can find the available accession IDs list here: MADAME/Downloads/" + Color.BOLD + Color.YELLOW + f"{user_session}" + Color.END + f"/{user_session}_listOfAccessionIDs.tsv")
        input("\n\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue.")

    # If there's umbrella projects, return available accessions as a dictionary (True/False)
    if user_choice == 2:  
        dictOfAvailableAccessions =  dict(zip(listOfAvailableAccessions, check_umbrella))
        return dictOfAvailableAccessions

    # Return available accessions as a list
    return listOfAvailableAccessions
        

#DIGIT ACCESSION CODES

def UserDigitCodesInput(user_session):

    box = Panel(Text.assemble("Digit the accession codes you are interested in, separated by ", ("comma", "u"), ".\nYou can also digit accession codes as a range → ", ("ERR1701208-ERR1701215", "u"), "\n\nExamples of accession codes:\n1) PRJNA689547\n2) ERP107880, DRP004449, SRP187334\n3) SRX7355606-SRX7355624, SRR8890490\n\n>>> Your current session is ", (f"{user_session}", "rgb(255,255,0)"), " <<<\n\n--- If you want to return to the METADATA retrieval MODULE menu digit: ", ("back", "rgb(255,0,255)")," ---", style = None, justify="left"), title=Text.assemble((" ◊", "rgb(0,255,0)"), " DIGIT LIST OF ACCESSION CODES ", ("◊ ", "rgb(0,255,0)")), border_style= "rgb(255,0,255)", padding= (0,1))
    rich_print(box)

    user_query_input = ''
    while user_query_input.strip() == '':
        user_query_input = str(input("  >> Digit your list: "))

    if user_query_input.lower() in ("back"):
        return "back"

    # Clean user input
    user_query_input = user_query_input.replace(" ", "") # remove whitespaces
    user_query_input = list(user_query_input.split(",")) # split string with comma 
    user_query_input = list(dict.fromkeys(user_query_input)) # remove duplicates
    
    return user_query_input


def UserDigitCodesIDlist(user_query_input, user_session):

    user_choice = False
    umbrella_projects = []

    # Check validity of digited accessions
    listOfAccessionIDs, dictionaryOfAccessionIDs = GetIDlist.IDlistFromUserInput(user_session, user_input = user_query_input)
    if ((len(listOfAccessionIDs) == 0) and (all(len(value) == 0 for value in dictionaryOfAccessionIDs.values()))):
        return listOfAccessionIDs
    
    # Check if among the inputted accessions there's umbrella projects - only if project IDs were inputted
    
    projects_IDs = dictionaryOfAccessionIDs["projects"]
    
    if projects_IDs and len(listOfAccessionIDs) != 0:
        console = Console()

        # Spinner for showing MADAME is working (this process can be lenghty)
        with console.status("\n☂ Checking for Umbrella Projects, please wait...") as status:
            umbrella_projects, projects = Project.getCheckedUmbrellaList(projects_IDs)

        total_of_umbrella = len(umbrella_projects)
        total_umbrella_plus_projects = total_of_umbrella + len(projects)

        # If there's at least one umbrella project among the project IDs:
        if total_of_umbrella != 0:

            # logger
            logger = LoggerManager.log(user_session)
            logger.debug(f"[FOUND-UMBRELLA-PROJECTS]: {umbrella_projects}")

            # Print warning to console
            rich_print(f"\n[yellow]WARNING[/yellow] - [rgb(0,255,0)]{total_of_umbrella}[/rgb(0,255,0)] out of [rgb(0,255,0)]{len(listOfAccessionIDs)}[/rgb(0,255,0)] inputted accessions are [yellow]UMBRELLA projects[/yellow]:")

            # Print details about each umbrella (read experiment metadata online).
            # → Project IDs are clickable

            components_dict = {}
            for projectID in umbrella_projects:

                # Spinner for showing MADAME is working (this process can be lenghty)
                with console.status("\n☂ Calculating the component projects, please wait...") as status:
                    component_projects = Project.getComponentProjects(projectID, "online", user_session)
                    components_dict[projectID] = component_projects
                
                if len(component_projects) == 1:
                    rich_print(f"[yellow]☂[/yellow] [link=https://www.ebi.ac.uk/ena/browser/view/{projectID}]{projectID}[/link] → [rgb(0,255,0)]{len(component_projects)}[/rgb(0,255,0)] component project")

                    # logger
                    logger = LoggerManager.log(user_session)
                    logger.debug(f"[UMBRELLA-PROJECT]: {projectID} → {len(component_projects)} component project")
  
                else:
                    rich_print(f"[yellow]☂[/yellow] [link=https://www.ebi.ac.uk/ena/browser/view/{projectID}]{projectID}[/link] → [rgb(0,255,0)]{len(component_projects)}[/rgb(0,255,0)] component projects")

                    # logger
                    logger = LoggerManager.log(user_session)
                    logger.debug(f"[UMBRELLA-PROJECT]: {projectID} → {len(component_projects)} component projects")

            component_projects_list = [component for components in list(components_dict.values()) for component in components]

            # Print info box and let the user decide how to proceed
            print()
            console = Console()
            box = console.print(Panel(("Instead of holding data, umbrella projects group together multiple component projects that are part of the same research motivation or collaboration.\n→ Each umbrella can contain [yellow]a few to thousands[/yellow] of other projects, and [yellow]not all of them[/yellow] may be related to your query.\nMore info on [link=https://ena-docs.readthedocs.io/en/latest/retrieval/ena-project.html]ENA's documentation[/link]."), title=(":umbrella: Umbrella Projects - Info Box"), border_style= "rgb(255,255,0)", padding= (0,1), title_align="left"))

            rich_print("\n  [rgb(255,0,255)]1[/rgb(255,0,255)] - Exclude umbrella projects\n  [rgb(255,0,255)]2[/rgb(255,0,255)] - Include umbrella projects")

            while True:
                    
                user_choice = input("\n  >> How do you want to proceed? Enter your option: ")
                if user_choice.isnumeric():
                    user_choice = int(user_choice)
                    if user_choice not in (1, 2):
                        rich_print("[bold red]Error[/bold red], enter a valid choice!")
                        continue
                    break
                else:
                    print("[bold red]Error[/bold red], expected a numeric input. Try again.\n")


            # Proceed excluding umbrella projects
            if user_choice == 1:            

                # logger
                logger = LoggerManager.log(user_session)
                logger.debug(f"[OPTION-1]: - EXCLUDE UMBRELLA PROJECTS")

                dictionaryOfAccessionIDs["projects"] = projects
                listOfAccessionIDs = [x for x in listOfAccessionIDs if x not in umbrella_projects]

            # Proceed including umbrella projects  
            if user_choice == 2:            

                # logger
                logger = LoggerManager.log(user_session)
                logger.debug(f"[OPTION-2]: - INCLUDE UMBRELLA PROJECTS")

                # Check if some of the projects in the list are also component of the umbrella we are including. If they are, they will be removed to avoid duplicate files
                components_to_remove = []
                if component_projects_list:
                    for component in component_projects_list:
                        if component in projects:
                            components_to_remove.append(component)

                if components_to_remove:

                    logger.debug(f"[OPTION-2]: - WARNING: {len(components_to_remove)} projects are component projects of umbrella projects already present in your list of accession IDs. To avoid downloading duplicate files, these components will be removed from the list.\nYou will find their metadata and data in their respective umbrella project:")
                    
                    if len(components_to_remove) > 1:
                        rich_print(f"\n[yellow]WARNING[/yellow] - [rgb(0,255,0)]{len(components_to_remove)}[/rgb(0,255,0)] projects are component projects of [yellow]umbrella projects[/yellow] already present in your list of accession IDs. [u]To avoid downloading duplicate files[/u], these components will be [u]removed[/u] from the list.\nYou will find their metadata and data in their respective umbrella project:\n")
                    else:
                        rich_print(f"\n[yellow]WARNING[/yellow] - [rgb(0,255,0)]{len(components_to_remove)}[/rgb(0,255,0)] project is a component project of an [yellow]umbrella project[/yellow] already present in your list of accession IDs. [u]To avoid downloading duplicate files[/u], this component will be [u]removed[/u] from the list.\nYou will find its metadata and data in its umbrella project:\n")

                    for component in components_to_remove:
                        for key, value in components_dict.items():
                            if isinstance(value, list) and component in value:
                                projectID = key
                        rich_print(f"[link=https://www.ebi.ac.uk/ena/browser/view/{component}]{component}[/link] → [yellow]☂[/yellow] [link=https://www.ebi.ac.uk/ena/browser/view/{projectID}]{projectID}[/link]")
                        logger.debug(f"{component} → ☂ {projectID}")

                    #Give time to user to read the warning
                    input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")

                    dictionaryOfAccessionIDs["projects"] = [x for x in projects if x not in components_to_remove] + umbrella_projects
                    listOfAccessionIDs = [x for x in listOfAccessionIDs if x not in components_to_remove]
                
                else: 
                    dictionaryOfAccessionIDs["projects"] = projects + umbrella_projects      

        # If none of the projects are umbrella
        else:
            dictionaryOfAccessionIDs["projects"] = projects


    # Fetch and print query details
    if user_choice == False or user_choice == 1:    
        GetIDlist.IDlistFromUserInputDetails(user_session, dictionaryOfAccessionIDs)

    if user_choice == 2: 
        GetIDlist.IDlistFromUserInputDetails(user_session, dictionaryOfAccessionIDs, umbrella_projects)


    # Check Accession availability and print details
    listOfAvailableAccessions, listOfUnvailableAccessions = Project.getAvailableAccessions(user_session, listOfAccessionIDs)

    rich_print(f"\n  >> [rgb(0,255,0)]{len(listOfAvailableAccessions)}[/rgb(0,255,0)] out of [rgb(0,255,0)]{len(listOfAccessionIDs)}[/rgb(0,255,0)] accessions are available. Check the details below:\n")

    if len(listOfAvailableAccessions) > 0:
        # The loop prints each accession one next to each other, they can be clicked and the last item (else) is printed differently, without the comma. If it's a list of projects comprehensive of umbrella projects, they are printed in yellow and next to the "☂" character.
        rich_print(f"[rgb(255,0,255)]Available accessions → [/rgb(255,0,255)]", end="")
        for accession in listOfAvailableAccessions[:-1]:
            if accession in umbrella_projects:
                rich_print(f"[link=https://www.ebi.ac.uk/ena/browser/view/{accession}][yellow]☂ {accession}[/yellow][/link], ", end="")
            else:
                rich_print(f"[link=https://www.ebi.ac.uk/ena/browser/view/{accession}]{accession}[/link], ", end="")
        else:
            if listOfAvailableAccessions[-1] in umbrella_projects:
                rich_print(f"[link=https://www.ebi.ac.uk/ena/browser/view/{listOfAvailableAccessions[-1]}][yellow]☂ {listOfAvailableAccessions[-1]}[/yellow][/link].\n")
            else:
                rich_print(f"[link=https://www.ebi.ac.uk/ena/browser/view/{listOfAvailableAccessions[-1]}]{listOfAvailableAccessions[-1]}[/link].\n")

    if len(listOfUnvailableAccessions) > 0:
        
        rich_print(f"[rgb(255,0,255)]Unavailable accessions → [/rgb(255,0,255)]", end="")
        for accession in listOfUnvailableAccessions[:-1]:
            if accession in umbrella_projects:
                rich_print(f"[link=https://www.ebi.ac.uk/ena/browser/view/{accession}][yellow]☂ {accession}[/yellow][/link], ", end="")
            else:
                rich_print(f"[link=https://www.ebi.ac.uk/ena/browser/view/{accession}]{accession}[/link], ", end="")
        else:
            if listOfUnvailableAccessions[-1] in umbrella_projects:
                rich_print(f"[link=https://www.ebi.ac.uk/ena/browser/view/{listOfUnvailableAccessions[-1]}][yellow]☂ {listOfUnvailableAccessions[-1]}[/yellow][/link].\n")
            else:
                rich_print(f"[link=https://www.ebi.ac.uk/ena/browser/view/{listOfUnvailableAccessions[-1]}]{listOfUnvailableAccessions[-1]}[/link].\n")


    # Create listOfAccessionIDs.tsv 
    Project.listOfAccessionIDsTSV(listOfAvailableAccessions, user_session)

    # Update listOfAccessionIDs.tsv with the new column umbrella (True/False) if user chose to include them
    if user_choice == 2:
        
        check_umbrella = []

        for accession in listOfAvailableAccessions:
            if accession not in umbrella_projects:
                check_umbrella.append(False)
            if accession in umbrella_projects:
                check_umbrella.append(True)

        listOfAccessionIDs_file = (os.path.join("Downloads", user_session, f'{user_session}_listOfAccessionIDs.tsv'))
        df = pd.read_csv(listOfAccessionIDs_file, sep='\t', dtype=str)
        df['umbrella'] = check_umbrella
        df.to_csv(listOfAccessionIDs_file, sep="\t", index=False)

        # logger
        logger = LoggerManager.log(user_session)
        logger.debug(f"{user_session}_listOfAccessionIDs.tsv UPDATED WITH UMBRELLA COLUMN")

    # Print warning if there is no available accession
    if len(listOfAvailableAccessions) == 0:
        print('Do you want to ' + Color.BOLD + 'try again?' + Color.END)
        input("Press " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")
    else:
        logger = LoggerManager.log(user_session)
        logger.debug(f"{user_session}_listOfAccessionIDs.tsv CREATED")
        print("Now you can find the available accession IDs list here: MADAME/Downloads/" + Color.BOLD + Color.YELLOW + f"{user_session}" + f"/{user_session}_listOfAccessionIDs.tsv" + Color.END)
        input("\n\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue.")

    # If there's umbrella projects, return available accessions as a dictionary (True/False)
    if user_choice == 2:  
        dictOfAvailableAccessions =  dict(zip(listOfAvailableAccessions, check_umbrella))
        return dictOfAvailableAccessions

    # Return available accessions as a list
    return listOfAvailableAccessions


#FILE ACCESSION CODES

def UserFileCodesInput(user_session):
    Utilities.clear()

    box = Panel(Text.assemble("Load a file containing the accession codes you are interested in. File format must be .csv or .tsv\n\n>>> Your current session is ", (f"{user_session}", "rgb(255,255,0)"), " <<<\n\n--- If you want to return to the METADATA retrieval MODULE menu digit: ", ("back", "rgb(255,0,255)")," ---", style = None, justify="left"), title=Text.assemble((" ◊", "rgb(0,255,0)"), " INPUT ACCESSION CODES FILE ", ("◊ ", "rgb(0,255,0)")), border_style= "rgb(255,0,255)", padding= (0,1))
    rich_print(box)

        
    csv_file_input = input("  >> Enter your csv or tsv file path: ")
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

        listOfProjectIDs = list(dict.fromkeys(listOfProjectIDs)) # remove duplicates
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


