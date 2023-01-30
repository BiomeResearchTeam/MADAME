import os
import subprocess
from Project import Project
#from rich.progress import track


class SequencesDownload:

    def __init__(self, name):
        self.name = name

    
    def runDownloadData(self, user_session, listOfProjectIDs, file_type):
    # Accepted file_types: {submitted,fastq,sra}
    # It needs enaBrowserTools scripts already installed: 
    # https://github.com/enasequence/enaBrowserTools#installing-and-running-the-scripts

    # Check file_type availability (not every project has both sra and fastq files available)
        
        #for projectID in track(listOfProjectIDs, description="Downloading..."): ###does not work with stdout and stderr regularlyvprinted
        for projectID in listOfProjectIDs:
            if Project.getAvailableRuns(user_session, projectID, file_type):
                print(f'Downloading {projectID}, project {listOfProjectIDs.index(projectID)+1} out of {len(listOfProjectIDs)}')
                self.enaBrowserTools(user_session, projectID, file_type)
            else:
                print(f"ERROR: No available '{file_type}' files for this project.")


    def enaBrowserTools(self, user_session, projectID, file_type):
        # Accepted file_types: {submitted,fastq,sra}

        path = os.path.join("Downloads", user_session, projectID)

        command = f'enaGroupGet -f {file_type} {projectID} -d {path}'
        subprocess.check_call(command, shell=True, stdout=1, stderr=2)    

        ####### da testare con -d path
        
        # Rename folder accordingly to file_type, only if it exists.
        # If it doesn't, an error message is printed.
        
        if os.path.isdir(os.path.join(path, projectID)):

            if file_type == 'submitted':
                file_type = Project.getSubmittedFormat(projectID)

            os.rename(os.path.join(path, projectID), os.path.join(path, f'{projectID}_{file_type}_files'))
        
        else:
            print("Something went wrong with your download.\nTry again or change file_type.")


SequencesDownload = SequencesDownload("SequencesDownload")




