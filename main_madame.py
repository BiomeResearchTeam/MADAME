#!/usr/bin/python

from Utilities import Color, Utilities
from metadata_retrievement_module import metadata_retrievement
from publications_retrievement_module import publications_retrievement
from report_generation_module import report_generation
from data_retrievement_module_2 import data_retrievement
from report_2_in_corso import report_generation #lo sto ancora modificando, quando sarà pronto sarà il report_generation_module da usare
import os
from rich.tree import Tree
from rich import print as rich_print
from rich.panel import Panel
from rich.text import Text
from rich.console import Console
import os.path
import readline

user_session = ""

def main():

    while True:
        Utilities.clear()
        madame_logo() 

        print("\n Choose your working session, it will be created in MADAME/Downloads \n")
        print(" 1 - Create new session")
        print(" 2 - Continue with existing session") #only if downloads isn't empty..
        print("\n --- If you want to close MADAME digit: " + Color.BOLD + Color.PURPLE +"exit" + Color.END + " ---\n")
        
        while True:
            module_choice = input(">> Enter your option: ")
            if module_choice.isnumeric():
                module_choice = int(module_choice)
                if module_choice not in (1, 2):
                    print("Error, enter a valid choice!\n")
                    continue
                break
            else:
                if module_choice in ("exit", "EXIT", "Exit"):
                    print(Color.BOLD + Color.PURPLE + "\nGood bye, see you soon!\n" + Color.END)
                    exit()
                else:
                    print("Wrong input, expected a numeric input or <exit> (without <>), try again.\n") 
        

        if module_choice == 1:            
            new_session()

        existing_sessions = [d for d in os.listdir("Downloads") if os.path.isdir(os.path.join("Downloads", d)) and not d.startswith(".")]

        if module_choice == 2 and existing_sessions:
            existing_session()
            
        elif module_choice == 2 and not existing_session: 
            print("\n Error: " + Color.BOLD + Color.YELLOW + "MADAME/Downloads" + Color.END + " is empty.")
            input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to create a new session ")
            new_session()

# FOLDER CREATED BY USER INPUT

def new_session():
    
    Utilities.clear()
    madame_logo()
    title = Panel(Text("CREATE NEW SESSION", style = "b magenta", justify="center"), style = "b magenta")
    rich_print(title)

    print(" --- If you want to return to the main menu digit: " + Color.BOLD + Color.PURPLE + "main menu" + Color.END + " ---\n")
    
    user_session = ''
    while user_session.strip() == '': 
        user_session = str(input(">> Digit the folder name: "))
    
    if user_session in ("main menu", "MAIN MENU", "Main menu"):
        return

    while os.path.isdir(os.path.join("Downloads", user_session)):
        print("\n Error: " + Color.BOLD + Color.YELLOW + f"{user_session}" + Color.END + " folder already exists.")
        user_session = ''
        while user_session.strip() == '': 
            user_session = str(input(">> Please digit a different name: ")) 
            if user_session in ("main menu", "MAIN MENU", "Main menu"):
                return


    Utilities.createDirectory(os.path.join("Downloads", user_session))
    print("\n Your new folder was succesfully created: MADAME/Downloads/" + Color.BOLD + Color.YELLOW + f"{user_session}" + Color.END + "")
    
    # logger = Utilities.log("main_madame", user_session)
    # logger.debug(f"[USER-SESSION-CREATED]: MADAME/Downloads/{user_session}")

    input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue")

    menu(user_session)


# EXISTING FOLDER

def existing_session():

    Utilities.clear()
    madame_logo()
    title = Panel(Text("CONTINUE WITH EXISTING SESSION", style = "b magenta", justify="center"), style = "b magenta")
    rich_print(title)

    print("\n Which existing session do you want to select?\n")

    print(" --- If you want to return to the main menu digit: " + Color.BOLD + Color.PURPLE + "main menu" + Color.END + " ---\n")
    
    user_session = ''
    while user_session.strip() == '': # preventing empty inputs (giulia)
        user_session = str(input(" >> Digit the folder name (case sensitive): "))
        if user_session in ("main menu", "MAIN MENU", "Main menu"):
            return

    while not os.path.isdir(os.path.join("Downloads", user_session)):
        print("\n Error: there is no folder named " + Color.BOLD + Color.YELLOW + f"{user_session}" + Color.END + ".")
        print(" Here's your current sessions:\n")

        madame_tree = Tree("MADAME")
        downloads_branch = madame_tree.add("Downloads")
        dirs_branches = [d for d in os.listdir("Downloads") if os.path.isdir(os.path.join("Downloads", d)) and not d.startswith(".")]
        for dir in dirs_branches:
            downloads_branch.add(dir)

        rich_print(madame_tree)

        user_session = ''
        while user_session.strip() == '': # preventing empty inputs (giulia)
            user_session = str(input("\n >> Digit the folder name (case sensitive): ")) 
            if user_session in ("main menu", "MAIN MENU", "Main menu"):
                return

    menu(user_session)

def menu(user_session):

    while True:
        Utilities.clear()
        madame_logo()

        print("\n\n Which module do you want to use? \n")
        print(" 1 - Metadata retrievement module: metadata search and download")
        print(" 2 - Publication retrievement module: metadata- and data- associated publications download")
        print(" 3 - Report module: explore metadata and publication retrivement outputs")
        print(" 4 - Data retrievement module: metadata-associated data download")
        print("\n >>> Your current session is " + Color.BOLD + Color.YELLOW +f"{user_session}" + Color.END + " <<<\n")
        print(" --- If you want to change session digit: " + Color.BOLD + Color.PURPLE +"change" + Color.END + " ---")
        print(" --- If you want to close MADAME digit: " + Color.BOLD + Color.PURPLE +"exit" + Color.END + " ---\n")

        while True:
            module_choice = input(">> Enter your option: ")
            if module_choice.isnumeric():
                module_choice = int(module_choice)
                if module_choice not in (1, 2, 3, 4):
                    print("Error, enter a valid choice!\n")
                    continue
                break
            else:
                if module_choice in ("exit", "EXIT", "Exit"):
                    print(Color.BOLD + Color.PURPLE + "\nGood bye, see you soon!\n" + Color.END)
                    exit()
                elif module_choice in ("change", "CHANGE", "Change"):
                    main()
                else:
                    print("Wrong input, expected a numeric input, <change> or <exit> (without <>). Try again.\n") 
        
        Utilities.clear()

        if module_choice == 1:            
            metadata_retrievement(user_session)

        if module_choice == 2:
            publications_retrievement(user_session)

        if module_choice == 3:
            report_generation(user_session)

        if module_choice == 4:  
            data_retrievement(user_session)



def madame_logo():

    c = Console()
    c.print("\n                                                           ##############\n                                                       #####################\n                                                    ##########################\n                                                  #############################         ╭─────── [green]Welcome to MADAME[/green] ───────╮\n                                                 ###############################        │     [green]◊[/green] MetADAta MicrobiomE [green]◊[/green]     │\n                                           ####  ###############################        │                                 │\n                                          ######################################        │ [i]Designed to automate the process[/i]│\n                                         #######################################        │  [i]of data and metadata retrieval[/i] │\n                                         ######################################(        │                                 │\n                                         ########################################       ╰────────────────▼────────────────╯\n##     ##     ###     #######       ###  ###[green]##[/green]#####[green]##[/green]##[green]########[/green]##################\n###   ###    ## ##    ##    ##     ## ##  ##[green]###[/green]###[green]###[/green]##[green]##[/green]##########################          ╭─ [green]Biome Research Team[/green] ─╮\n#### ####   ##   ##   ##     ##   ##   ##  #[green]####[/green]#[green]####[/green]##[green]##[/green]########################            │   --- click me! ---   │\n## ### ##  ##     ##  ##     ##  ##     ##  [green]##[/green]#[green]###[/green]#[green]##[/green]##[green]######[/green]###################)            │ [white][link=https://github.com/]:computer: GitHub[/link][/white]             │\n##     ##  #########  ##     ##  #########  [green]##[/green]#####[green]##[/green]##[green]##[/green]######################)             │ [white][link=https://biome-research-team.mailchimpsites.com/]:dna: Website[/link][/white]            │\n##     ##  ##     ##  ##    ##   ##     ##  [green]##     ##  ##[/green]######################              │ [white][link=https://www.linkedin.com/company/biome-research-team/]:briefcase: Linkedin[/link][/white]           │\n##     ##  ##     ##  #######    ##     ##  [green]##     ##  ########[/green]#######**######               ╰───────────────────────╯\n                                                     ################     ***\n                                                   #################\n", style = "magenta")





if __name__ == "__main__":
    main()