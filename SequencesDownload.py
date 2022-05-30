import subprocess
import os
from Project import Project
from subprocess import Popen, PIPE


class SequencesDownload:

    def __init__(self, name):
        self.name = name

    
    def runDownloadData(self, listOfProjectIDs, file_type):
    # Accepted file_types: {submitted,fastq,sra}
    # It needs enaBrowserTools scripts already installed: 
    # https://github.com/enasequence/enaBrowserTools#installing-and-running-the-scripts

    # Check file_type availability (not every project has both sra and fastq files available)
        files_availability = Project("files_availability")
        for projectID in listOfProjectIDs:
            if files_availability.getAvailableRuns(projectID, file_type):
                self.enaBrowserTools(projectID, file_type)
            else:
                print(f"ERROR: No available '{file_type}' files for this project.")


    def enaBrowserTools(self, projectID, file_type):
        # Accepted file_types: {submitted,fastq,sra}
        
        subprocess.run(f'enaGroupGet -f {file_type} {projectID} -d {projectID}', shell=True, capture_output=True, text=True)


        # Rename folder accordingly to file_type, only if it exists.
        # If it doesn't, an error message is printed.
        if os.path.isdir(os.path.join(projectID, projectID)):

            if file_type == 'submitted':
                check_submitted_type = Project("check_submitted_type")
                file_type = check_submitted_type.getSubmittedFormat(projectID)

                os.rename(os.path.join(projectID, projectID), os.path.join(projectID, f'{projectID}_{file_type}_files'))
        else:
            print("Something went wrong with your download.\nTry again or change file_type.")



listOfProjectIDs = ['PRJEB45401']
os.chdir("/mnt/c/Users/conog/Desktop/MADAME")
download_prova = SequencesDownload("prova")
download_prova.runDownloadData(listOfProjectIDs, 'submitted')
