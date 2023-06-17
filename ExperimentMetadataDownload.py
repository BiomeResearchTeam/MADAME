import os
import requests as rq
from Utilities import Utilities
from IDlist import GetIDlist
from user_agent import generate_user_agent
from requests.adapters import HTTPAdapter, Retry
from rich.progress import track
import pandas as pd
from Utilities import Color 
import re
import io

# Class for downloading project and experiments metadata.

class Exp_Proj_MetadataDownload:
    def __init__(self, name):
        self.name = name   
    
    def runDownloadMetadata(self, listOfAccessionIDs, user_session):
    # For each accession in listOfAccessionIDs creates the corresponding project folder and downloads metadata.
    # WARNING : it needs a list of the AVAILABLE PROJECTS (ProjectManager.getAvailableProjects(listOfAccessionIDs))  
        
        GENERIC_RANGE_PATTERN = r'^[a-zA-Z0-9]+-[a-zA-Z0-9]+$' 

        study_accession = []

        for accessionID in track(listOfAccessionIDs, description="Downloading..."): #--> should change into 'list of accession ids'

            if re.match(GetIDlist.PROJECTS_PATTERN, accessionID):
                projectID = accessionID
                study_accession.append(projectID)
                self.experimentsMetadataDownload_project(projectID, user_session)
                self.projectMetadataDownload(projectID, user_session, print_message = True) 

            elif re.match(GENERIC_RANGE_PATTERN, accessionID):
                projectID = self.experimentsMetadataDownload_range(accessionID, user_session)
                study_accession.append(projectID)
                self.projectMetadataDownload(projectID, user_session, print_message = True)

            else:
                projectID = self.experimentsMetadataDownload_other(accessionID, user_session)
                study_accession.append(projectID)
                self.projectMetadataDownload(projectID, user_session, print_message = False) # to prevent printing multiple times "the file already exists"

        # Merge all experiments-metadata files in a single file
        self.mergeExperimentsMetadata(user_session)

        # Update listOfAccessionIDs.tsv adding a second column, for project reference
        self.updateListOfAccessions(user_session, study_accession)

        # Removing duplicates to return a clean list for sample metadata download
        study_accession = list(dict.fromkeys(study_accession)) 

        return study_accession

  
    def projectMetadataDownload(self, projectID, user_session, print_message = True):
    # Download project metadata file only if it doesn't exist
        path = os.path.join("Downloads", user_session, projectID)
        if os.path.isfile(os.path.join(path, f'{projectID}_project-metadata.xml')):
            if print_message == True:
                print(f'{projectID}_project-metadata.xml', Color.BOLD + Color.GREEN + 'already exist!' + Color.END)
        else:
            s = rq.session()
            retries = Retry(total=5,
                            backoff_factor=0.1,
                            status_forcelist=[500, 502, 503, 504])
            s.mount('https://', HTTPAdapter(max_retries=retries))

            url = f"https://www.ebi.ac.uk/ena/browser/api/xml/{projectID}"
            headers = {"User-Agent": generate_user_agent()}
            download = s.get(url, headers=headers, allow_redirects=True)
            with open((os.path.join(path, f'{projectID}_project-metadata.xml')), 'wb') as file: 
                file.write(download.content)
            print(f'{projectID}_project-metadata.xml ' + Color.BOLD + Color.GREEN + 
            ' successfully downloaded' + Color.END)
     
        return

    def experimentsMetadataDownload_project(self, projectID, user_session):
    # Download experiments metadata file only if it doesn't exist - project accession code version
        path = os.path.join("Downloads", user_session, projectID)
        Utilities.createDirectory(path)

        if os.path.isfile(os.path.join(path, f'{projectID}_experiments-metadata.tsv')):
            print(f'{projectID}_experiments-metadata.tsv', Color.BOLD + Color.GREEN + 'already exist!' + Color.END)
        else:
            s = rq.session()
            retries = Retry(total=5,
                            backoff_factor=0.1,
                            status_forcelist=[500, 502, 503, 504])
            s.mount('https://', HTTPAdapter(max_retries=retries))

            url = f"https://www.ebi.ac.uk/ena/portal/api/filereport?accession={projectID}&result=read_run&fields=study_accession,secondary_study_accession,sample_accession,secondary_sample_accession,experiment_accession,run_accession,submission_accession,tax_id,scientific_name,instrument_platform,instrument_model,library_name,nominal_length,library_layout,library_strategy,library_source,library_selection,read_count,base_count,center_name,first_public,last_updated,experiment_title,study_title,study_alias,experiment_alias,run_alias,fastq_bytes,fastq_md5,fastq_ftp,fastq_aspera,fastq_galaxy,submitted_bytes,submitted_md5,submitted_ftp,submitted_aspera,submitted_galaxy,submitted_format,sra_bytes,sra_md5,sra_ftp,sra_aspera,sra_galaxy,sample_alias,broker_name,sample_title,nominal_sdev,first_created&format=tsv&download=true&limit=0"
            headers = {"User-Agent": generate_user_agent()}
            download = s.get(url, headers=headers, allow_redirects=True)
            with open((os.path.join(path, f'{projectID}_experiments-metadata.tsv')), 'wb') as file:
                file.write(download.content)                
            print(f'{projectID}_experiments-metadata.tsv' + Color.BOLD + Color.GREEN + 
            ' successfully downloaded' + Color.END)

    def experimentsMetadataDownload_other(self, accessionID, user_session):
    # Download experiments metadata file only if it doesn't exist - other accession code version
       
        s = rq.session()
        retries = Retry(total=5,
                        backoff_factor=0.1,
                        status_forcelist=[500, 502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        url = f"https://www.ebi.ac.uk/ena/portal/api/filereport?accession={accessionID}&result=read_run&fields=study_accession,secondary_study_accession,sample_accession,secondary_sample_accession,experiment_accession,run_accession,submission_accession,tax_id,scientific_name,instrument_platform,instrument_model,library_name,nominal_length,library_layout,library_strategy,library_source,library_selection,read_count,base_count,center_name,first_public,last_updated,experiment_title,study_title,study_alias,experiment_alias,run_alias,fastq_bytes,fastq_md5,fastq_ftp,fastq_aspera,fastq_galaxy,submitted_bytes,submitted_md5,submitted_ftp,submitted_aspera,submitted_galaxy,submitted_format,sra_bytes,sra_md5,sra_ftp,sra_aspera,sra_galaxy,sample_alias,broker_name,sample_title,nominal_sdev,first_created&format=tsv&download=true&limit=0"
        headers = {"User-Agent": generate_user_agent()}
        content = s.get(url, headers=headers, allow_redirects=True).content
        incoming_df = pd.read_csv(io.StringIO(content.decode('utf-8')), sep='\t').reset_index(drop=True)
        projectID = incoming_df.loc[incoming_df.index[0], 'study_accession']

        path = os.path.join("Downloads", user_session, projectID)
        Utilities.createDirectory(path)

        # Check if experiments-metadata.tsv file is already present
        metadata_file = os.path.join(path, f'{projectID}_experiments-metadata.tsv')
        if os.path.isfile(metadata_file):
            local_df = pd.read_csv(metadata_file, sep="\t")
            local_df_numpy = local_df.to_numpy()
            # Check if accessionID is already in the experiments-metadata.tsv file
            if accessionID in local_df_numpy:
                print(f'{accessionID} is', Color.BOLD + Color.GREEN + 'already present ' + Color.END + f'in {projectID}_experiments-metadata.tsv!')
            # If not, merge dataframes and save with the same name
            else:
                merged_dataframe = pd.concat([local_df, incoming_df]).drop_duplicates().reset_index(drop=True)
                merged_dataframe.to_csv(os.path.join(path, f'{projectID}_experiments-metadata.tsv'), sep="\t", index=False)
                print(f'{accessionID} ', Color.BOLD + Color.GREEN + 'successfully added' + Color.END + f' to {projectID}_experiments-metadata.tsv')

        # If not, save the retrieved dataframe to experiments-metadata.tsv
        else:
            incoming_df.to_csv(os.path.join(path, f'{projectID}_experiments-metadata.tsv'), sep="\t", index = False)
            print(f'{projectID}_experiments-metadata.tsv' + Color.BOLD + Color.GREEN + 
            ' successfully downloaded' + Color.END)

        return projectID

    def experimentsMetadataDownload_range(self, accessionID, user_session):
        # Download experiments metadata file only if it doesn't exist - accessions range version

        accessions = GetIDlist.expand_accessions_range(accessionID)
       
        s = rq.session()
        retries = Retry(total=5,
                        backoff_factor=0.1,
                        status_forcelist=[500, 502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        url_1 = f"https://www.ebi.ac.uk/ena/portal/api/filereport?accession={accessions[0]}&result=read_run&fields=study_accession,secondary_study_accession,sample_accession,secondary_sample_accession,experiment_accession,run_accession&format=tsv&download=true&limit=0"
        headers = {"User-Agent": generate_user_agent()}
        content_1 = s.get(url_1, headers=headers, allow_redirects=True).content
        incoming_df_1 = pd.read_csv(io.StringIO(content_1.decode('utf-8')), sep='\t')
        projectID = incoming_df_1.loc[incoming_df_1.index[0], 'study_accession']

        # After obtaining the corresponding projectID, access to the whole project's metadata and
        # filter it selecting only the rows corresponding to the accessions range
        url_2 = f"https://www.ebi.ac.uk/ena/portal/api/filereport?accession={projectID}&result=read_run&fields=study_accession,secondary_study_accession,sample_accession,secondary_sample_accession,experiment_accession,run_accession,submission_accession,tax_id,scientific_name,instrument_platform,instrument_model,library_name,nominal_length,library_layout,library_strategy,library_source,library_selection,read_count,base_count,center_name,first_public,last_updated,experiment_title,study_title,study_alias,experiment_alias,run_alias,fastq_bytes,fastq_md5,fastq_ftp,fastq_aspera,fastq_galaxy,submitted_bytes,submitted_md5,submitted_ftp,submitted_aspera,submitted_galaxy,submitted_format,sra_bytes,sra_md5,sra_ftp,sra_aspera,sra_galaxy,sample_alias,broker_name,sample_title,nominal_sdev,first_created&format=tsv&download=true&limit=0"
        content_2 = s.get(url_2, headers=headers, allow_redirects=True).content
        incoming_df_2 = pd.read_csv(io.StringIO(content_2.decode('utf-8')), sep='\t')

        if re.match(GetIDlist.RUNS_PATTERN, accessions[0]):
            column_name = "run_accession"
        if re.match(GetIDlist.EXPERIMENTS_PATTERN, accessions[0]):
            column_name = "experiment_accession"
        if re.match(GetIDlist.SAMPLES_PATTERN, accessions[0]):
            column_name = "secondary_sample_accession"
        if re.match(GetIDlist.BIOSAMPLES_PATTERN, accessions[0]):
            column_name = "sample_accession"

        incoming_df_2 = incoming_df_2[incoming_df_2[column_name].between(accessions[0], accessions[-1])].reset_index(drop=True)

        path = os.path.join("Downloads", user_session, projectID)
        Utilities.createDirectory(path)

        # Check if experiments-metadata.tsv file is already present
        metadata_file = os.path.join(path, f'{projectID}_experiments-metadata.tsv')
        if os.path.isfile(metadata_file):
            local_df = pd.read_csv(metadata_file, sep="\t")
            local_df_numpy = local_df.to_numpy()
            # If all the accessions in the range are already in the experiments-metadata.tsv file, skip
            if all(id in local_df_numpy for id in accessions):
                print(f'{accessionID} is', Color.BOLD + Color.GREEN + 'already present ' + Color.END + f'in {projectID}_experiments-metadata.tsv!')
            # If only part of the accessions in the range are already present, merge without duplicates
            elif any(id in local_df_numpy for id in accessions):
                print(f'Part of {accessionID} is', Color.BOLD + Color.GREEN + 'already present ' + Color.END + f'in {projectID}_experiments-metadata.tsv.')
                merged_dataframe = pd.concat([local_df, incoming_df_2]).drop_duplicates().reset_index(drop=True)
                merged_dataframe.to_csv(os.path.join(path, f'{projectID}_experiments-metadata.tsv'), sep="\t", index = False)
                print(f'{accessionID} range', Color.BOLD + Color.GREEN + 'successfully added' + Color.END + f' to {projectID}_experiments-metadata.tsv')
            # If no accession from the range is present, merge dataframes and save with the same name
            else:
                merged_dataframe = pd.concat([local_df, incoming_df_2]).drop_duplicates().reset_index(drop=True)
                merged_dataframe.to_csv(os.path.join(path, f'{projectID}_experiments-metadata.tsv'), sep="\t", index = False)
                print(f'{accessionID} range', Color.BOLD + Color.GREEN + 'successfully added' + Color.END + f' to {projectID}_experiments-metadata.tsv')

        # If not, save the retrieved dataframe to experiments-metadata.tsv
        else:
            incoming_df_2.to_csv(os.path.join(path, f'{projectID}_experiments-metadata.tsv'), sep="\t", index = False)
            print(f'{projectID}_experiments-metadata.tsv' + Color.BOLD + Color.GREEN + 
            ' successfully downloaded' + Color.END)

        return projectID


    def mergeExperimentsMetadata(self, user_session):

        logger = Utilities.log("ExperimentMetadataDownload", user_session)
        path = (os.path.join("Downloads", user_session))
        dataframes = []

        for dir in os.listdir(path):
                tsv = f'{dir}_experiments-metadata.tsv'
                tsv_path = os.path.join(path, dir, tsv)
                if os.path.isfile(tsv_path) and os.path.getsize(tsv_path) > 0:
                    dataframes.append(pd.read_csv(tsv_path, sep='\t'))

        # Stop and print message if dataframes list is empty
        if not dataframes:
            logger.debug(f"[ERROR] - couldn't create {user_session}_merged_experiments-metadata.tsv: no experiments-metadata.tsv file found")
            print(f"\nError: couldn't create {user_session}_merged_experiments-metadata.tsv: " + Color.BOLD + Color.RED + 
            "no experiments-metadata.tsv file found." + Color.END)   ####messaggio da rivedere
            return 

        merged_dataframe = pd.concat(dataframes)
        merged_dataframe.to_csv(os.path.join(path, f'{user_session}_merged_experiments-metadata.tsv'), sep="\t")

        logger.debug(f"{user_session}_merged_experiments-metadata.tsv successfully created")
        print(f'\n{user_session}_merged_experiments-metadata.tsv' + Color.BOLD + Color.GREEN + 
            ' successfully created' + Color.END)

    def updateListOfAccessions(self, user_session, study_accession):

        listOfAccessionIDs_file = (os.path.join("Downloads", user_session, f'{user_session}_listOfAccessionIDs.tsv'))
        df = pd.read_csv(listOfAccessionIDs_file, sep='\t')
        df['study_accession'] = study_accession
        df.to_csv(listOfAccessionIDs_file, sep="\t", index=False)

        print(f'\n{user_session}_listOfAccessionIDs.tsv' + Color.BOLD + Color.GREEN + ' successfully updated\n' + Color.END)


Exp_Proj_MetadataDownload = Exp_Proj_MetadataDownload('Exp_Proj_MetadataDownload')