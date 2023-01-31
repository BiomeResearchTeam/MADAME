import os
import subprocess
import pandas as pd
from Project import Project
from Utilities import Utilities, Color
#from rich.progress import track

# NEEDS NESTED RICH BAR FOR OVERALL AND PARTIAL DOWNLOAD (example https://github.com/Textualize/rich/discussions/950)

class SequencesDownload:

    def __init__(self, name):
        self.name = name

    
    def runDownloadData(self, user_session, e_df, file_type):
    # Accepted file_types: {submitted,fastq,sra}
    # It needs enaBrowserTools scripts already installed: 
    # https://github.com/enasequence/enaBrowserTools#installing-and-running-the-scripts

    
        listOfProjectIDs = e_df['study_accession'].unique().tolist()
        
        for projectID in listOfProjectIDs:
                # Select the sub-dataframe for each project
                project_df = e_df.loc[e_df['study_accession'] == projectID]
                # Check for available runs in the selected format
                available_runs = Project.getAvailableRuns(projectID, project_df, file_type)
                
                if available_runs:
                  
                    # Create main files directory (only if it doesn't exist yet)
                    path = os.path.join("Downloads", user_session, projectID, f'{projectID}_{file_type}_files')
                    Utilities.createDirectory(path)


                    # RICH TRACK NOT COMPATIBLE WITH ENABT STDOUT (the bar is printed again for each new output line on screen)
                    #for runID in track(available_runs, description=f"Downloading selected runs for {projectID}..."):
                    for runID in available_runs:
                        download = self.enaBT(path, runID, file_type)

                        if download == 0:
                            print(Color.RED + "\nSomething went wrong with your download (internet connection, or ENA server overload)." + Color.END) # messaggio da modificare ? 
                            input("\nPress " + Color.BOLD + Color.PURPLE + "ENTER" + Color.END + " to return to the main menu ")
                            return #goes back to data retrievement module
                    
                    #####
                    # INSERIRE QUI UN CHECK SUI FILE SCARICATI (PUO' SUCCEDERE CHE ALCUNI VENGANO SALTATI)
                    #####

                    print("\nSEQUENCES DOWNLOAD completed!")
                    print(f"Now you can find the {file_type} files divided by projects. Example path: MADAME/Downloads/projectID/" + Color.BOLD + Color.YELLOW + f"projectID_{file_type}_files" + Color.END) # messaggio da modificare ?
                    input("\nPress " + Color.BOLD + Color.PURPLE + "ENTER" + Color.END + " to return to the main menu ")
                    return #goes back to data retrievement module - should go back to main menu..

                else:
                    print(f"No available {file_type} format files for {projectID}. Skipping") # messaggio da modificare ?


    def enaBT(self, path, runID, file_type):
        # Accepted file_types: {submitted,fastq,sra}

        command = f'enaDataGet -f {file_type} {runID} -d {path}'
        try:
            subprocess.run(command, check=True, shell=True, stdout=1, stderr=2)
            
        except subprocess.CalledProcessError as error:
            # spesso ENA rifiuta la connessione, potremmo riprovare il comando di subprocess con lo stesso runID tot volte, e se dà sempre errore solo allora printare l'errore (how???)     
            return 0
            

    def check_files():



        return
SequencesDownload = SequencesDownload("SequencesDownload")