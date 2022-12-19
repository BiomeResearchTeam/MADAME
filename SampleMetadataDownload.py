import os
import requests as rq
import pandas as pd
from Utilities import Directory
from user_agent import generate_user_agent
from requests.adapters import HTTPAdapter, Retry

# Class for downloading sample metadata.

class SampleMetadataDownload:
    def __init__(self, name):
        self.name = name

    def runDownloadMetadata(self, listOfProjectIDs):
    # For each projectID in listOfProjectIDs, enters the project folder, creates
    # samples-metadata_xml folder, extracts sample ids from previously downloaded experiments metadata,
    # downloads sample metadata (xml) in samples-metadata_xml folder, exits to main dir.
    # WARNING : it needs a list of the AVAILABLE PROJECTS (IDlist.getAvailableProjects(listOfProjectIDs))
        
        for projectID in listOfProjectIDs:  

            os.chdir(projectID)
            
            # Read metadata file and check if it's empty or not
            experiments_metadata = f'{projectID}_experiments-metadata.tsv'
            if os.path.getsize(experiments_metadata) == 0:
                print(f'{projectID}_experiments-metadata.tsv is empty. Skipping.')  # no samples column!
            else:
                sample_xml_Directory = Directory("CreateSamplesXMLDirectory")
                sample_xml_Directory.createDirectory("samples-metadata_xml")
                experiments_metadata_df = pd.read_csv(experiments_metadata, sep='\t')
                sample_ids = experiments_metadata_df['sample_accession'].unique().tolist()

                for sampleID in sample_ids:
                    # Checking the file existence before downloading
                    if os.path.isfile(os.path.join('samples-metadata_xml', f'{sampleID}.xml')):
                        print(f"{sampleID} metadata file already downloaded, skipping. ({sample_ids.index(sampleID)+1}/{len(sample_ids)}) - project {listOfProjectIDs.index(projectID)+1}/{len(listOfProjectIDs)}")
                        pass
                    else:
                        print(f"Downloading {sampleID} metadata ({sample_ids.index(sampleID)+1}/{len(sample_ids)}) - project {listOfProjectIDs.index(projectID)+1}/{len(listOfProjectIDs)}")
                        self.sampleMetadataDownload(sampleID)
                print(f'✅   Successful download of {projectID} samples metadata!')  

            os.chdir(os.path.pardir)


    def sampleMetadataDownload(self, sampleID):
    # Download sample metadata file
        s = rq.session()
        retries = Retry(total=5,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries)) 

        url = f"https://www.ebi.ac.uk/ena/browser/api/xml/{sampleID}?download=true"
        headers = {"User-Agent": generate_user_agent()}
        download = s.get(url, headers=headers, allow_redirects=True)
        with open((os.path.join('samples-metadata_xml', f'{sampleID}.xml')), 'wb') as file:
            file.write(download.content)

