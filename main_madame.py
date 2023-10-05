#!/usr/bin/python

from Utilities import Color, Utilities, LoggerManager
from metadata_retrieval_module import metadata_retrieval
from publications_retrieval_module import publications_retrieval
from report_generation_module import report_generation
from data_retrieval_module import data_retrieval
import os
from rich.tree import Tree
from rich import print as rich_print
from rich.panel import Panel
from rich.text import Text
from rich.console import Console
from rich.theme import Theme
import os.path
import platform
if platform.system() != "Windows":
    import readline

user_session = ""

def main():

    while True:
        Utilities.clear()
        if platform.system() != "Windows":
            readline.parse_and_bind('tab: complete')
            readline.set_completer_delims(' \t\n')
        madame_logo()

        box = Panel(Text.assemble(("◊", "rgb(0,255,0)"), " Choose your working session. You will find all your sessions in ", ("MADAME/Downloads/", "rgb(255,255,0)"),"\n\n1 - Create new session\n2 - Continue with existing session\n\n--- If you want to close MADAME digit: ", ("exit", "rgb(255,0,255)")," ---", style = None, justify="left"), border_style= "rgb(255,0,255)", padding= (0,1))
        rich_print(box)

        while True:
            module_choice = input("  >> Enter your option: ")
            if module_choice.isnumeric():
                module_choice = int(module_choice)
                if module_choice not in (1, 2):
                    print("Error, enter a valid choice!\n")
                    continue
                break
            else:
                if module_choice.lower() == "exit":
                    print(Color.BOLD + Color.PURPLE + "\nGood bye, see you soon!\n" + Color.END)
                    logger = LoggerManager.log(user_session)
                    logger.debug(f"[EXIT]\n")
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

    box = Panel(Text.assemble("Digit the folder name, it will be created in ", ("MADAME/Downloads/", "rgb(255,255,0)"), ". MADAME will work in your new session folder.\n\n--- If you want to go back digit: ", ("back", "rgb(255,0,255)")," ---", style = None, justify="left"), title=Text.assemble((" ◊", "rgb(0,255,0)"), " CREATE NEW SESSION ", ("◊ ", "rgb(0,255,0)")), border_style= "rgb(255,0,255)", padding= (0,1))
    rich_print(box)
    
    user_session = ''
    while user_session.strip() == '': 
        user_session = str(input("\n  >> Digit the folder name: "))
    
    if user_session.lower() in ("back"):
        return

    while os.path.isdir(os.path.join("Downloads", user_session)):
        print("\n Error: " + Color.BOLD + Color.YELLOW + f"{user_session}" + Color.END + " folder already exists.")
        user_session = ''
        while user_session.strip() == '': 
            user_session = str(input("  >> Please digit a different name: ")) 
            if user_session.lower() in ("back"):
                return


    Utilities.createDirectory(os.path.join("Downloads", user_session))
    print("\n Your new folder was succesfully created: MADAME/Downloads/" + Color.BOLD + Color.YELLOW + f"{user_session}" + Color.END + "")
    
    logger = LoggerManager.log(user_session)
    logger.debug(f"[MADAME INITIALIZED]")
    logger = LoggerManager.log(user_session)
    logger.debug(f"[USER-SESSION-CREATED]: MADAME/Downloads/{user_session}")

    input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue")

    menu(user_session)


# EXISTING FOLDER

def existing_session():
    Utilities.clear()
    madame_logo()

    box = Panel(Text.assemble("Which existing session do you want to select?\n\n--- If you want to go back digit: ", ("back", "rgb(255,0,255)")," ---", style = None, justify="left"), title=Text.assemble((" ◊", "rgb(0,255,0)"), " CONTINUE WITH EXISTING SESSION ", ("◊ ", "rgb(0,255,0)")), border_style= "rgb(255,0,255)", padding= (0,1))
    rich_print(box)
    
    user_session = ''
    while user_session.strip() == '': # preventing empty inputs
        user_session = str(input("  >> Digit the folder name (case sensitive): "))
        if user_session.lower() in ("back"):
            return

    while not os.path.isdir(os.path.join("Downloads", user_session)):
        print("\n Error: there is no folder named " + Color.BOLD + Color.YELLOW + f"{user_session}" + Color.END)
        print(" Here's your current sessions:\n")

        madame_tree = Tree("MADAME")
        downloads_branch = madame_tree.add("Downloads")

        dirs_branches = [d for d in os.listdir("Downloads") if os.path.isdir(os.path.join("Downloads", d)) and not d.startswith(".")]
        for dir in dirs_branches:
            downloads_branch.add(dir)

        rich_print(madame_tree)

        user_session = ''
        while user_session.strip() == '': # preventing empty inputs
            user_session = str(input("\n  >> Digit the folder name (case sensitive): ")) 
            if user_session.lower() in ("back"):
                return
    logger = LoggerManager.log(user_session)
    logger.debug(f"[MADAME INITIALIZED]")
    logger = LoggerManager.log(user_session)
    logger.debug(f"[PRE-EXISTING-USER-SESSION-CHOSEN]: MADAME/Downloads/{user_session}")
    menu(user_session)

def menu(user_session):

    while True:
        Utilities.clear()
        madame_logo()

        box = Panel(Text.assemble("Which module do you want to use?\n\n1 - Metadata retrieval module: metadata search and download\n2 - Publication retrieval module: metadata- and data- associated publications download\n3 - Report generation module: explore metadata and publication retrieval outputs\n4 - Data retrieval module: metadata-associated data download\n\n>>> Your current session is ", (f"{user_session}", "rgb(255,255,0)"), " <<<\n\n--- If you want to change session digit: ", ("change", "rgb(255,0,255)")," ---\n--- If you want to close MADAME digit: ", ("exit", "rgb(255,0,255)")," ---", style = None, justify="left"), title=Text.assemble((" ◊", "rgb(0,255,0)"), " MAIN MENU ", ("◊ ", "rgb(0,255,0)")), border_style= "rgb(255,0,255)", padding= (0,1))
        rich_print(box)

        while True:
            module_choice = input("  >> Enter your option: ")
            if module_choice.isnumeric():
                module_choice = int(module_choice)
                if module_choice not in (1, 2, 3, 4):
                    print("Error, enter a valid choice!\n")
                    continue
                break
            else:
                if module_choice.lower() == "exit":
                    print(Color.BOLD + Color.PURPLE + "\nGood bye, see you soon!\n" + Color.END)
                    logger = LoggerManager.log(user_session)
                    logger.debug(f"[EXIT]\n")
                    exit()
                elif module_choice.lower() in "change":
                    main()
                else:
                    print("Wrong input, expected a numeric input, <change> or <exit> (without <>). Try again.\n") 
        
        Utilities.clear()

        if module_choice == 1: 
            logger = LoggerManager.log(user_session)
            logger.debug(f"[METADATA MODULE - INITIALIZED]")
            metadata_retrieval(user_session)

        if module_choice == 2:
            publications_retrieval(user_session)

        if module_choice == 3:
            logger = logger = LoggerManager.log(user_session)
            logger.debug(f"[REPORT MODULE - INITIALIZED]")
            report_generation(user_session)

        if module_choice == 4:
            logger = logger = LoggerManager.log(user_session)
            logger.debug(f"[DATA MODULE - INITIALIZED]") 
            data_retrieval(user_session)



def madame_logo():

    custom_theme = Theme({
        "green": "rgb(0,255,0)",
        "white": "rgb(255,255,255)",
        "purple": "rgb(255,0,255)"})

    c = Console(theme=custom_theme)
    c.print("\n                                                           ##############\n                                                       #####################\n                                                    ##########################\n                                                  #############################         ╭─────── [green]Welcome to MADAME[/green] ───────╮\n                                                 ###############################        │     [green]◊[/green] MetADAta MicrobiomE [green]◊[/green]     │\n                                           ####  ###############################        │                                 │\n                                          ######################################        │ [i]Designed to automate the process[/i]│\n                                         #######################################        │  [i]of data and metadata retrieval[/i] │\n                                         ######################################(        │                                 │\n                                         ########################################       ╰────────────────▼────────────────╯\n##     ##     ###     #######       ###  ###[green]##[/green]#####[green]##[/green]##[green]########[/green]##################\n###   ###    ## ##    ##    ##     ## ##  ##[green]###[/green]###[green]###[/green]##[green]##[/green]##########################          ╭─ [green]Biome Research Team[/green] ─╮\n#### ####   ##   ##   ##     ##   ##   ##  #[green]####[/green]#[green]####[/green]##[green]##[/green]########################            │   --- click me! ---   │\n## ### ##  ##     ##  ##     ##  ##     ##  [green]##[/green]#[green]###[/green]#[green]##[/green]##[green]######[/green]###################)            │ [white][link=https://github.com/Biome-team]:computer: GitHub[/link][/white]             │\n##     ##  #########  ##     ##  #########  [green]##[/green]#####[green]##[/green]##[green]##[/green]######################)             │ [white][link=https://biome-research-team.mailchimpsites.com/]:dna: Website[/link][/white]            │\n##     ##  ##     ##  ##    ##   ##     ##  [green]##     ##  ##[/green]######################              │ [white][link=https://www.linkedin.com/company/biome-research-team/]:briefcase: Linkedin[/link][/white]           │\n##     ##  ##     ##  #######    ##     ##  [green]##     ##  ########[/green]#######**######               ╰───────────────────────╯\n                                                     ################     ***\n                                                   #################\n", style = "purple")


if __name__ == "__main__":
    main()