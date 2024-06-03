import os
import requests as rq
import pandas as pd
from Utilities import Utilities, Color, LoggerManager
from user_agent import generate_user_agent
from requests.adapters import HTTPAdapter, Retry
from rich.progress import track
from rich import print as rich_print
from Project import Project
import time

# Class for downloading sample metadata.

class SampleMetadataDownload:
    def __init__(self, name):
        self.name = name

    def runDownloadMetadata(self, listOfProjectIDs, user_session):
    # For each projectID in listOfProjectIDs, enters the project folder, creates
    # samples-metadata_xml folder, extracts sample ids from previously downloaded experiments metadata,
    # downloads sample metadata (xml) in samples-metadata_xml folder, exits to main dir.
    # WARNING : it needs a list of the AVAILABLE PROJECTS (IDlist.getAvailableProjects(listOfProjectIDs))

        projects_list = listOfProjectIDs
        cyan = "rgb(0,255,255)"
        logger = LoggerManager.log(user_session)
        
        # Determining if there's umbrella projects from listOfAccessionIDs' type
        if type(listOfProjectIDs) is dict:
            projects_list = list(listOfProjectIDs.keys())

        
        for projectID in projects_list:  

            path = os.path.join("Downloads", user_session, projectID)
            # Read metadata file and check if it's empty or not
            experiments_metadata = os.path.join(path , f'{projectID}_experiments-metadata.tsv')

            # Print according to project type
            if os.path.getsize(experiments_metadata) == 0:
                if type(listOfProjectIDs) is dict and listOfProjectIDs[f'{projectID}'] == True:
                    rich_print(f'Metadata file for [yellow]☂[/yellow] {projectID} is empty. Skipping.')
                else:
                    rich_print(f'Metadata file for {projectID} is empty. Skipping.')  
            else:
                experiments_metadata_df = pd.read_csv(experiments_metadata, sep='\t', dtype=str)
                
                # If projectID is an umbrella project
                if type(listOfProjectIDs) is dict and listOfProjectIDs[f'{projectID}'] == True:
                    component_samples_metadata_xml_folder = os.path.join(path, "component_samples-metadata_xml")
                    Utilities.createDirectory(component_samples_metadata_xml_folder)

                    # Obtain list of component projects
                    component_projects = Project.getComponentProjects(projectID, "local", user_session)
                    
                    for project in component_projects:
                        # logger
                        logger.debug(f"Downloading ☂ {projectID} [project {projects_list.index(projectID)+1}/{len(projects_list)}] → {project} [component {component_projects.index(project)+1}/{len(component_projects)}] sample metadata")

                        sample_ids = experiments_metadata_df.loc[experiments_metadata_df['study_accession'] == f'{project}', 'sample_accession'].unique().tolist()

                        samples_metadata_xml_folder = os.path.join(component_samples_metadata_xml_folder, f'{project}_samples-metadata_xml')
                        Utilities.createDirectory(samples_metadata_xml_folder)

                        for sampleID in track(sample_ids, description=f"Downloading [yellow]☂[/yellow] {projectID} \[project [{cyan}]{projects_list.index(projectID)+1}[/{cyan}]/[{cyan}]{len(projects_list)}[/{cyan}]] → {project} \[component [{cyan}]{component_projects.index(project)+1}[/{cyan}]/[{cyan}]{len(component_projects)}[/{cyan}]] sample metadata: "):

                            # Checking the file existence before downloading
                            if sampleID.count("SAMN") > 1: #avoid error for multiple samples 
                                single_sampleID = sampleID.split(";")
                                for sampleID in single_sampleID:
                                    if os.path.isfile(os.path.join(samples_metadata_xml_folder, f'{sampleID}.xml')):
                                        pass
                                    else:
                                        self.sampleMetadataDownload(sampleID, samples_metadata_xml_folder, project, user_session)
                            else:
                                if os.path.isfile(os.path.join(samples_metadata_xml_folder, f'{sampleID}.xml')):
                                    pass
                                else:
                                    self.sampleMetadataDownload(sampleID, samples_metadata_xml_folder, project, user_session)

                    rich_print(f'[yellow]☂[/yellow] {projectID} → {project} samples metadata files were [b rgb(0,255,0)]successfully downloaded[/b rgb(0,255,0)]\n')

    
                
                # If projectID is NOT an umbrella project
                else:
                    # logger
                    logger.debug(f"Downloading {projectID} [project {projects_list.index(projectID)+1}/{len(projects_list)}] sample metadata")
                    
                    samples_metadata_xml_folder = os.path.join(path, "samples-metadata_xml")
                    Utilities.createDirectory(samples_metadata_xml_folder)

                    sample_ids = experiments_metadata_df['sample_accession'].unique().tolist()

                    for sampleID in track(sample_ids, description=f"Downloading {projectID} \[project [{cyan}]{projects_list.index(projectID)+1}[/{cyan}]/[{cyan}]{len(projects_list)}[/{cyan}]] sample metadata: "):

                        # Checking the file existence before downloading
                        if sampleID.count("SAMN") > 1: #avoid error for multiple samples 
                            single_sampleID = sampleID.split(";")
                            for sampleID in single_sampleID:
                                if os.path.isfile(os.path.join(samples_metadata_xml_folder, f'{sampleID}.xml')):
                                    pass
                                else:
                                    self.sampleMetadataDownload(sampleID, samples_metadata_xml_folder, projectID, user_session)
                        else:
                            if os.path.isfile(os.path.join(samples_metadata_xml_folder, f'{sampleID}.xml')):
                                pass
                            else:
                                self.sampleMetadataDownload(sampleID, samples_metadata_xml_folder, projectID, user_session)

                    rich_print(f'{projectID} samples metadata files were [b rgb(0,255,0)]successfully downloaded[/b rgb(0,255,0)]\n')


    def sampleMetadataDownload(self, sampleID, sample_metadata_xml_folder, projectID, user_session):
    # Download sample metadata file

        logger = LoggerManager.log(user_session)
        s = rq.session()
        retries = Retry(total=5,
                    backoff_factor=0.1,
                    status_forcelist=[429, 500, 502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        url = f"https://www.ebi.ac.uk/ena/browser/api/xml/{sampleID}?download=true"
        headers = {"User-Agent": generate_user_agent()}
        logger.debug(f"sampleID: {sampleID}")
        try:
            download = s.get(url, headers=headers, allow_redirects=True)
            with open((os.path.join(sample_metadata_xml_folder, f'{sampleID}.xml')), 'wb') as file:
                file.write(download.content)
        except rq.exceptions.ChunkedEncodingError as e:
            rich_print(f"[yellow]ChunkedEncodingError: {e}[/yellow] for sampleID {sampleID}. Waiting 3 seconds, then [u]trying again[/u].")
            logger.debug(f"ChunkedEncodingError: {e} for sampleID {sampleID}. Waiting 3 seconds, then trying again.")
            time.sleep(3)
            try:
                download = s.get(url, headers=headers, allow_redirects=True)
                with open((os.path.join(sample_metadata_xml_folder, f'{sampleID}.xml')), 'wb') as file:
                    file.write(download.content)  
            except rq.exceptions.ChunkedEncodingError as e:
                rich_print(f"[yellow]ChunkedEncodingError: {e}[/yellow] for sampleID {sampleID}. It is not possible at the moment to download {sampleID}.xml.\nYou will find this information in the log file.")
                logger.debug(f"ChunkedEncodingError: {e} for sampleID {sampleID}. It is not possible at the moment to download {sampleID}.xml. FILE SKIPPED.")
            
            #if isinstance(e.__cause__, IncompleteRead): 
                #incomplete_read_exception = e.__cause__
                #print(f"IncompleteRead Exception: {incomplete_read_exception}")
                #logger.debug(f"IncompleteRead Exception: {incomplete_read_exception}")
    
SampleMetadataDownload = SampleMetadataDownload('SampleMetadataDownload')