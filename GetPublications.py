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

            if os.path.isfile(os.path.join(projectID, f'{projectID}_publications-metadata.tsv')):
                print(f'{projectID}_publications-metadata.tsv already exist!')

            else:
                experiments_metadata = os.path.join(projectID, f'{projectID}_experiments-metadata.tsv')
                metadata_df = pd.read_csv(experiments_metadata, sep='\t')
                accessions_columns = ['study_accession', 'secondary_study_accession', 'sample_accession', 'secondary_sample_accession', 'experiment_accession', 'run_accession', 'submission_accession']
                accessions_list = []
                
                for column in accessions_columns:
                    accessions = metadata_df[column].unique().tolist()
                    for accession in accessions:
                        accessions_list.append(accession)
                
                PMC_dataframe = self.PMC_dataframe(accessions_list, input_accession_id=projectID) 

                if len(PMC_dataframe.columns) == 0:
                    print(f"🔎  Couldn't find any publications for {projectID}")

                else:
                    PMC_dataframe.to_csv(os.path.join(projectID, f'{projectID}_publications-metadata.tsv'), sep="\t") 
                    print(f'✅  Publications metadata saved as {projectID}_publications-metadata.tsv')  


    def PMC_dataframe(self, accessions_list, input_accession_id=None):
       

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


        dict_list = []      

        for queried_accession_id in accessions_list:
            query = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={queried_accession_id}&format=xml&resultType=core"
            response = urllib.request.urlopen(query).read()
            tree = ET.fromstring(response)
            
            for hit in tree.iter('responseWrapper'):
                hitcount = int(hit.find('hitCount').text)
                if hitcount == 0:
                    break

                else:                    
                    labels = []
                    data = []

                    for children in tree.iter("result"):
                        pub_id = children.find("id").text
                    if any(d.get('id') == pub_id for d in dict_list):
                        break

                    if input_accession_id is not None:
                        labels.append("input_accession_id")
                        data.append(input_accession_id)

                    labels.append("queried_accession_id")
                    data.append(queried_accession_id)

                    europePMCIterator('result', 'id')
                    europePMCIterator('result', 'source')
                    europePMCIterator('result', 'pmid')
                    europePMCIterator('result', 'pmcid')
                    europePMCIterator('fullTextId', tag_renamed='fullTextIdList', mode='multiple')
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
                    europePMCIterator('keyword', tag_renamed='keywordList', mode='multiple')
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


                    # Getting HTML and PDF links
                    list_of_links = {}

                    for node in tree.iter("fullTextUrl"):
                        documentStyle = node.find("documentStyle")
                        if documentStyle is not None:
                            style = documentStyle.text
                            url = node.find("url").text
                            list_of_links[style] = url
                       
                    if list_of_links:   #questa linea è superflua?
                        if "html" in list_of_links:
                            labels.append("HTML")
                            data.append(list_of_links["html"])
                        if "pdf" in list_of_links:
                            labels.append("PDF")
                            data.append(list_of_links["pdf"])

                            #PDF size
                            response = rq.head(list_of_links["pdf"], allow_redirects=True)
                            pdf_bytes = int(response.headers['Content-Length'])
                            labels.append("PDF_bytes")
                            data.append(pdf_bytes)
                        

                    # Getting fulltext XML links
                    index = labels.index("fullTextIdList")
                    fullTextIdList = data[index]
                    if fullTextIdList != "NA":
                        IdList = fullTextIdList.split(";")
                        fulltextXML_links = []
                        for id in IdList:
                            link = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{id}/fullTextXML"
                            fulltextXML_links.append(link)
                        
                        labels.append("fulltextXML")
                        data.append(';'.join(fulltextXML_links))
                    
                    
                    # Getting TGZ package link
                    index = labels.index("pmcid")
                    pmcid = data[index]
                    if pmcid != "NA":
                        tgz_xml = f"https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id={pmcid}" 
                        response = urllib.request.urlopen(tgz_xml).read()
                        tree = ET.fromstring(response)
                        records = tree.find('records')

                        if records is not None:
                            tgz = tree.find(".//*[@format='tgz']")                                    
                            tgz_download_link = tgz.get('href').replace("ftp://", "http://")

                            labels.append("TGZpackage")
                            data.append(tgz_download_link)

                            # TGZ package size
                            response = rq.head(tgz_download_link, allow_redirects=True)
                            tgz_bytes = int(response.headers['Content-Length'])

                            labels.append("TGZpackage_bytes")
                            data.append(tgz_bytes)


                    # Build dictionary from labels and relative data
                    dictionary = dict(zip(labels, data))  
                    dict_list.append(dictionary)

        # Convert into dataframe
        PMC_dataframe = pd.DataFrame(dict_list).fillna("NA")
        
        return PMC_dataframe










