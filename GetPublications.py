from user_agent import generate_user_agent
import xml.etree.ElementTree as ET
import requests as rq
from requests.adapters import HTTPAdapter, Retry
import pandas as pd
import os
from rich.progress import track
from io import StringIO
from Utilities import Color, Utilities  #---> RICH


# Class for finding publications from sequences' accessions.
# It returns one .tsv dataframe for each input accession.
class GetPublications:
    def __init__(self, name):
        self.name = name 

    def runGetPublications(self, listOfProjectIDs, user_session):
    # For each project ID, reads from the already downloaded experiments metadata file and
    # creates a list of all the accessions in it. The list of accessions plus the project ID 
    # are given as input to GetPublicatios.PMC_dataframe, which returns a list of dictionaries
    # after querying each accession. This list of dictionaries, if not empty, is converted to
    # a pandas dataframe and then saved as a .tsv file to the corresponding project directory.

        projects_with_no_publication = []   # Is it useful?

        for projectID in track(listOfProjectIDs, description="Searching for publications..."):
            path = os.path.join(user_session, projectID)  #modificato da sara: tolto download perché già inserito in publication module
            publications_metadata = os.path.join(path, f'{projectID}_publications-metadata.tsv')
            if os.path.isfile(publications_metadata):
                logger = Utilities.log("GetPublications", user_session)
                logger.debug(f"{projectID}_publications-metadata.tsv already exist!")
                print(f'{projectID}_publications-metadata.tsv', Color.BOLD + Color.GREEN + 'already exist!' + Color.END)

            else:
                accessions_list = self.ENA_Xref_check(projectID)          
                PMC_pd_dataframe = self.PMC_pd_dataframe(projectID, accessions_list, path)  
                
                if PMC_pd_dataframe.empty:   
                    logger = Utilities.log("GetPublications", user_session)
                    logger.debug(f"No publications were found for {projectID}")
                    print(Color.BOLD + Color.RED +"No publications" + Color.END, f" were found for {projectID}")
                    projects_with_no_publication.append(projectID)
                    with open(os.path.join(path, f'{projectID}_publications-metadata.tsv'), 'w') as file:  
                        file.write("")  

                else:
                    PMC_pd_dataframe.to_csv(os.path.join(path, f'{projectID}_publications-metadata.tsv'), sep="\t") 
                    logger = Utilities.log("GetPublications", user_session)
                    logger.debug(f"Publications metadata was downloaded as {projectID}_publications-metadata.tsv")
                    print(Color.BOLD + Color.GREEN + 'Publications metadata was downloaded' + Color.END, f'as {projectID}_publications-metadata.tsv')  
                
            

    def ENA_Xref_check(self, projectID):
        # Given a projectID, checks with the ENA Xref API if the project has any linked publications.
        # It returns a list of accessions (PubMed primary accessions) which will be used by PMC_pd_dataframe
        # function. Only if the returned list is empty (no linked publications in ENA Xref API), the 
        # PMC_pd_dataframe function will search for every accession linked to the project. 
        
        ## TO TEST ###### https://stackoverflow.com/questions/15431044/can-i-set-max-retries-for-requests-request
        s = rq.session()
        retries = Retry(total=6,
                        backoff_factor=0.1,
                        status_forcelist=[500, 502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        # Create an empty accessions_list
        accessions_list = []
        # Check projectID with ENA Xref API:
        ENA_Xref_url = f"https://www.ebi.ac.uk/ena/xref/rest/tsv/search?accession={projectID}"
        # a random user-agent is generated for each query
        headers = {"User-Agent": generate_user_agent()}
        response = s.get(ENA_Xref_url, headers=headers)
        data = StringIO(response.text)

        # Read dataframe online:
        df = pd.read_csv(data, sep='\t', keep_default_na=False) #keep_default_na=False is for avoiding pandas adding .0 to numbers
        # If df is empty, return accessions_list as it is (empty)
        if df.empty:
            return accessions_list

        EuropePMC_rows = df[df['Source'] == "EuropePMC"]
        if df.empty: 
            pass
        else:
            accessions = EuropePMC_rows['Source secondary accession'].unique().tolist()
            accessions_list.extend(accessions)
    
        PubMed_rows = df[df['Source'] == "PubMed"]
        if df.empty: 
            pass
        else:
            accessions = PubMed_rows['Source primary accession'].unique().tolist()
            accessions_list.extend(accessions)
        
        accessions_list = list(dict.fromkeys(accessions_list)) #removing any possible duplicates

        return accessions_list 

    def PMC_pd_dataframe(self, projectID, accessions_list, path):
       
        ## TO TEST ###### https://stackoverflow.com/questions/15431044/can-i-set-max-retries-for-requests-request
        s = rq.session()
        retries = Retry(total=6,
                        backoff_factor=0.1,
                        status_forcelist=[500, 502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        # dict_list will be filled with a dictionary of labels and values for each publication found.   
        dict_list = [] 

        # Fetching local metadata file and building the accessions list, only if it's None
        # (so if it's not provided by ENA_Xref_check)
        if not accessions_list:
            experiments_metadata = os.path.join(path, f'{projectID}_experiments-metadata.tsv')
            metadata_df = pd.read_csv(experiments_metadata, sep='\t')
            accessions_columns = ['study_accession', 'secondary_study_accession', 'sample_accession', 'secondary_sample_accession', 'experiment_accession', 'run_accession', 'submission_accession']
            accessions_list = []
            
            for column in accessions_columns:
                accessions = metadata_df[column].unique().tolist()
                accessions_list.extend(accessions)
        
      
        for queried_accession_id in accessions_list:
            print(f"{projectID}: querying {queried_accession_id} ({accessions_list.index(queried_accession_id)+1}/{len(accessions_list)})") # come sovrascrivere la precedente linea printata?
            #capire come renderlo utile per user (queried accession id è inutile da sapere per uno user)  

            query = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={queried_accession_id}&format=xml&resultType=core" 
            # a random user-agent is generated for each query
            headers = {"User-Agent": generate_user_agent()}
            response = s.get(query, headers=headers).content
            
            # Parsing response XML 
            tree = ET.fromstring(response)
            
            for hit in tree.iter('responseWrapper'):
                hitcount = int(hit.find('hitCount').text)
                # if hitcount = 0, there's no publication. 
                # Skip to the next accession
                if hitcount == 0:
                    break

                else:   

                    # Each <result> tag corresponds to an article 
                    for children in tree.iter("result"):

                        # Create "labels" and "data" lists for storing parsed articles metadata              
                        labels = []
                        data = []

                        def EPMC_tree_parser(tag_or_XPath, tag_name = None, mode = None):
                        # Custom ElementTree parser. Takes a tag or an XPath as input, an optional 
                        # custom name for renaming the tag (it will be the column name in the pandas
                        # dataframe) and an optional mode: None or value_list.

                        # Mode = None fetches data from XML structures like this: <TAG> DATA </TAG>
                        # Mode = value_list fetches data from XML structures like this:
                        # <TAG>        
                        #   <TAG> DATA </TAG>
                        #   <TAG> DATA </TAG>
                        # </TAG>
                        # and joins all data fields with a ';' separator.

                            
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
                                    if str:
                                        value_list.append(str)
                                if value_list:
                                    values = ';'.join(value_list) 
                                    data.append(values)
                                else:
                                    data.append("NA")

                        # Check: if the unique article identifier "id" it's already in dict_list,
                        # skip to the next query, without parsing anything.
                        pub_id = children.find("id").text
                        if any(d.get('id') == pub_id for d in dict_list):
                            break

                        # Project ID column
                        labels.append("project_id")
                        data.append(projectID)

                        # Queried accession, associated with input accession
                        labels.append("queried_accession_id")
                        data.append(queried_accession_id)

                        # Parse a selected list of fields with EPMC_tree_parser function.

                        # DA DECIDERE COSA TENERE:
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


                        # Get HTML and PDF links. 
                        list_of_links = {}
                        for node in children.findall("./fullTextUrlList/fullTextUrl"):
                            documentStyle = node.find("documentStyle")
                            if documentStyle is not None:
                                style = documentStyle.text
                                url = node.find("url").text
                                list_of_links[style] = url  

                        labels.append("DOI")
                        if "doi" in list_of_links: 
                            data.append(list_of_links["doi"])
                        else:
                            data.append("NA")
                
                        labels.append("HTML")
                        if "html" in list_of_links: 
                            data.append(list_of_links["html"])
                        else:
                            data.append("NA")

                        labels.append("PDF")
                        if "pdf" in list_of_links:
                            data.append(list_of_links["pdf"])
                        else:
                            data.append("NA")



                        # Get fulltext XML link(s)
                        fullTextIdList_index = labels.index("fullTextIdList")
                        fullTextIdList = data[fullTextIdList_index]
                        isOpenAccess_index = labels.index("isOpenAccess")
                        isOpenAccess = data[isOpenAccess_index]

                        labels.append("fulltextXML")
                        if fullTextIdList != "NA" and isOpenAccess =="Y":
                            IdList = fullTextIdList.split(";")
                            fulltextXML_links = []
                            for id in IdList:
                                link = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{id}/fullTextXML"
                                fulltextXML_links.append(link)
                            data.append(';'.join(fulltextXML_links))
                        else:
                            data.append("NA")


                        # Get supplementaries link(s)
                        hasSuppl_index = labels.index("hasSuppl")
                        hasSuppl = data[hasSuppl_index]

                        labels.append("Suppl")
                        if fullTextIdList != "NA" and hasSuppl == "Y" and isOpenAccess =="Y":
                            suppl_links = []
                            for id in IdList:
                                suppl = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{id}/supplementaryFiles?includeInlineImage=yes"
                                suppl_links.append(suppl)
                            data.append(';'.join(suppl_links))
                        else:
                            data.append("NA")
                        
                        
                        # Get TGZ package link
                        pmcid_index = labels.index("pmcid")
                        pmcid = data[pmcid_index]

                        labels.append("TGZpackage")
                        if pmcid != "NA" and isOpenAccess =="Y":
            
                            tgz_xml = f"https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id={pmcid}" 
                            response = s.get(tgz_xml, headers=headers).content
                            tree = ET.fromstring(response)
                            records = tree.find('records')

                            if records is not None:
                                tgz = tree.find(".//*[@format='tgz']")                                    
                                tgz_download_link = tgz.get('href').replace("ftp://", "http://")

                                data.append(tgz_download_link)

                        else:
                            data.append("NA")


                        # Build a dictionary from labels and data, append it to dict_list
                        dictionary = dict(zip(labels, data))  
                        dict_list.append(dictionary)
            

        if len(dict_list) == 0:
            PMC_pd_dataframe = pd.DataFrame(dict_list) 
        else:
            PMC_pd_dataframe = pd.DataFrame(dict_list).fillna("NA")
            
        
        return PMC_pd_dataframe

    def getTextMinedTerms(self, listOfProjectIDs, user_session):

        for projectID in track(listOfProjectIDs, description="Getting text mined terms..."):      
            # Fetching local publications metadata file 
            publications_metadata = os.path.join(user_session, projectID, f'{projectID}_publications-metadata.tsv') #mod da sara: rimosso download

            if os.path.isfile(publications_metadata):
                metadata_df = pd.read_csv(publications_metadata, sep='\t')
                metadata_df_filtered = metadata_df.loc[metadata_df["hasTextMinedTerms"] == "Y"]

                if len(metadata_df_filtered.columns) != 0:
                    article_ids = []
                    for id_list in metadata_df_filtered['fullTextIdList'].unique().tolist():
                        ids = id_list.split(";")
                        article_ids.extend(ids)

                    for article_id in article_ids: 
                        source = article_id[:3]
                        external_id = article_id[3:]
                        url = f"https://www.ebi.ac.uk/europepmc/annotations_api/annotationsByArticleIds?articleIds={source}:{external_id}&format=XML"

                        s = rq.session()
                        retries = Retry(total=5,
                                        backoff_factor=0.1,
                                        status_forcelist=[500, 502, 503, 504])
                        s.mount('https://', HTTPAdapter(max_retries=retries))
                        headers = {"User-Agent": generate_user_agent()}
                        response = s.get(url, headers=headers).content

                        dict_list = []

                        tree = ET.fromstring(response)
                        for children in tree.iter("annotation"):

                            # Create "labels" and "data" lists for storing parsed articles metadata              
                            labels = []
                            data = []

                            def tmt_tree_parser(tag_or_XPath, tag_name = None):
                            # Custom ElementTree parser. Takes a tag or an XPath as input and an optional 
                            # custom name for renaming the tag (it will be the column name in the pandas
                            # dataframe). 

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

                            labels.append("article_id")
                            data.append(article_id)

                            tmt_tree_parser("prefix") 
                            tmt_tree_parser("exact")
                            tmt_tree_parser("postfix")
                            tmt_tree_parser("./tags/tag/name", "tag_name")
                            tmt_tree_parser("./tags/tag/uri", "tag_uri")
                            tmt_tree_parser("id")
                            tmt_tree_parser("type")
                            tmt_tree_parser("section")
                            tmt_tree_parser("provider")

                            dictionary = dict(zip(labels, data))  
                            dict_list.append(dictionary)

                        text_mined_terms_dataframe = pd.DataFrame(dict_list)
                        text_mined_terms_dataframe.to_csv(os.path.join(user_session, projectID, f'{projectID}_{article_id}_text-mined-terms.tsv'), sep="\t") #mod da sara: rimosso download
                        print(f'Text mined terms saved as {projectID}_{article_id}_text-mined-terms.tsv')  

                     
                else:
                    print(f"No {projectID} publication has text mined terms available.")

            else:
                print(f"{projectID}_publications-metadata.tsv not found. Either {projectID} has no associated publication or you didn't download this file yet.")
            


    def mergePublicationsMetadata(self, user_session):

            #path = user_session #mod da sara: rimosso download
            dataframes = []

            for dir in os.listdir(user_session): #mod sara: prima era path
                    tsv = f'{dir}_publications-metadata.tsv'
                    tsv_path = os.path.join(user_session, dir, tsv) #mod sara: prima era path
                    if os.path.isfile(tsv_path) and os.path.getsize(tsv_path) > 0:
                        dataframes.append(pd.read_csv(tsv_path, sep='\t').loc[:, 'project_id':])

            # stop if dataframes list is empty
            if not dataframes:
                print(f"\nError: couldn't create {user_session}_merged_publications-metadata.tsv: " + Color.BOLD + Color.RED + "no publications-metadata.tsv file found." + Color.END)   ####messaggio da rivedere
                return

            merged_dataframe = pd.concat(dataframes)
            merged_dataframe.to_csv(os.path.join(user_session, f'{os.path.basename(user_session)}_merged_publications-metadata.tsv'), sep="\t") #mod sara: prima era path, aggiunto os.path.basaname

            # print(f'{user_session}_merged_publications-metadata.tsv' + Color.BOLD + Color.GREEN +  #silenziato da sara
            #     ' successfully created' + Color.END)

            # return


  
    def download_publications(self, listOfProjectIDs):

        ######DA SCRIVERE#######

        return
              

GetPublications = GetPublications('GetPublications')