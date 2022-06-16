import os
import requests as rq
import pandas as pd
from Utilities import Directory

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
            sample_xml_Directory = Directory("CreateSamplesXMLDirectory")
            sample_xml_Directory.createDirectory("samples-metadata_xml")
            experiments_metadata = pd.read_csv(f'{projectID}_experiments-metadata.tsv', sep='\t')
            sample_ids = experiments_metadata['sample_accession'].tolist()
            for sampleID in sample_ids:
                self.sampleMetadataDownload(sampleID)
            os.chdir(os.path.pardir)
            print(f'✅   Successful download of {projectID} samples metadata!')  


    def sampleMetadataDownload(self, sampleID):
    # Download sample metadata file only if it doesn't exist
        if os.path.isfile(os.path.join('samples-metadata_xml', f'{sampleID}.xml')):
            pass
        else:
            url = f"https://www.ebi.ac.uk/ena/browser/api/xml/{sampleID}?download=true"
            download = rq.get(url, allow_redirects=True)
            with open((os.path.join('samples-metadata_xml', f'{sampleID}.xml')), 'wb') as file:
                file.write(download.content)


