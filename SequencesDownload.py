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
                        self.enaBT(path, runID, file_type)
                        # print success message only if the loop didn't finish with an error (how???)

                else:
                    print(f"No available {file_type} format files for {projectID}. Skipping") # messaggio da modificare


    def enaBT(self, path, runID, file_type):
        # Accepted file_types: {submitted,fastq,sra}

        command = f'enaDataGet -f {file_type} {runID} -d {path}'
        try:
            subprocess.check_call(command, shell=True, stdout=1, stderr=2)
            
        except subprocess.CalledProcessError as error:
            # riprovare il comando di subprocess con lo stesso runID tot volte, e se dà sempre errore solo allora printare l'errore (how???)
            print("Something went wrong with the download (internet connection, or ENA server overload). Please try again later.") # messaggio da modificare  
            input("\nPress " + Color.BOLD + Color.PURPLE + "ENTER" + Color.END + " to return to the main menu ")


SequencesDownload = SequencesDownload("SequencesDownload")


e_df = pd.read_csv("/home/gsoletta/MADAME/Downloads/cutaneous_microbiome/cutaneous_microbiome_merged_experiments-metadata.tsv", delimiter='\t')
SequencesDownload.runDownloadData("cutaneous_microbiome", e_df, "fastq")