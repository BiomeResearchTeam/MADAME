import requests as rq
import os
import sys
import xml.etree.ElementTree as ET
import pandas as pd
from rich.progress import track
from Utilities import Utilities, Color

class Project:
    def __init__(self, projectID):
        self.ProjectID = projectID
    
    def getProjectID(self):
        return self.ProjectID

    def getProjectAvailability(self, projectID):
    # Check Project's availability based on its metadata availability
        url = f"https://www.ebi.ac.uk/ena/portal/api/filereport?accession={projectID}&result=read_run&fields=study_accession,sample_accession,experiment_accession,run_accession,tax_id,scientific_name,fastq_ftp,submitted_ftp,sra_ftp&format=tsv&download=true&limit=0"
        response = rq.head(url, allow_redirects=True)

        # If metadata exists, Content-Lenght in header is present:
        # this means the project contains uploaded data, so that is available.
        if 'Content-Length' in response.headers:
            self.ProjectAvailability = True
        else:
            self.ProjectAvailability = False

        return self.ProjectAvailability


    def getAvailableProjects(self, listOfProjectIDs):
    # Input is the full list of project IDs, output is the list of the available projects.
    # This list is needed for all steps after getting a listOfProjectIDs.

        listOfAvailableProjects = []

        for projectID in track(listOfProjectIDs, description= "Checking for availability..."):
            if self.getProjectAvailability(projectID) == True:
                listOfAvailableProjects.append(projectID)

        
        print("\nThere are:", Color.BOLD + Color.GREEN + str(len(listOfAvailableProjects)), 
        "out of", str(len(listOfProjectIDs)) + Color.END ,"available projects") #sara

        print("Available projects: ", ', '.join(listOfAvailableProjects), "\n")



        return listOfAvailableProjects


    def getProjectBytes(self, projectID, e_df, file_type): 
        # file_type can only be 'sra' or 'fastq'.
        bytes_column = f'{file_type}_bytes'
        ftp_column = f'{file_type}_ftp'  
 
        df = e_df.loc[e_df['study_accession'] == projectID]

        # Only read df lines which are not NaN in the bytes_column (so, they are available runs)
        df1 = df[df[bytes_column].notna()]

        # Group by fastq_ftp and then fastq_bytes columns: so if a file is repeated in multiple
        # lines (e.g. multiple samples for the same run), we count it only one time
        df2 = df1.groupby([ftp_column, bytes_column])[bytes_column].count().to_frame(name = 'count').reset_index()

        # If files are single-end, values in fastq_bytes will be integers -> df.sum()
        if df2[bytes_column].dtypes == 'int64':
            bytes = df2[bytes_column].sum()

        elif df2[bytes_column].dtypes == 'float64':
            bytes = df2[bytes_column].sum()
        # If files are paired-end, values in fastq_bytes will be a string, like '716429859;741556367'. 
        # Split the two numbers and add them to each other, before calculating the total of the column. 
        else:
            df3 = df2[bytes_column].apply(lambda x: sum(map(int, x.split(';'))))
            bytes = df3.sum()

        return bytes

    def getProjectSize(self, projectID, e_df, file_type):

        bytes = self.getProjectBytes(projectID, e_df, file_type)
        size = Utilities.bytes_converter(bytes)

        return size

    
    def getAllRuns(self, projectID, e_df):

        df = e_df.loc[e_df['study_accession'] == projectID]
        all_runs = df['run_accession'].unique().tolist()

        return all_runs

    # GET AVAILABLE RUNS FOR A CERTAIN FILE TYPE
    def getAvailableRuns(self, projectID, e_df, file_type): 
        # Accepted file_types: {submitted,fastq,sra}

        df = e_df.loc[e_df['study_accession'] == projectID]
        df1 = df[df[f'{file_type}_bytes'].notna()]
        df2 = df1.groupby([f'{file_type}_ftp',f'{file_type}_bytes','run_accession'])[f'{file_type}_bytes'].count().to_frame(name = 'count').reset_index()
        available_runs = df2['run_accession'].to_list() 

        return available_runs

    # GET UNAVAILABLE RUNS FOR A CERTAIN FILE TYPE
    def getUnavailableRuns(self, projectID, e_df, file_type):
        # Accepted file_types: {submitted,fastq,sra}

        all_runs = self.getAllRuns(projectID, e_df)
        available_runs = self.getAvailableRuns(projectID, e_df, file_type)
        subtraction = set(all_runs) - set(available_runs)
        unavailable_runs = list(subtraction)

        return unavailable_runs

    def getSubmittedFormat(self, projectID, e_df):
        
        df = e_df.loc[e_df['study_accession'] == projectID]
        submitted_format = df['submitted_format'].unique().tolist()

        return submitted_format #list
        

    def getProjectInfo(self, user_session, projectID, field):
        # Utility function for getProjectName, getProjectTitle, getProjectDescription functions.
        
        tree = ET.parse(os.path.join("Downloads", user_session, projectID, f'{projectID}_project-metadata.xml'))
        root = tree.getroot()

        for children in root.iter("PROJECT"):
            child = children.find(field)
            if child is not None:
                value = child.text
            else:
                value = f"ERROR: MISSING FIELD [{field}]"
                sys.exit()

        return value   

    def getProjectName(self, user_session, projectID):
        projectName = self.getProjectInfo(user_session, projectID, "NAME")

        return projectName

    def getProjectTitle(self, user_session, projectID):
        projectTitle = self.getProjectInfo(user_session, projectID, "TITLE")
        
        return projectTitle

    def getProjectDescription(self, user_session,  projectID):
        projectDescription = self.getProjectInfo(user_session, projectID, "DESCRIPTION")
        
        return projectDescription


    def listOfAccessionIDsTSV(self, listOfProjectIDs, user_session): 
        #Creates user_session folder and saves the list of available accession IDs as TSV
        path = (os.path.join("Downloads", user_session))
        Utilities.createDirectory(path)

        listOfAccessionIDs = pd.DataFrame({"accession_ids":listOfProjectIDs})
        listOfAccessionIDs.to_csv(os.path.join(path, '_listOfAccessionIDs.tsv'), sep="\t", index=False)

Project = Project('Project') 
