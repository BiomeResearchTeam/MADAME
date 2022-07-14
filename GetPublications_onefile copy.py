import xml.etree.ElementTree as ET
import requests as rq
from user_agent import generate_user_agent
import time
import pandas as pd
import os



class GetPublications:
    def __init__(self, name):
        self.name = name 

    def runGetPublications(self, listOfProjectIDs):
              
        dict_list = []

        for projectID in listOfProjectIDs:
           
            experiments_metadata = f'{projectID}.tsv'
            metadata_df = pd.read_csv(experiments_metadata, sep='\t')
            accessions_columns = ['study_accession', 'secondary_study_accession', 'sample_accession', 'secondary_sample_accession', 'experiment_accession', 'run_accession', 'submission_accession']
            accessions_list = []
            
            for column in accessions_columns:
                accessions = metadata_df[column].unique().tolist()
                accessions_list.extend(accessions)

            print(f"now working on {projectID}, project {listOfProjectIDs.index(projectID)+1} out of {len(listOfProjectIDs)}")
            
            dictionary_list = self.PMC_dataframe(accessions_list, input_accession_id=projectID) 
            dict_list.extend(dictionary_list)
            
        
        PMC_dataframe = pd.DataFrame(dict_list).fillna("NA")   
        PMC_dataframe.to_csv('df3_publications-metadata.tsv', sep="\t") 
        print("done!")
        
          


    def PMC_dataframe(self, accessions_list, input_accession_id=None):     

        dict_list = []  
        rq.adapters.DEFAULT_RETRIES = 5 
        s = rq.session()
        s.keep_alive = False    

          


        for queried_accession_id in accessions_list:
            print(f"now querying {queried_accession_id}, id {accessions_list.index(queried_accession_id)+1} out of {len(accessions_list)}")

            query = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={queried_accession_id}&format=xml&resultType=core"
            headers = {"User-Agent": generate_user_agent()}
            response = s.get(query, headers=headers).content
            
            tree = ET.fromstring(response)
            
            for hit in tree.iter('responseWrapper'):
                hitcount = int(hit.find('hitCount').text)
                if hitcount == 0:
                    break

                else:                    
                    labels = []
                    data = []

                    for children in tree.iter("result"):

                        def EPMC_tree_parser(tag_or_XPath, tag_name = None, mode = None):
                            
                            if mode == None:    
                                
                                if tag_name:
                                    labels.append(tag_name)
                                else:
                                    labels.append(tag_or_XPath)
                                
                                child = children.find(tag_or_XPath)
                                if child is not None:
                                    value = child.text                 
                                    data.append(value)
                                else:
                                    data.append("NA") 
                                    
                            if mode == "value_list":

                                labels.append(tag_name)
                                
                                value_list = []
                                for single_value in children.findall(tag_or_XPath):
                                    str = single_value.text
                                    value_list.append(str)
                                if value_list:
                                    values = ';'.join(value_list) 
                                    data.append(values)
                                else:
                                    data.append("NA")

                        pub_id = children.find("id").text

                        if any(d.get('id') == pub_id for d in dict_list):
                            break

                        if input_accession_id is not None:
                            labels.append("input_accession_id")
                            data.append(input_accession_id)

                        labels.append("queried_accession_id")
                        data.append(queried_accession_id)

                        EPMC_tree_parser('id')
                        EPMC_tree_parser('source')
                        EPMC_tree_parser('pmid')
                        EPMC_tree_parser('pmcid')
                        EPMC_tree_parser('./fullTextIdList/fullTextId', 'fullTextIdList', mode='value_list')
                        EPMC_tree_parser('doi')
                        EPMC_tree_parser('title')
                        EPMC_tree_parser('authorString')
                        EPMC_tree_parser('./journalInfo/issue', 'journal_issue')
                        EPMC_tree_parser('./journalInfo/volume', 'journal_volume')
                        EPMC_tree_parser('./journalInfo/journalIssueId', 'journalIssueId')
                        EPMC_tree_parser('./journalInfo/dateOfPublication', 'journal_dateOfPublication')
                        EPMC_tree_parser('./journalInfo/monthOfPublication', 'journal_monthOfPublication')
                        EPMC_tree_parser('./journalInfo/yearOfPublication', 'journal_yearOfPublication')
                        EPMC_tree_parser('./journalInfo/printPublicationDate', 'journal_printPublicationDate')
                        EPMC_tree_parser('./journalInfo/journal/title', 'journal_title')
                        EPMC_tree_parser('./journalInfo/journal/ISOAbbreviation', 'journal_ISOAbbreviation')
                        EPMC_tree_parser('./journalInfo/journal/medlineAbbreviation', 'journal_medlineAbbreviation')
                        EPMC_tree_parser('./journalInfo/journal/NLMid', 'journal_NLMid')
                        EPMC_tree_parser('./journalInfo/journal/ISSN', 'journal_ISSN')
                        EPMC_tree_parser('./journalInfo/journal/ESSN', 'journal_ESSN')
                        EPMC_tree_parser('pubYear')
                        EPMC_tree_parser('pageInfo')
                        EPMC_tree_parser('abstractText')
                        EPMC_tree_parser('affiliation')
                        EPMC_tree_parser('publicationStatus')
                        EPMC_tree_parser('language')
                        EPMC_tree_parser('pubModel')
                        EPMC_tree_parser('./pubTypeList/pubType', 'pubTypeList', mode='value_list')
                        EPMC_tree_parser('./keywordList/keyword', 'keywordList', mode='value_list')
                        EPMC_tree_parser('isOpenAccess')
                        EPMC_tree_parser('inEPMC')
                        EPMC_tree_parser('inPMC')
                        EPMC_tree_parser('hasPDF')
                        EPMC_tree_parser('hasBook')
                        EPMC_tree_parser('hasSuppl')
                        EPMC_tree_parser('citedByCount')
                        EPMC_tree_parser('hasData')
                        EPMC_tree_parser('hasReferences')
                        EPMC_tree_parser('hasTextMinedTerms') 
                        EPMC_tree_parser('hasDbCrossReferences')
                        EPMC_tree_parser('hasLabsLinks')  
                        EPMC_tree_parser('license')  
                        EPMC_tree_parser('hasTMAccessionNumbers')
                        EPMC_tree_parser('./tmAccessionTypeList/accessionType', 'tmAccessionTypeList', mode='value_list') 
                        EPMC_tree_parser('dateOfCreation')
                        EPMC_tree_parser('firstIndexDate')
                        EPMC_tree_parser('fullTextReceivedDate')
                        EPMC_tree_parser('dateOfRevision')
                        EPMC_tree_parser('electronicPublicationDate')
                        EPMC_tree_parser('firstPublicationDate')


                        # Getting HTML and PDF links

                        list_of_links = {}
                        for node in children.findall("./fullTextUrlList/fullTextUrl"):
                            documentStyle = node.find("documentStyle")
                            if documentStyle is not None:
                                style = documentStyle.text
                                url = node.find("url").text
                                list_of_links[style] = url
                        
                     
                            if "html" in list_of_links:
                                labels.append("HTML")
                                data.append(list_of_links["html"])
                            if "pdf" in list_of_links:
                                labels.append("PDF")
                                data.append(list_of_links["pdf"])

                                #PDF size
                                response = s.head(list_of_links["pdf"], headers=headers, allow_redirects=True)
                                is_chunked = response.headers.get('transfer-encoding', '') == 'chunked'
                                content_length_s = response.headers.get('content-length')

                                if not is_chunked and content_length_s.isdigit():
                                    pdf_bytes = int(content_length_s)
                                else:
                                    pdf_bytes = "NA"
                            
                                labels.append("PDF_bytes")
                                data.append(pdf_bytes)


                        # Getting fulltext XML links
                        fullTextIdList_index = labels.index("fullTextIdList")
                        fullTextIdList = data[fullTextIdList_index]
                        if fullTextIdList != "NA":
                            IdList = fullTextIdList.split(";")
                            fulltextXML_links = []
                            for id in IdList:
                                link = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{id}/fullTextXML"
                                fulltextXML_links.append(link)
                            
                            labels.append("fulltextXML")
                            data.append(';'.join(fulltextXML_links))


                        # Getting supplementaries links
                        hasSuppl_index = labels.index("hasSuppl")
                        hasSuppl = data[hasSuppl_index]
                        if fullTextIdList != "NA" and hasSuppl == "Y":
                            suppl_links = []
                            for id in IdList:
                                suppl = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{id}/supplementaryFiles?includeInlineImage=yes"
                                suppl_links.append(suppl)
                            
                            labels.append("Suppl")
                            data.append(';'.join(suppl_links))
                        
                        
                        # Getting TGZ package link
                        pmcid_index = labels.index("pmcid")
                        pmcid = data[pmcid_index]
                        if pmcid != "NA":
            
                            tgz_xml = f"https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id={pmcid}" 
                            response = s.get(tgz_xml, headers=headers).content
                            tree = ET.fromstring(response)
                            records = tree.find('records')

                            if records is not None:
                                tgz = tree.find(".//*[@format='tgz']")                                    
                                tgz_download_link = tgz.get('href').replace("ftp://", "http://")

                                labels.append("TGZpackage")
                                data.append(tgz_download_link)

                                # TGZ package size
                                response = s.head(tgz_download_link, headers=headers, allow_redirects=True)
                                is_chunked = response.headers.get('transfer-encoding', '') == 'chunked'
                                content_length_s = response.headers.get('content-length')

                                if not is_chunked and content_length_s.isdigit():
                                    tgz_bytes = int(content_length_s)
                                else:
                                    tgz_bytes = "NA"

                                labels.append("TGZpackage_bytes")
                                data.append(tgz_bytes)


                        # Build dictionary from labels and relative data
                        dictionary = dict(zip(labels, data))      
                        dict_list.append(dictionary)

                    print(dict_list)

        return dict_list

        


#os.chdir("/mnt/c/Users/conog/Desktop")
#listOfProjectIDs = [os.path.splitext(filename)[0] for filename in os.listdir("/mnt/c/Users/conog/Desktop/DF3_METADATA")]
prova = GetPublications("a")
#prova.runGetPublications(listOfProjectIDs)

os.chdir("/mnt/c/Users/conog/Desktop")
prova.PMC_dataframe(["ERP005182"])








# prova = GetPublications("a")
# idlist = prova.runGetPublications(["PRJNA719282"])
# print("idlist lenght:", len(idlist))
# queries = []

# index = 0
# string = idlist[index]

# #while index <= len(idlist)-2:
# for id in idlist[index+1:]:
#     if len(string) + len('%20OR%20') + len(id) <= 1959:
#         string = string + '%20OR%20' + id
#         index = idlist.index(id)
#     else:
#         string = string
#         query = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={string}&format=xml&resultType=core"
#         queries.append(query)
#         print("last index:", index)
#         print("query lenght:", len(query), "/ 2048")
#         break

# print(queries)




