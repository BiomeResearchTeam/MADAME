import requests as rq
import os
import sys
import xml.etree.ElementTree as ET
import pandas as pd
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

        for projectID in listOfProjectIDs:
            if self.getProjectAvailability(projectID) == True:
                listOfAvailableProjects.append(projectID)

        
        print("\nThere are:", Color.BOLD + Color.GREEN + str(len(listOfAvailableProjects)), 
        "out of", str(len(listOfProjectIDs)) + Color.END ,"available projects") #sara

        print("Available projects: ", ', '.join(listOfAvailableProjects), "\n")



        return listOfAvailableProjects


    def getProjectBytes(self, projectID, file_type, metadata_file = None, user_session = None):
        # file_type can only be 'sra' or 'fastq'.
        bytes_column = f'{file_type}_bytes'
        ftp_column = f'{file_type}_ftp'
       
        if metadata_file == None:
            # Read experiments metadata
            metadata_file = (os.path.join("Downloads", user_session, f'{projectID}', f'{projectID}_experiments-metadata.tsv'))
            df = pd.read_csv(metadata_file, sep='\t')

        else: 
            df = metadata_file.loc[metadata_file['study_accession'] == projectID]
        
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

    def getProjectSize(self, user_session, projectID, file_type):
        # Accepted file_types: {submitted,fastq,sra}
        bytes = self.getProjectBytes(user_session, projectID, file_type)
        size = Utilities.bytes_converter(bytes)

        return size

    
    def getAllRuns(self, user_session, projectID):

        metadata_file = (os.path.join("Downloads", user_session, projectID, f'{projectID}_experiments-metadata.tsv'))
        df = pd.read_csv(metadata_file, sep='\t')
        df1 = df['run_accession'].value_counts().to_frame(name = 'value_counts').reset_index()
        all_runs = df1['index'].to_list()

        return all_runs

    def getAvailableRuns(self, user_session, projectID, file_type): 
        # Accepted file_types: {submitted,fastq,sra}
        metadata_file = (os.path.join("Downloads", user_session, projectID, f'{projectID}_experiments-metadata.tsv')) 
        df = pd.read_csv(metadata_file, sep='\t') 
        df1 = df[df[f'{file_type}_bytes'].notna()]
        df2 = df1.groupby([f'{file_type}_ftp',f'{file_type}_bytes','run_accession'])[f'{file_type}_bytes'].count().to_frame(name = 'count').reset_index()
        available_runs = df2['run_accession'].to_list()

        return available_runs

    def getUnavailableRuns(self, user_session,  projectID, file_type):
        # Accepted file_types: {submitted,fastq,sra}
        all_runs = self.getAllRuns(user_session, projectID)
        available_runs = self.getAvailableRuns(user_session, projectID, file_type)
        subtraction = set(all_runs) - set(available_runs)
        unavailable_runs = list(subtraction)

        return unavailable_runs

    def getSubmittedFormat(self, user_session,  projectID):
        metadata_file = os.path.join("Downloads", user_session, projectID, f'{projectID}_experiments-metadata.tsv')
        df = pd.read_csv(metadata_file, sep='\t')
        df1 = df['submitted_format'].value_counts().to_frame(name = 'value_counts').reset_index()
        submitted_format = df1['index'].tolist()
        # If there's multiple submitted formats, output will be the list 
        # If not, output will be the only submitted format 
        if len(submitted_format) == 1:
            submitted_format = submitted_format[0]
            return submitted_format
        elif len(submitted_format) == 0:
            return None
        else:
            return submitted_format


        

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

