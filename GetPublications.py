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
        #aggiungere le due colonne con id cercato e id trovato

        def europePMCIterator(tag_1, tag_2 = None, tag_renamed = None, mode = None):
            
            if mode == None:
            
                for children in tree.iter(tag_1):
                    child = children.find(tag_2) 

                    if tag_renamed:
                        labels.append(tag_renamed)
                    else:
                        labels.append(tag_2)

                    if child is not None:
                        value = child.text                 
                        data.append(value)
                    else:
                        data.append("NA")

    
                
            if mode == "multiple":

                value_list = []

                if tag_renamed:
                    labels.append(tag_renamed)
                else:
                    labels.append(tag_1) 

                for children in tree.iter(tag_1):
                    single_value = children.text
                    value_list.append(single_value)

                if value_list:
                    values = ';'.join(value_list)
                    data.append(values)
                else:
                    data.append("NA")


        empty_df = []      

        for accession_id in accessions_list:
            query = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={accession_id}&format=xml&resultType=core"
            response = urllib.request.urlopen(query).read()
            tree = ET.fromstring(response)

            
            for hit in tree.iter('responseWrapper'):
                hitcount = int(hit.find('hitCount').text)
                if hitcount == 0:
                    pass

                else:                    
                    labels = []
                    data = []
                    labels.append("queried_accession_id")
                    data.append(accession_id)
                    europePMCIterator('result', 'id')
                    europePMCIterator('result', 'source')
                    europePMCIterator('result', 'pmid')
                    europePMCIterator('result', 'pmcid')
                    europePMCIterator('result', 'doi')
                    europePMCIterator('result', 'title')
                    europePMCIterator('result', 'authorString')
                    europePMCIterator('journalInfo', 'issue', 'journal_issue')
                    europePMCIterator('journalInfo', 'volume', 'journal_volume')
                    europePMCIterator('journalInfo', 'journalIssueId')
                    europePMCIterator('journalInfo', 'dateOfPublication', 'journal_dateOfPublication')
                    europePMCIterator('journalInfo', 'monthOfPublication', 'journal_monthOfPublication')
                    europePMCIterator('journalInfo', 'yearOfPublication', 'journal_yearOfPublication')
                    europePMCIterator('journalInfo', 'printPublicationDate', 'journal_printPublicationDate')
                    europePMCIterator('journal', 'title', 'journal_title')
                    europePMCIterator('journal', 'ISOAbbreviation', 'journal_ISOAbbreviation')
                    europePMCIterator('journal', 'medlineAbbreviation', 'journal_medlineAbbreviation')
                    europePMCIterator('journal', 'NLMid', 'journal_NLMid')
                    europePMCIterator('journal', 'ISSN', 'journal_ISSN')
                    europePMCIterator('journal', 'ESSN', 'journal_ESSN')
                    europePMCIterator('result', 'pubYear')
                    europePMCIterator('result', 'pageInfo')
                    europePMCIterator('result', 'abstractText')
                    europePMCIterator('result', 'affiliation')
                    europePMCIterator('result', 'publicationStatus')
                    europePMCIterator('result', 'language')
                    europePMCIterator('result', 'pubModel')
                    europePMCIterator('pubType', tag_renamed='pubTypeList', mode='multiple')
                    europePMCIterator('keyword', tag_renamed='keywords', mode='multiple')
                    europePMCIterator('result', 'isOpenAccess')
                    europePMCIterator('result', 'inEPMC')
                    europePMCIterator('result', 'inPMC')
                    europePMCIterator('result', 'hasPDF')
                    europePMCIterator('result', 'hasBook')
                    europePMCIterator('result', 'hasSuppl')
                    europePMCIterator('result', 'citedByCount')
                    europePMCIterator('result', 'hasData')
                    europePMCIterator('result', 'hasReferences')
                    europePMCIterator('result', 'hasTextMinedTerms') 
                    europePMCIterator('result', 'hasDbCrossReferences')
                    europePMCIterator('result', 'hasLabsLinks')  
                    europePMCIterator('result', 'license')  
                    europePMCIterator('result', 'hasTMAccessionNumbers')
                    europePMCIterator('accessionType', tag_renamed='tmAccessionTypeList', mode='multiple') 
                    europePMCIterator('result', 'dateOfCreation')
                    europePMCIterator('result', 'firstIndexDate')
                    europePMCIterator('result', 'fullTextReceivedDate')
                    europePMCIterator('result', 'dateOfRevision')
                    europePMCIterator('result', 'electronicPublicationDate')
                    europePMCIterator('result', 'firstPublicationDate')

                    # Build dictionary from labels and relative data
                    d = dict(zip(labels, data))  
                    empty_df.append(d)

        # Convert into dataframe
        PMC_dataframe = pd.DataFrame(empty_df).fillna("NA")
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
print(prova.PMC_dataframe(['PRJEB31610', 'PPR505492']))

#prova.runGetPublications(['PRJEB31610'])