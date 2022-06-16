import xml.etree.ElementTree as ET
import urllib.request
import requests as rq
import pandas as pd
import os

# Class for finding publications from one or more accession IDs.
# It returns a .tsv dataframe.

class GetPublications:
    def __init__(self, name):
        self.name = name 

    def runGetPublications(self, listOfProjectIDs):

        for projectID in listOfProjectIDs:
            experiments_metadata = os.path.join(projectID, f'{projectID}_experiments-metadata.tsv')
            metadata_df = pd.read_csv(experiments_metadata, sep='\t')
            accessions_list = []
            accessions_columns = ['study_accession', 'secondary_study_accession', 'sample_accession', 'secondary_sample_accession', 'experiment_accession', 'run_accession', 'submission_accession']
            for column in accessions_columns:
                accessions = metadata_df[column].unique().tolist()
                for accession in accessions:
                    accessions_list.append(accession)
            print(accessions_list)   #prova
        


    def PMC_dataframe(self, accessions_list):
        # ...
        #aggiungere le due colonne con id cercato e id trovato

        def europePMCIterator(tag_1, tag_2, tag_2_renamed = None):
            for children in tree.iter(tag_1):
                child = children.find(tag_2)
                
                if tag_2_renamed:
                        labels.append(tag_2_renamed)
                else:
                        labels.append(tag_2) 
                
                if child is not None:
                    value = child.text                 
                    data.append(value)
                else:
                    data.append("NA")


        empty_df = []      

        for accession_id in accessions_list:
            query = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={accession_id}&format=xml&resultType=core"
            response = urllib.request.urlopen(query).read()
            tree = ET.fromstring(response)

            labels = []
            data = []
            
            for hit in tree.iter('responseWrapper'):
                hitcount = int(hit.find('hitCount').text)
                if hitcount == 0:
                    pass
                else:
                    europePMCIterator('result', 'id')
                    europePMCIterator('result', 'source')
                    europePMCIterator('result', 'pmid')
                    europePMCIterator('result', 'pmcid')
                    europePMCIterator('result', 'doi')
                    europePMCIterator('result', 'title')
                    europePMCIterator('result', 'authorString')
                    europePMCIterator('journal', 'title', 'journal_title')
                    europePMCIterator('journalInfo', 'issue', 'journal_issue')
                    europePMCIterator('journalInfo', 'volume', 'journal_volume')
                    europePMCIterator('result', 'pubYear')
                    europePMCIterator('result', 'pageInfo')
                    europePMCIterator('pubTypeList', 'pubType')
                    europePMCIterator('result', 'isOpenAccess')
                    europePMCIterator('result', 'inEPMC')
                    europePMCIterator('result', 'inPMC')
                    europePMCIterator('result', 'hasPDF')
                    europePMCIterator('result', 'hasSuppl')
                    europePMCIterator('result', 'hasData')
                    europePMCIterator('result', 'hasTextMinedTerms')              

            # Build dictionary from labels and relative data
            d = dict(zip(labels, data))  #e se d è vuoto?
            empty_df.append(d)

        # Convert into dataframe
        PMC_dataframe = pd.DataFrame(empty_df)
        PMC_dataframe.to_csv("prova.tsv", sep="\t") #temporaneo

        return PMC_dataframe


    def retrievePublicationID(self, projectID):
        pass

    def getXMLfulltext(self, publicationID):
        pass

    def getFileLinks(self, publicationID):
        pass

    def getFileSize(self, file_link):
        pass



os.chdir("/mnt/c/Users/conog/Desktop/MADAME")

prova = GetPublications('prova')
print(prova.PMC_dataframe(['PRJEB33230']))
prova.runGetPublications(['PRJEB25465'])