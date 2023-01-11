import os
import requests as rq
from Utilities import Utilities
from user_agent import generate_user_agent
from requests.adapters import HTTPAdapter, Retry
from rich.progress import track
import pandas as pd
from Utilities import Color 

# Class for downloading project and experiments metadata.

class Exp_Proj_MetadataDownload:
    def __init__(self, name):
        self.name = name   
    
    def runDownloadMetadata(self, listOfProjectIDs, user_session):
    # For each projectID in listOfProjectIDs creates project folder and downloads metadata.
    # WARNING : it needs a list of the AVAILABLE PROJECTS (ProjectManager.getAvailableProjects(listOfProjectIDs))  
        
        for projectID in track(listOfProjectIDs, description="Downloading..."):
            path = os.path.join("Downloads", user_session, projectID)
            Utilities.createDirectory(path)
            self.projectMetadataDownload(projectID, path) 
            self.experimentsMetadataDownload(projectID, path)
        
        self.mergeExperimentsMetadata(user_session)

  
    def projectMetadataDownload(self, projectID, path):
    # Download project metadata file only if it doesn't exist
        if os.path.isfile(os.path.join(path, f'{projectID}_project-metadata.xml')):
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
            print(f'\n{projectID}_project-metadata.xml was' + Color.BOLD + Color.GREEN + 
            ' successfully downloaded' + Color.END)
        
        return

    def experimentsMetadataDownload(self, projectID, path):
    # Download experiments metadata file only if it doesn't exist
        if os.path.isfile(os.path.join(path, f'{projectID}_experiments-metadata.tsv')):
            print(f'{projectID}_experiments-metadata.tsv', Color.BOLD + Color.GREEN + 'already exist!' + Color.END)
        else:
            s = rq.session()
            retries = Retry(total=5,
                            backoff_factor=0.1,
                            status_forcelist=[500, 502, 503, 504])
            s.mount('https://', HTTPAdapter(max_retries=retries))

            url = f"https://www.ebi.ac.uk/ena/portal/api/filereport?accession={projectID}&result=read_run&fields=study_accession,secondary_study_accession,sample_accession,secondary_sample_accession,experiment_accession,run_accession,submission_accession,tax_id,scientific_name,instrument_platform,instrument_model,library_name,nominal_length,library_layout,library_strategy,library_source,library_selection,read_count,base_count,center_name,first_public,last_updated,experiment_title,study_title,study_alias,experiment_alias,run_alias,fastq_bytes,fastq_md5,fastq_ftp,fastq_aspera,fastq_galaxy,submitted_bytes,submitted_md5,submitted_ftp,submitted_aspera,submitted_galaxy,submitted_format,sra_bytes,sra_md5,sra_ftp,sra_aspera,sra_galaxy,cram_index_ftp,cram_index_aspera,cram_index_galaxy,sample_alias,broker_name,sample_title,nominal_sdev,first_created&format=tsv&download=true&limit=0"
            headers = {"User-Agent": generate_user_agent()}
            download = s.get(url, headers=headers, allow_redirects=True)
            with open((os.path.join(path, f'{projectID}_experiments-metadata.tsv')), 'wb') as file:
                file.write(download.content)                
            print(f'{projectID}_experiments-metadata.tsv' + Color.BOLD + Color.GREEN + 
            ' successfully downloaded' + Color.END)

    def mergeExperimentsMetadata(self, user_session):

        path = (os.path.join("Downloads", user_session))
        dataframes = []

        for dir in os.listdir(path):
                tsv = f'{dir}_experiments-metadata.tsv'
                tsv_path = os.path.join(path, dir, tsv)
                if os.path.isfile(tsv_path) and os.path.getsize(tsv_path) > 0:
                    dataframes.append(pd.read_csv(tsv_path, sep='\t'))

        # stop if dataframes list is empty
        if not dataframes:
            return

        merged_dataframe = pd.concat(dataframes)
        merged_dataframe.to_csv(os.path.join(path, f'{user_session}_merged_experiments-metadata.tsv'), sep="\t")

        print(f'{user_session}_merged_experiments-metadata.tsv' + Color.BOLD + Color.GREEN + 
            ' successfully created' + Color.END)

        return


Exp_Proj_MetadataDownload = Exp_Proj_MetadataDownload('Exp_Proj_MetadataDownload')