import os
import requests as rq
from Utilities import Directory

# Class for downloading project and experiments metadata.

class Exp_Proj_MetadataDownload:
    def __init__(self, name):
        self.name = name   
    
    def runDownloadMetadata(self, listOfProjectIDs):
    # For each projectID in listOfProjectIDs creates project folder and downloads metadata.
    # WARNING : it needs a list of the AVAILABLE PROJECTS (IDlist.getAvailableProjects(listOfProjectIDs))
        for projectID in listOfProjectIDs:
            projectDirectory = Directory("CreateDirectory")
            projectDirectory.createDirectory(projectID)
            self.projectMetadataDownload(projectID)
            self.experimentsMetadataDownload(projectID)
        return

    
    def projectMetadataDownload(self, projectID):
    # Download project metadata file only if it doesn't exist
        if os.path.isfile(os.path.join(f'{projectID}', f'{projectID}_project-metadata.xml')):
            print(f'{projectID}_project-metadata.xml already exist!')
        else:
            url = f"https://www.ebi.ac.uk/ena/browser/api/xml/{projectID}"
            download = rq.get(url, allow_redirects=True)
            with open((os.path.join(f'{projectID}', f'{projectID}_project-metadata.xml')), 'wb') as file:
                file.write(download.content)
            print(f'✅  Successful download of {projectID}_project-metadata.xml')
        
        return

    def experimentsMetadataDownload(self, projectID):
    # Download experiments metadata file only if it doesn't exist
        if os.path.isfile(os.path.join(f'{projectID}', f'{projectID}_experiments-metadata.tsv')):
            print(f'{projectID}_experiments-metadata.tsv already exist!')
        else:
            url = f"https://www.ebi.ac.uk/ena/portal/api/filereport?accession={projectID}&result=read_run&fields=study_accession,secondary_study_accession,sample_accession,secondary_sample_accession,experiment_accession,run_accession,submission_accession,tax_id,scientific_name,instrument_platform,instrument_model,library_name,nominal_length,library_layout,library_strategy,library_source,library_selection,read_count,base_count,center_name,first_public,last_updated,experiment_title,study_title,study_alias,experiment_alias,run_alias,fastq_bytes,fastq_md5,fastq_ftp,fastq_aspera,fastq_galaxy,submitted_bytes,submitted_md5,submitted_ftp,submitted_aspera,submitted_galaxy,submitted_format,sra_bytes,sra_md5,sra_ftp,sra_aspera,sra_galaxy,cram_index_ftp,cram_index_aspera,cram_index_galaxy,sample_alias,broker_name,sample_title,nominal_sdev,first_created&format=tsv&download=true&limit=0"
            download = rq.get(url, allow_redirects=True)
            with open((os.path.join(f'{projectID}', f'{projectID}_experiments-metadata.tsv')), 'wb') as file:
                file.write(download.content)                
            print(f'✅  Successful download of {projectID}_experiments-metadata.tsv')