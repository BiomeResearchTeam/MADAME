import os
import subprocess
import shutil 
from Project import Project
from Utilities import Utilities, Color, LoggerManager
from rich.console import Console
from rich import print as rich_print
from rich.panel import Panel
from rich.text import Text
import pandas as pd

import concurrent.futures

import time


class SequencesDownload:

    def __init__(self, name):
        self.name = name

    
    def runDownloadData(self, EnaBT_path, user_session, e_df, file_type):
    # Accepted file_types: {submitted,fastq,sra}
    # It needs enaBrowserTools scripts already installed: 
    # https://github.com/enasequence/enaBrowserTools#installing-and-running-the-scripts

        # Get Project IDs from the merged experiments dataframe
        listOfProjectIDs = e_df['study_accession'].unique().tolist()
        umbrella_projects = []
        user_choice = False

        # Check if there's umbrella projects in merged experiment metadata
        if 'umbrella_project' in e_df.columns:
            
            # List of all umbrella projects in e_df, filtered to remove empty strings
            umbrella_projects = list(filter(None, e_df['umbrella_project'].unique().tolist()))
            # List of all component projects in e_df
            component_projects = e_df.loc[e_df['umbrella_project'] != '', 'study_accession'].unique().tolist()
            # List of not umbrella and not component projects
            listOfProjectIDs = [x for x in listOfProjectIDs if x not in component_projects]
            # List of umbrella + not umbrella projects, without all the component projects
            listOfProjectIDs_full = listOfProjectIDs + umbrella_projects
            
            # logger
            logger = LoggerManager.log(user_session)
            logger.debug(f"[FOUND-UMBRELLA-PROJECTS]: {umbrella_projects}")


            # Print warning to console
            rich_print(f"\n[yellow]WARNING[/yellow] - {user_session}_merged_experiments-metadata.tsv contains [rgb(0,255,0)]{len(listOfProjectIDs_full)}[/rgb(0,255,0)] projects, but [rgb(0,255,0)]{len(umbrella_projects)}[/rgb(0,255,0)] of them are [yellow]UMBRELLA projects[/yellow]:")

            # Print details about each umbrella (read experiment metadata online).
            # → Project IDs are clickable

            for projectID in umbrella_projects:

                components = e_df.loc[e_df['umbrella_project'] == f'{projectID}', 'study_accession'].unique().tolist()
                
                rich_print(f"[yellow]☂[/yellow] [link=https://www.ebi.ac.uk/ena/browser/view/{projectID}]{projectID}[/link] → [rgb(0,255,0)]{len(components)}[/rgb(0,255,0)] component projects")

                # logger
                logger = LoggerManager.log(user_session)
                logger.debug(f"[UMBRELLA-PROJECT]: {projectID} → {len(components)} component projects")

            # Print info box and let the user decide how to proceed
            print()
            console = Console()
            box = console.print(Panel(("Instead of holding data, umbrella projects group together multiple component projects that are part of the same research motivation or collaboration.\n→ Each umbrella can contain [yellow]a few to thousands[/yellow] of other projects, and this [yellow]can significantly prolong[/yellow] the data download.\nMore info on [link=https://ena-docs.readthedocs.io/en/latest/retrieval/ena-project.html]ENA's documentation[/link]."), title=(":umbrella: Umbrella Projects - Info Box"), border_style= "rgb(255,255,0)", padding= (0,1), title_align="left"))

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
                listOfProjectIDs = listOfProjectIDs

                # logger
                logger = LoggerManager.log(user_session)
                logger.debug(f"[OPTION-1]: - EXCLUDE UMBRELLA PROJECTS")

            # Proceed including umbrella projects  
            if user_choice == 2:            

                # logger
                logger = LoggerManager.log(user_session)
                logger.debug(f"[OPTION-2]: - INCLUDE UMBRELLA PROJECTS")

                listOfProjectIDs = listOfProjectIDs_full   


        dictOfAvailableProjectIDs = {}
        not_available = []
        bytes_total = 0

        # Spinner animation while checking projects and calculating size
        console = Console()
        with console.status("Checking available runs and total file size...") as status:

            size_to_print = []

            for projectID in listOfProjectIDs:

                # Select the sub-dataframe for each project
                if projectID in umbrella_projects:
                    project_df = e_df.loc[e_df['umbrella_project'] == projectID]
                else:
                    project_df = e_df.loc[e_df['study_accession'] == projectID]

                # Check for available runs in the selected format
                if projectID in umbrella_projects:
                    available_runs = Project.getAvailableRuns(projectID, project_df, file_type, umbrella = True)
                else:
                    available_runs = Project.getAvailableRuns(projectID, project_df, file_type)

                # If the project has available runs, append projectID and the runs to a dictionary.
                # Then, calculate project size and sum with total
                if available_runs:
                    dictOfAvailableProjectIDs[projectID] = available_runs
                    
                    if projectID in umbrella_projects:
                        bytes = Project.getProjectBytes(projectID, e_df, file_type, umbrella = True)
                        size_to_print.append(f"[yellow]☂[/yellow] [link=https://www.ebi.ac.uk/ena/browser/view/{projectID}]{projectID}[/link] → {Utilities.bytes_converter(bytes)}")
                    else:
                        bytes = Project.getProjectBytes(projectID, e_df, file_type)
                        size_to_print.append(f"[link=https://www.ebi.ac.uk/ena/browser/view/{projectID}]{projectID}[/link] → {Utilities.bytes_converter(bytes)}")

                    bytes_total += bytes
                    
                # Else, append projectID to not_available list.
                else:
                    not_available.append(projectID)

        # Print to screen project name and project size
        print()
        rich_print("[b rgb(255,0,255)]Projects size summary[/b rgb(255,0,255)]")
        for line in size_to_print:
            rich_print(line)

        # No available runs across all projects for chosen file_type 
        if bytes_total == 0:
            print()
            print(Color.BOLD + Color.RED + f"NO AVAILABLE {file_type} format files." + Color.END + " Try selecting a different file format")
            logger = LoggerManager.log(user_session)
            logger.debug(f"NO AVAILABLE {file_type} format files")
            input("\nPress " + Color.BOLD + Color.PURPLE + "ENTER" + Color.END + " to return to the main menu ")
            return 

        # Calculate free space on disk and % of total file size on free space
        free, percentage = self.check_available_disk_space(bytes_total)

        # No available free space on disk
        if free == 0:
            print(Color.BOLD + Color.RED + f"\nERROR" + Color.END + ": no available free space on disk")
            logger.debug("[ERROR]: no available free space on disk")
            input("\nPress " + Color.BOLD + Color.PURPLE + "ENTER" + Color.END + " to return to the main menu ")
            return 
        
        # Print message for not available projects, if there's any
        if not_available:
            # The loop prints each accession one next to each other, they can be clicked and the last item (else) is printed differently, without the comma. If it's a list of projects comprehensive of umbrella projects, they are printed next to the "☂" character.
            print()
            rich_print(f"[b red]No available[/b red] {file_type} format files for projectIDs → ", end="")
            for accession in not_available[:-1]:
                if accession in umbrella_projects:
                    rich_print(f"[link=https://www.ebi.ac.uk/ena/browser/view/{accession}][yellow]☂[/yellow] {accession}[/link], ", end="")
                else:
                    rich_print(f"[link=https://www.ebi.ac.uk/ena/browser/view/{accession}]{accession}[/link], ", end="")
            else:
                if not_available[-1] in umbrella_projects:
                    rich_print(f"[link=https://www.ebi.ac.uk/ena/browser/view/{not_available[-1]}][yellow]☂[/yellow] {not_available[-1]}[/link].\n")
                else:
                    rich_print(f"[link=https://www.ebi.ac.uk/ena/browser/view/{not_available[-1]}]{not_available[-1]}[/link].\n")
            
            logger.debug(f"[WARNING]: no available {file_type} format files for projectIDs: {not_available}")

        # Setting color for printing the preview
        if percentage < 50:
            color = "[green]"
        elif percentage >= 50 and percentage < 80:
            color = "[yellow]"
        elif percentage >= 80:
            color = "[red]"

        # # For printing very little percentages:
        # if percentage < 1:
        #     percentage = "<1"
        download_preview = f"[white]Available/Total Projects ({file_type}) = {len(dictOfAvailableProjectIDs)}/{len(listOfProjectIDs)}" + f"\nTotal file size = {Utilities.bytes_converter(bytes_total)}" + f"\nYou are going to occupy {color}{percentage}% of free disk space"
        title = Panel.fit(download_preview, style = "magenta", title=Text.assemble((" ◊", "rgb(0,255,0)"), " DOWNLOAD PREVIEW ", ("◊ ", "rgb(0,255,0)")), border_style= "rgb(255,0,255)")
        print()
        logger = LoggerManager.log(user_session)
        logger.debug(f"Total file size = {Utilities.bytes_converter(bytes_total)}. You are going to occupy {percentage}% of free disk space")
        rich_print(title)

        # Percentage higher than 1%, user has to digit yes to continue with download
        if percentage >= 0 and percentage <= 95:
            print(Color.YELLOW + Color.BOLD + "\nWARNING" + Color.END + ": you're gonna occupy" + Color.YELLOW + Color.BOLD + f" {percentage} % " + Color.END + "of your free disk space")
            logger.debug(f"[WARNING]: you're gonna occupy {percentage} % of your free disk space")
            while True: 
                user_input = ''
                while user_input.strip() == '': 
                    user_input = str(input("  >> Digit " + Color.BOLD + Color.PURPLE + "yes" + Color.END + " to start downloading, or " + Color.BOLD + Color.PURPLE + "back" + Color.END + " to go back: "))
                    
                    if user_input.lower() in ("yes"):
                        logger.debug("DOWNLOAD INITIALIZED")
                        t0 = time.time()

                        failed_runs = {}

                        for project, runIDs in dictOfAvailableProjectIDs.items():

                            # If the project is an umbrella
                            if project in umbrella_projects: 

                                components = e_df.loc[e_df['umbrella_project'] == f'{projectID}', 'study_accession'].unique().tolist()

                                component_project_files = os.path.join("Downloads", user_session, project, 'component_project_files')
                                Utilities.createDirectory(component_project_files)

                                unavailable_components = []
                                for component in components:
                                    component_df = project_df.loc[project_df['study_accession'] == component]
                                    runIDs = Project.getAvailableRuns(component, component_df, file_type)
                                    if not runIDs:
                                        unavailable_components.append(component)
                                        # skip to next component
                                        continue

                                    path = os.path.join(component_project_files, f'{component}_{file_type}_files')
                                    Utilities.createDirectory(path)

                                    failed = []

                                    with concurrent.futures.ThreadPoolExecutor() as executor:
                                        futures = {executor.submit(self.enaBT, user_session, path, EnaBT_path, runID, file_type): runID for runID in runIDs}
                                        print(futures)

                                        for future in concurrent.futures.as_completed(futures):
                                            runID = futures[future]
                                            try:
                                                success = future.result()
                                                print(success)
                                                if not success:
                                                    print(f"Failed to process runID {runID}. Retrying...")
                                                    retry_success = self.retry_enaBT(user_session, path, EnaBT_path, runID, file_type)
                                                    if not retry_success:
                                                        print(f"Failed to retry runID {runID}")
                                                        failed.append(runID)
                                            except Exception as e:
                                                print(f"Error processing run {runID}: {e}")
                                                logger.debug(f"Error processing run {runID}: {e}")

                                    if failed:
                                        failed_runs[component] = failed

                                # Print message for not available component projects, if there's any
                                if unavailable_components:
                                    rich_print(f"\n[b red]No available[/b red] {file_type} format files for these [yellow]☂[/yellow] {project}'s components: {unavailable_components}")
                                    # logger
                                    logger.debug(f"[WARNING]: no available {file_type} format files for these ☂ {project}'s components: {unavailable_components}")

                            # If the project is not an umbrella
                            else: 
                                path = os.path.join("Downloads", user_session, project, f'{project}_{file_type}_files')
                                Utilities.createDirectory(path)

                                failed = []

                                with concurrent.futures.ThreadPoolExecutor() as executor:
                                    futures = {executor.submit(self.enaBT, user_session, path, EnaBT_path, runID, file_type): runID for runID in runIDs}
                                    #print(futures)

                                    for future in concurrent.futures.as_completed(futures):
                                        runID = futures[future]
                                        try:
                                            success = future.result()
                                            print(success)
                                            if not success:
                                                print(f"Failed to process runID {runID}. Retrying...")
                                                retry_success = self.retry_enaBT(user_session, path, EnaBT_path, runID, file_type)
                                                if not retry_success:
                                                    print(f"Failed to retry runID {runID}")
                                                    failed.append(runID)
                                        except Exception as e:
                                            print(f"Error processing run {runID}: {e}")
                                            logger.debug(f"Error processing run {runID}: {e}")

                                if failed:
                                    failed_runs[project] = failed
                        
                        if failed_runs:
                            rich_print(f"\n[b red]WARNING[/b red]! Some runs were not downloaded. You can find  a detailed list in the log file.")
                            logger.debug(f'WARNING! List of runs that were not downloaded: {failed_runs}')
                        else:
                            print(Color.BOLD + Color.GREEN + "SUCCESS! All runs were downloaded\n" + Color.END)
                            logger.debug('SUCCESS! All runs were downloaded')


                        #-------------------------#

                        # results = []
                        # with concurrent.futures.ThreadPoolExecutor() as executor:
                        #     while max_retries > 0:
                        #         future_to_runID = {
                        #             executor.submit(self.enaBT, user_session, path, EnaBT_path, runID, file_type): runID
                        #             for runID, file_type in runIDs
                        #         }

                        #         for future in concurrent.futures.as_completed(future_to_runID):
                        #             runID = future_to_runID[future]
                        #             try:
                        #                 result = future.result()
                        #                 if result[1] is not None:
                        #                     print(f"Successfully processed runID: {runID}")
                        #                     # Aggiungi il risultato alla lista dei risultati validi
                        #                     results.append(result)
                        #                 else:
                        #                     print(f"Failed to process runID {runID}: {result[1]}")
                        #                     # Riduci il numero di tentativi rimanenti
                        #                     max_retries -= 1
                        #                     if max_retries > 0:
                        #                         print(f"Retrying runID {runID} after 5 seconds...")
                        #                         time.sleep(5)
                        #                         # Ritenta il download
                        #                         future_retry = executor.submit(self.enaBT, user_session, path, EnaBT_path, runID, file_type)
                        #                         future_to_runID[future_retry] = runID
                        #             except Exception as e:
                        #                 print(f"Error processing runID {runID}: {e}")




                            # with concurrent.futures.ThreadPoolExecutor() as executor:
                            #     executor.map(lambda runID: self.enaBT(user_session, path, EnaBT_path, runID, file_type), runIDs)

                                #download = self.enaBT(user_session, path, EnaBT_path, run, file_type)

                                # if download == 0:
                                #     print(Color.RED + "\nSomething went wrong with your download (internet connection, or ENA server overload)." + Color.END) # messaggio da modificare ? 
                                #     logger.debug("[ERROR]: Something went wrong with your download (internet connection, or ENA server overload)")
                                #     input("\nPress " + Color.BOLD + Color.PURPLE + "ENTER" + Color.END + " to return to the main menu")
                                #     return 

                        #------------------------------#

                        print('time (s):', time.time() - t0)  
                    
                        break
                    
                    elif user_input.lower() in ("back"):
                        return 
                    
                    else:
                        print("Error, enter a valid choice!\n")


        # Unsafe percentage, cannot proceed with the download
        elif percentage > 95:
            print(Color.RED + Color.BOLD + f"\nERROR: the selected runs would occupy more than 95% of your free disk space" + Color.END)
            logger.debug("[ERROR]: the selected runs would occupy more than 95 percent of your free disk space. Download not allowed.")
            input("\nPress " + Color.BOLD + Color.PURPLE + "ENTER" + Color.END + " to return to the main menu ")
            return 

        # Final message
        print("\nSEQUENCES DOWNLOAD completed!")
        print(f"Now you can find the {file_type} files divided by projects. Example path: MADAME/Downloads/projectID/" + Color.BOLD + Color.YELLOW + f"projectID_{file_type}_files" + Color.END) 
        logger.debug("SEQUENCES DOWNLOAD completed!")
        logger.debug(f"Now you can find the {file_type} files divided by projects. Example path: MADAME/Downloads/projectID/projectID_{file_type}_files")
        input("\nPress " + Color.BOLD + Color.PURPLE + "ENTER" + Color.END + " to return to the main menu ")
        return 

    
    def enaBT(self, user_session, path, EnaBT_path, runID, file_type):
        
        # Give execution permission to enaBT
        os.chmod(EnaBT_path, 0o755)

        command = f'{EnaBT_path} -f {file_type} {runID} -d "{path}"' 
        logger = LoggerManager.log(user_session)
        logger.debug(f"{command}")
        try:
            subprocess.run(command, check=True, shell=True, stdout=1, stderr=2) 
            return True  
        except subprocess.CalledProcessError as error:
            return False


    def retry_enaBT(self, user_session, path, EnaBT_path, runID, file_type, max_retries=3, retry_interval=5):
        max_retries = 3
        for _ in range(max_retries):
            time.sleep(5)
            success = self.enaBT(user_session, path, EnaBT_path, runID, file_type)
            if success:
                return True
        return False 


    def check_available_disk_space(self, bytes_total):
           
        total, used, free = shutil.disk_usage("/")
   
        try:
            return free, round((bytes_total / free) * 100)
        
        except ZeroDivisionError:
            return 0, 0

SequencesDownload = SequencesDownload("SequencesDownload")