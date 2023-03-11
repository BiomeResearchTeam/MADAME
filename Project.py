import requests as rq
import os
import re
import io
import sys
import xml.etree.ElementTree as ET
import pandas as pd
from rich.progress import track
from Utilities import Utilities, Color
from user_agent import generate_user_agent
from requests.adapters import HTTPAdapter, Retry

class Project:
    def __init__(self, projectID):
        self.ProjectID = projectID
    
    def getProjectID(self):
        return self.ProjectID

    def getAccessionAvailability(self, accessionID):
    # Check the accession ID availability based on its metadata availability

        s = rq.session()
        retries = Retry(total=5,
                        backoff_factor=0.1,
                        status_forcelist=[500, 502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        url = f"https://www.ebi.ac.uk/ena/portal/api/filereport?accession={accessionID}&result=read_run&fields=study_accession,sample_accession,experiment_accession,run_accession,tax_id,scientific_name,fastq_ftp,submitted_ftp,sra_ftp&format=tsv&download=true&limit=0"
        headers = {"User-Agent": generate_user_agent()}
        download = s.head(url, headers=headers, allow_redirects=True)

        # If metadata exists, Content-Lenght in header is present:
        # this means the accession has uploaded data, so it is available.
        if 'Content-Length' in download.headers:
            return True
        else:
            return False


    def getAvailableAccessions(self, user_session, listOfAccessionIDs):
    # Input is the full list of accession IDs, output is the list of the available accessions.
    # This list is needed for all steps after getting a listOfAccessionIDs.

        GENERIC_RANGE_PATTERN = r'^[a-zA-Z0-9]+-[a-zA-Z0-9]+$'
        listOfAvailableAccessions = []


        for accessionID in track(listOfAccessionIDs, description= "Checking for availability..."):
            
            # If it's a range, check the first and last element availability (to exclude out of range mistakes)
            if re.match(GENERIC_RANGE_PATTERN, accessionID):
                range_ids = accessionID.split("-")
                first_id_availability = self.getAccessionAvailability(range_ids[0])
                second_id_availability = self.getAccessionAvailability(range_ids[1])

                if first_id_availability and second_id_availability == False:
                    continue

                elif first_id_availability and second_id_availability == True:
                    # If they are both available, check if they are part of the same project (it is possible they are not)
                    first_id_project = self.getAccessionProject(range_ids[0])
                    second_id_project = self.getAccessionProject(range_ids[1])

                    if first_id_project == second_id_project:
                        listOfAvailableAccessions.append(accessionID)
                    else:
                        print(Color.BOLD + Color.RED + "\nWARNING" + Color.END, f": out of range error. {range_ids[0]} and {range_ids[1]} belong to different projects.\n")
               
                elif first_id_availability != second_id_availability:
                    print(Color.BOLD + Color.RED + "\nWARNING" + Color.END, f": out of range error. Please check if the first or last element of {accessionID} is correct.\n")

            # If it's a single accession, check the accession availability
            else:
                if self.getAccessionAvailability(accessionID) == True:
                    listOfAvailableAccessions.append(accessionID)

        
        print("\nThere are:", Color.BOLD + Color.GREEN + str(len(listOfAvailableAccessions)), 
        "out of", str(len(listOfAccessionIDs)) + Color.END ,"available accessions.")

        print("Available accessions: ", ', '.join(listOfAvailableAccessions), "\n")

        # logger = Utilities.log("Project", user_session)
        # logger.debug(f"[AVAILABLE-ACCESSIONS]: {listOfAvailableAccessions}")

        return listOfAvailableAccessions


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
            df3 = df2[bytes_column].apply(lambda x: sum(int(float(num)) for num in x.split(';'))) #sara
            #df3 = df2[bytes_column].apply(lambda x: sum(map(int, x.split(';')))) #silenziata da sara
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
    
    def getAccessionProject(self, accessionID):
        # Return the corresponding project ID for any accessionID entered as input

        s = rq.session()
        retries = Retry(total=5,
                        backoff_factor=0.1,
                        status_forcelist=[500, 502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        url = f"https://www.ebi.ac.uk/ena/portal/api/filereport?accession={accessionID}&result=read_run&fields=study_accession,secondary_study_accession,sample_accession,secondary_sample_accession,experiment_accession,run_accession&format=tsv&download=true&limit=0"
        headers = {"User-Agent": generate_user_agent()}
        content = s.get(url, headers=headers, allow_redirects=True).content
        incoming_df = pd.read_csv(io.StringIO(content.decode('utf-8')), sep='\t').reset_index(drop=True)
        projectID = incoming_df.iloc[0,0]

        return projectID


    def listOfAccessionIDsTSV(self, listOfProjectIDs, user_session): 
        #Creates user_session folder and saves the list of available accession IDs as TSV
        path = (os.path.join("Downloads", user_session))
        Utilities.createDirectory(path)

        listOfAccessionIDs = pd.DataFrame({"accession_ids":listOfProjectIDs})
        listOfAccessionIDs.to_csv(os.path.join(path, f'{user_session}_listOfAccessionIDs.tsv'), sep="\t", index=False)

        # logger = Utilities.log("Project", user_session)
        # logger.debug(f"[LIST-OF-ACCESSIONS-SAVED]: MADAME/Downloads/{user_session}/{user_session}_listOfAccessionIDs.tsv")

Project = Project('Project') 
