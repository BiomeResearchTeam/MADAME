import requests as rq
import os
import xml.etree.ElementTree as ET
import pandas as pd
from Experiment import Experiment
from Utilities import Utilities

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

    def getProjectBytes(self, projectID):
        os.chdir(projectID)
        # Read experiments metadata
        df = pd.read_csv(f'{projectID}_experiments-metadata.tsv', sep='\t')

        # Only read df lines which are not NaN in the fastq_bytes column (so, they are available runs)
        df1 = df[df['fastq_bytes'].notna()]

        # Group by fastq_ftp and then fastq_bytes columns: so if a file is repeated in multiple
        # lines (e.g. multiple samples for the same run), we count it only one time
        df2 = df1.groupby(['fastq_ftp','fastq_bytes'])['fastq_bytes'].count().to_frame(name = 'count').reset_index()

        # If files are paired-end, values in fastq_bytes will be a string, like '716429859;741556367'. 
        # Split the two numbers and add them to each other, before calculating the total of the column.
        if df2['fastq_bytes'].dtypes != 'int64':
            df3 = df2['fastq_bytes'].apply(lambda x: sum(map(int, x.split(';'))))
            bytes = df3.sum()

        # If files are single-end, values in fastq_bytes will be integers -> df.sum()
        else:
            bytes = df2['fastq_bytes'].sum() 

        os.chdir(os.path.pardir)

        return bytes

    def getProjectSize(self, projectID):
        bytes = self.getProjectBytes(projectID)
        convert = Utilities("convert")
        size = convert.bytes_converter(bytes)
             
        return size

    def getProjectInfo(self, projectID, field):
        # Utility function for getProjectName, getProjectTitle, getProjectDescription functions.
        os.chdir(projectID)
        tree = ET.parse(f'{projectID}_project-metadata.xml')
        root = tree.getroot()

        for children in root.iter("PROJECT"):
            child = children.find(field)
            if child is not None:
                value = child.text
            else:
                value = f"ERROR: MISSING FIELD ({field})"
        
        os.chdir(os.path.pardir)

        return value   

    def getProjectName(self, projectID):
        projectName = self.getProjectInfo(projectID, "NAME")
        print('Project Name:', projectName)

    def getProjectTitle(self, projectID):
        projectTitle = self.getProjectInfo(projectID, "TITLE")
        print('Project Title:', projectTitle)

    def getProjectDescription(self, projectID):
        projectDescription = self.getProjectInfo(projectID, "DESCRIPTION")
        print('Project Description:', projectDescription)
   
    
#   EDITATO FIN QUI ########

    def createExperiments(self, logger, listOfExp):
        logger.info('[CREATE-EXPERIMENTS]: ' + str(listOfExp))
        for item, idExp in enumerate(listOfExp):
            experiment = Experiment(projectID=idExp)
            self.listOfExperiments.append(experiment)

    def toXML(self, logger):
        logger.info('[CREATE-XML-PROJECT] - ID: ' + str(self.IDProject))
        # qui creo il singolo nodo xml per il progetto corrente
        # richiamo experiment.toXML() perchè ogni singolo project
        # contiene una (potenziale) lista di experiments
        # gli xml-element degli experiment fanno riferimento allo stesso
        # xml-element di projects
        '''
            <project id="PRJEB1787">
                <experiments>
                    <exp1>
                        <samples> <sample> </sample> </samples>
                    </exp1>
                    <exp2>
                        <samples> <sample> </sample> </samples>
                    </exp2>
                </experiments>
            <project>
        '''
        logger.info('[CREATE-XML-EXPERIMENTS] - IDs: ' + str(self.listOfExperiments))
        for exp in self.listOfExperiments:
            expXml = exp.toXMLExperiment()

        return

os.chdir("/mnt/c/Users/conog/Desktop/MADAME")
size = Project("size")
print(size.getProjectSize('PRJEB31610'))