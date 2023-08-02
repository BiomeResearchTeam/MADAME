import os
import subprocess
import shutil 
from Project import Project
from Utilities import Utilities, Color
from rich.console import Console
from rich import print as rich_print
from rich.panel import Panel
from rich.text import Text

class SequencesDownload:

    def __init__(self, name):
        self.name = name

    
    def runDownloadData(self, EnaBT_path, user_session, e_df, file_type):
    # Accepted file_types: {submitted,fastq,sra}
    # It needs enaBrowserTools scripts already installed: 
    # https://github.com/enasequence/enaBrowserTools#installing-and-running-the-scripts
        
        # Get Project IDs from a merged experiments dataframe
        listOfProjectIDs = e_df['study_accession'].unique().tolist()

        dictOfAvailableProjectIDs = {}
        not_available = []
        bytes_total = 0

        # Spinner animation while checking projects and calculating size
        console = Console()
        with console.status("Checking available runs and total file size...") as status:

            for projectID in listOfProjectIDs:
                # Select the sub-dataframe for each project
                project_df = e_df.loc[e_df['study_accession'] == projectID]
                # Check for available runs in the selected format
                available_runs = Project.getAvailableRuns(projectID, project_df, file_type)
                
                # If the project has available runs, append projectID and the runs to a dictionary.
                # Then, calculate project size and sum with total
                if available_runs:
                    dictOfAvailableProjectIDs[projectID] = available_runs
                    bytes = Project.getProjectBytes(projectID, e_df, file_type)
                    bytes_total += bytes
                # Else, append projectID to not_available list.
                else:
                    not_available.append(projectID)

        # No available runs across all projects for chosen file_type 
        if bytes_total == 0:
            print(Color.BOLD + Color.RED + f"NO AVAILABLE {file_type} format files." + Color.END + " Try selecting a different file format") 
            input("\nPress " + Color.BOLD + Color.PURPLE + "ENTER" + Color.END + " to return to the main menu ")
            return 

        # Calculate free space on disk and % of total file size on free space
        free, percentage = self.check_available_disk_space(bytes_total)

        # No available free space on disk
        if free == 0:
            print(Color.BOLD + Color.RED + f"\nERROR" + Color.END + ": no available free space on disk") 
            input("\nPress " + Color.BOLD + Color.PURPLE + "ENTER" + Color.END + " to return to the main menu ")
            return 
        
        # Print message for not available projects, if there's any
        if not_available:
            print(Color.BOLD + Color.RED + "\nNo available " + Color.END + f"{file_type} format files for projectIDs: {not_available}")

        # Setting color for printing the preview
        if percentage < 50:
            color = "[green]"
        elif percentage >= 50 and percentage < 80:
            color = "[yellow]"
        elif percentage >= 80:
            color = "[red]"

        # For printing very little percentages:
        if percentage < 1:
            percentage = "<1"

        download_preview = f"[white]Available/Total Projects ({file_type}) = {len(dictOfAvailableProjectIDs)}/{len(listOfProjectIDs)}" + f"\nTotal file size = {Utilities.bytes_converter(bytes_total)}" + f"\nYou are going to occupy {color}{percentage}% of free disk space"
        title = Panel.fit(download_preview, style = "magenta", title=Text.assemble((" ◊", "rgb(0,255,0)"), " DOWNLOAD PREVIEW ", ("◊ ", "rgb(0,255,0)")), border_style= "rgb(255,0,255)")
        print()
        rich_print(title)

        # # Safe percentage, just press ENTER to loop through available projects and ids in the dictionary
        # if percentage < 50:
        #     input("\nPress " + Color.BOLD + Color.PURPLE + "ENTER" + Color.END + " to continue with the download")
        #     for project, runs in dictOfAvailableProjectIDs.items():
        #         path = os.path.join("Downloads", user_session, project, f'{project}_{file_type}_files')
        #         Utilities.createDirectory(path)
            
        #         for run in runs:
        #             download = self.enaBT(path, EnaBT_path, run, file_type)

        #             if download == 0:
        #                 print(Color.RED + "\nSomething went wrong with your download (internet connection, or ENA server overload)." + Color.END) # messaggio da modificare ? 
        #                 input("\nPress " + Color.BOLD + Color.PURPLE + "ENTER" + Color.END + " to return to the main menu")
        #                 return 
        
        # Percentage higher than 1%, user has to digit yes to continue with download
        if percentage >= 1 and percentage <= 95:
            print(Color.YELLOW + Color.BOLD + "\nWARNING" + Color.END + ": you're gonna occupy" + Color.YELLOW + Color.BOLD + f" {percentage} % " + Color.END + "of your free disk space.")
            while True: 
                user_input = ''
                while user_input.strip() == '': 
                    user_input = str(input("  >> Digit " + Color.BOLD + Color.PURPLE + "yes" + Color.END + " to start downloading, or " + Color.BOLD + Color.PURPLE + "back" + Color.END + " to go back: "))
                    
                    if user_input.lower() in ("yes"):
                        for project, runs in dictOfAvailableProjectIDs.items():
                            path = os.path.join("Downloads", user_session, project, f'{project}_{file_type}_files')
                            Utilities.createDirectory(path)
                            
                            for run in runs:
                                download = self.enaBT(path, EnaBT_path, run, file_type)

                                if download == 0:
                                    print(Color.RED + "\nSomething went wrong with your download (internet connection, or ENA server overload)." + Color.END) # messaggio da modificare ? 
                                    input("\nPress " + Color.BOLD + Color.PURPLE + "ENTER" + Color.END + " to return to the main menu")
                                    return 
                        break
                    
                    elif user_input.lower() in ("back"):
                        return 
                    
                    else:
                        print("Error, enter a valid choice!\n")


        # Unsafe percentage, cannot proceed with the download
        elif percentage > 95:
            print(Color.RED + Color.BOLD + f"\nERROR: the selected runs would occupy more than 95% of your free disk space." + Color.END)
            input("\nPress " + Color.BOLD + Color.PURPLE + "ENTER" + Color.END + " to return to the main menu ")
            return 

        # Final message
        print("\nSEQUENCES DOWNLOAD completed!")
        print(f"Now you can find the {file_type} files divided by projects. Example path: MADAME/Downloads/projectID/" + Color.BOLD + Color.YELLOW + f"projectID_{file_type}_files" + Color.END) 
        input("\nPress " + Color.BOLD + Color.PURPLE + "ENTER" + Color.END + " to return to the main menu ")
        return 
        
            # if available_runs:
                
            #     # Create main files directory (only if it doesn't exist yet)
            #     path = os.path.join("Downloads", user_session, projectID, f'{projectID}_{file_type}_files')
            #     Utilities.createDirectory(path)


            #     # RICH TRACK NOT COMPATIBLE WITH ENABT STDOUT (the bar is printed again for each new output line on screen)
            #     #for runID in track(available_runs, description=f"Downloading selected runs for {projectID}..."):
            #     for runID in available_runs:
            #         download = self.enaBT(path, EnaBT_path, runID, file_type) #silenziato da sara
            #         #download = self.enaBT_path(path, runID, file_type)

            #         if download == 0:
            #             print(Color.RED + "\nSomething went wrong with your download (internet connection, or ENA server overload)." + Color.END) # messaggio da modificare ? 
            #             input("\nPress " + Color.BOLD + Color.PURPLE + "ENTER" + Color.END + " to return to the main menu ")
            #             return #goes back to data retrievement module
                
            #     #####
            #     # INSERIRE QUI UN CHECK SUI FILE SCARICATI (PUO' SUCCEDERE CHE ALCUNI VENGANO SALTATI)
            #     #####

            #     print("\nSEQUENCES DOWNLOAD completed!")
            #     print(f"Now you can find the {file_type} files divided by projects. Example path: MADAME/Downloads/projectID/" + Color.BOLD + Color.YELLOW + f"projectID_{file_type}_files" + Color.END) # messaggio da modificare ?
            #     input("\nPress " + Color.BOLD + Color.PURPLE + "ENTER" + Color.END + " to return to the main menu ")
            #     return #goes back to data retrievement module - should go back to main menu..

            # else:
            #     print(f"No available {file_type} format files for {projectID}. Skipping") # messaggio da modificare ?


    
    def enaBT(self, path, EnaBT_path, runID, file_type):
        
        command = f'{EnaBT_path} -f {file_type} {runID} -d {path}'
        try:
            subprocess.run(command, check=True, shell=True, stdout=1, stderr=2) 
                    # print(os.getcwd())
                    # subprocess.run([command], check=True, shell=True, stdout=1, stderr=2)
                        
        except subprocess.CalledProcessError as error:
 
            return 0


    def check_available_disk_space(self, bytes_total):
           
        total, used, free = shutil.disk_usage("/")
   
        try:
            return free, round((bytes_total / free) * 100)
        
        except ZeroDivisionError:
            return 0, 0

SequencesDownload = SequencesDownload("SequencesDownload")