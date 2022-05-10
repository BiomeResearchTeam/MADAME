import requests as rq
from Experiment import Experiment

class Project:
    def __init__(self, projectID):
        self.ProjectID = projectID
    

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

    def getProjectDescription(self):
        pass

    def getProjectName(self):
        pass

    def getProjectID(self):
        return self.ProjectID

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
