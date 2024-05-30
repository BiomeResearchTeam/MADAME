from user_agent import generate_user_agent
import xml.etree.ElementTree as ET
import requests as rq
from requests.adapters import HTTPAdapter, Retry
import pandas as pd
import os
import re
from rich.progress import track
from io import StringIO
from Utilities import Color, Utilities, LoggerManager
from IDlist import GetIDlist
from rich import print as rich_print
from rich.console import Console
from rich.panel import Panel


# Class for finding publications from sequences' accessions.
# It returns one .tsv dataframe for each input accession.
class GetPublications:
    def __init__(self, name):
        self.name = name 

    def runGetPublications(self, listOfProjectIDs, e_df, user_session):
    # For each project ID, reads from the already downloaded experiments metadata file and
    # creates a list of all the accessions in it. The list of accessions plus the project ID 
    # are given as input to GetPublicatios.PMC_dataframe, which returns a list of dictionaries
    # after querying each accession. This list of dictionaries, if not empty, is converted to
    # a pandas dataframe and then saved as a .tsv file to the corresponding project directory.

        projects_with_no_publication = []  
        umbrella_projects = []
        user_choice = False

        # Check if there's umbrella projects in merged experiment metadata
        if 'umbrella_project' in e_df.columns:

            # Spinner for showing MADAME is working (this process can be lenghty)
            console = Console()
            with console.status("\n☂ Checking for Umbrella Projects, please wait...") as status:
            
                # List of all umbrella projects in e_df, filtered to remove empty strings
                umbrella_projects = list(filter(None, e_df['umbrella_project'].unique().tolist()))

                # List of all component projects in e_df
                component_projects = {}

                for projectID in umbrella_projects:
                    components = e_df.loc[e_df['umbrella_project'] == f'{projectID}', 'study_accession'].unique().tolist()
                    component_projects[projectID] = components

                component_projects_list = [component for components in list(component_projects.values()) for component in components]

                # List of not umbrella and not component projects
                listOfProjectIDs = e_df.loc[e_df['umbrella_project'] == '', 'study_accession'].unique().tolist()

                # List of umbrella + not umbrella projects, without all the component projects
                listOfProjectIDs_full = listOfProjectIDs + umbrella_projects
            
            # logger
            logger = LoggerManager.log(user_session)
            logger.debug(f"[FOUND-UMBRELLA-PROJECTS]: {umbrella_projects}")

            # Print warning to console
            session_name = str(user_session).split('/')[1]
            rich_print(f"\n[yellow]WARNING[/yellow] - {session_name}_merged_experiments-metadata.tsv contains [rgb(0,255,0)]{len(listOfProjectIDs_full)}[/rgb(0,255,0)] projects, but [rgb(0,255,0)]{len(umbrella_projects)}[/rgb(0,255,0)] of them are [yellow]UMBRELLA projects[/yellow]:")
   
            # Print details about each umbrella (read experiment metadata online).
            # → Project IDs are clickable

            for projectID in component_projects:

                if len(component_projects[projectID]) == 1:
                    rich_print(f"[yellow]☂[/yellow] [link=https://www.ebi.ac.uk/ena/browser/view/{projectID}]{projectID}[/link] → [rgb(0,255,0)]{len(component_projects[projectID])}[/rgb(0,255,0)] component project")

                    # logger
                    logger = LoggerManager.log(user_session)
                    logger.debug(f"[UMBRELLA-PROJECT]: {projectID} → {len(component_projects[projectID])} component project")

               
                else: 
                    rich_print(f"[yellow]☂[/yellow] [link=https://www.ebi.ac.uk/ena/browser/view/{projectID}]{projectID}[/link] → [rgb(0,255,0)]{len(component_projects[projectID])}[/rgb(0,255,0)] component projects")

                    # logger
                    logger = LoggerManager.log(user_session)
                    logger.debug(f"[UMBRELLA-PROJECT]: {projectID} → {len(component_projects[projectID])} component projects")

            # Print info box and let the user decide how to proceed
            print()
            console = Console()
            box = console.print(Panel(("Instead of holding data, umbrella projects group together multiple component projects that are part of the same research motivation or collaboration.\n→ Each umbrella can contain [yellow]a few to thousands[/yellow] of other projects, and this [yellow]can significantly prolong[/yellow] the publication research.\nMore info on [link=https://ena-docs.readthedocs.io/en/latest/retrieval/ena-project.html]ENA's documentation[/link]."), title=(":umbrella: Umbrella Projects - Info Box"), border_style= "rgb(255,255,0)", padding= (0,1), title_align="left"))

            rich_print("\n  [rgb(255,0,255)]1[/rgb(255,0,255)] - Exclude umbrella projects\n  [rgb(255,0,255)]2[/rgb(255,0,255)] - Include umbrella projects")

            while True:
                    
                user_choice = input("\n  >> How do you want to proceed? Enter your option: ")
                if user_choice.isnumeric():
                    user_choice = int(user_choice)
                    if user_choice not in (1, 2):
                        rich_print("[bold red]Error[/bold red], enter a valid choice!")
                        continue
                    break
                else:
                    print("[bold red]Error[/bold red], expected a numeric input. Try again.\n")


            # Proceed excluding umbrella projects
            if user_choice == 1:            
                listOfProjectIDs = listOfProjectIDs

                # logger
                logger = LoggerManager.log(user_session)
                logger.debug(f"[OPTION-1]: - EXCLUDE UMBRELLA PROJECTS")

            # Proceed including umbrella projects  
            if user_choice == 2:            

                # logger
                logger = LoggerManager.log(user_session)
                logger.debug(f"[OPTION-2]: - INCLUDE UMBRELLA PROJECTS")

                listOfProjectIDs = listOfProjectIDs_full   


        # Queries loop
        print()
        for projectID in track(listOfProjectIDs, description="Searching for publications..."):

            path = os.path.join(user_session, projectID) 
            publications_metadata = os.path.join(path, f'{projectID}_publications-metadata.tsv')
            if os.path.isfile(publications_metadata):
                # Print different message whether the project is an umbrella or not
                if projectID in umbrella_projects:
                    rich_print(f'[yellow]☂[/yellow] {projectID}_publications-metadata.tsv [rgb(0,255,0)]already exist![/rgb(0,255,0)]')
                    #logger
                    logger = LoggerManager.log(user_session)
                    logger.debug(f"[GET-PUBLICATIONS]: ☂ {projectID}_publications-metadata.tsv already exist!")
                else:
                    rich_print(f'{projectID}_publications-metadata.tsv [rgb(0,255,0)]already exist![/rgb(0,255,0)]')
                    #logger
                    logger = LoggerManager.log(user_session)
                    logger.debug(f"[GET-PUBLICATIONS]: {projectID}_publications-metadata.tsv already exist!")

            else:
                # Project ID is an umbrella
                if projectID in umbrella_projects: 

                    umbrella_dataframe_list = []

                    #Search publication for the umbrella project ID
                    u_accessions_list = self.ENA_Xref_check(projectID)          
                    umbrella_dataframe = self.PMC_pd_dataframe(e_df, projectID, u_accessions_list, user_session, umbrella = True)
                    umbrella_dataframe_list.append(umbrella_dataframe)

                    #Search publication for each component of the umbrella
                    components = component_projects[projectID]

                    for component in components:
                        c_accessions_list = self.ENA_Xref_check(component)          
                        component_dataframe = self.PMC_pd_dataframe(e_df, component, c_accessions_list, user_session, umbrella = projectID, component = True, components = components, umbrella_dataframe_list = umbrella_dataframe_list)
                        if not component_dataframe.empty:
                            umbrella_dataframe_list.append(component_dataframe)

                    #Merge all obtained dataframes in a single dataframe and add the umbrella_project column
                    PMC_pd_dataframe = pd.concat(umbrella_dataframe_list).reset_index(drop=True)
                    PMC_pd_dataframe['umbrella_project'] = f'{projectID}'

                # Project ID is not an umbrella
                else:
                    accessions_list = self.ENA_Xref_check(projectID)          
                    PMC_pd_dataframe = self.PMC_pd_dataframe(e_df, projectID, accessions_list, user_session)  
                
                if PMC_pd_dataframe.empty:   

                    if projectID in umbrella_projects:
                        rich_print(f'[b red]No publications[/b red] were found for [yellow]☂[/yellow] {projectID}')
                        #logger
                        logger = LoggerManager.log(user_session)
                        logger.debug(f"[GET-PUBLICATIONS]: No publications were found for ☂ {projectID}")
                    else:
                        rich_print(f'[b red]No publications[/b red] were found for {projectID}')
                        #logger
                        logger = LoggerManager.log(user_session)
                        logger.debug(f"[GET-PUBLICATIONS]: No publications were found for {projectID}")


                    projects_with_no_publication.append(projectID)
                    if not os.path.exists(path):
                        os.mkdir(path) 
                    with open(os.path.join(path, f'{projectID}_publications-metadata.tsv'), 'w') as file:  
                        file.write("")  

                else:
                    if os.path.exists(path):
                        PMC_pd_dataframe.to_csv(os.path.join(path, f'{projectID}_publications-metadata.tsv'), sep="\t", index=False) 
                    else:
                        os.mkdir(path)
                        PMC_pd_dataframe.to_csv(os.path.join(path, f'{projectID}_publications-metadata.tsv'), sep="\t", index=False) 
                    logger = LoggerManager.log(user_session)
                    logger.debug(f"[GET-PUBLICATIONS]: Publications metadata was downloaded as {projectID}_publications-metadata.tsv")
                    print(Color.BOLD + Color.GREEN + 'Publications metadata was downloaded' + Color.END, f'as {projectID}_publications-metadata.tsv')  
                
            
    def ENA_Xref_check(self, projectID):
        # Given a projectID, checks with the ENA Xref API if the project has any linked publications.
        # It returns a list of accessions (PubMed primary accessions) which will be used by PMC_pd_dataframe
        # function. Only if the returned list is empty (no linked publications in ENA Xref API), the 
        # PMC_pd_dataframe function will search for every accession linked to the project. 
        
        ## source https://stackoverflow.com/questions/15431044/can-i-set-max-retries-for-requests-request
        s = rq.session()
        retries = Retry(total=6,
                        backoff_factor=0.1,
                        status_forcelist=[429, 500, 502, 503, 504])
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
        df = pd.read_csv(data, sep='\t', dtype=str, keep_default_na=False) #keep_default_na=False is for avoiding pandas adding .0 to numbers
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

    def PMC_pd_dataframe(self, e_df, projectID, accessions_list, user_session, umbrella = False, component = False, components = [], umbrella_dataframe_list = []):

        s = rq.session()
        retries = Retry(total=6,
                        backoff_factor=0.1,
                        status_forcelist=[429, 500, 502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        # dict_list will be filled with a dictionary of labels and values for each publication found.   
        dict_list = [] 

        # Fetching merged_metadata file and building the accessions list, only if it's None
        # (so if it's not provided by ENA_Xref_check)
        if not accessions_list:

            e_df['grouping_col'] = e_df['study_accession']
            e_df.loc[e_df['grouping_col'].isna(), 'grouping_col'] = e_df['secondary_study_accession']
            metadata_df = e_df.loc[e_df['grouping_col'] == projectID]   
            # experiments_metadata = os.path.join(user_session, projectID, f'{projectID}_experiments-metadata.tsv')
            # metadata_df = pd.read_csv(experiments_metadata, sep='\t')
            accessions_columns = ['study_accession', 'secondary_study_accession', 'sample_accession', 'secondary_sample_accession', 'experiment_accession', 'run_accession', 'submission_accession']
            accessions_list = []
                
            for column in accessions_columns:
                accessions = metadata_df[column].unique().tolist()
                # clean list from nan values
                accessions = [x for x in accessions if str(x) != 'nan']
                # split merged ids, if present
                for accession in accessions:
                    if ";" in accession:
                        splitted_accessions = accession.split(";")
                        # remove every instance of accession inside accessions list
                        accessions = [i for i in accessions if i != accession] 
                        accessions.extend(splitted_accessions)

                accessions_list.extend(accessions)

            # Remove duplicates
            accessions_list = list(dict.fromkeys(accessions_list))
        
        for queried_accession_id in accessions_list:

            # Print message and counter according to project ID type
            if umbrella == True:
                rich_print(f"[yellow]☂[/yellow] {projectID}: querying {queried_accession_id} ({accessions_list.index(queried_accession_id)+1}/{len(accessions_list)})")
            elif component == True:
                rich_print(f"[yellow]☂[/yellow] {umbrella} → component project {projectID} ({components.index(projectID)+1}/{len(components)}): querying {queried_accession_id} ({accessions_list.index(queried_accession_id)+1}/{len(accessions_list)})")
            else:
                rich_print(f"{projectID}: querying {queried_accession_id} ({accessions_list.index(queried_accession_id)+1}/{len(accessions_list)})") 

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
                        if any(d.get('id') == pub_id for d in dict_list) and not umbrella_dataframe_list:

                            #logger
                            logger = LoggerManager.log(user_session)
                            logger.debug(f"[GET-PUBLICATIONS]: {projectID} → {queried_accession_id} returned publication with id {pub_id}. ALREADY FOUND, SKIPPING")

                            break

                        # Check for umbrella projects loop: if the unique article identifier "id" it's already in any of the dataframes in umbrella_dataframe_list; if it is, skip to the next query without parsing anything.

                        elif umbrella_dataframe_list and any(pub_id in df["id"].values for df in [df for df in umbrella_dataframe_list if not df.empty]):

                            #logger
                            logger = LoggerManager.log(user_session)
                            logger.debug(f"[GET-PUBLICATIONS]: ☂ {umbrella} → component project {projectID} → {queried_accession_id} returned publication with id {pub_id}. ALREADY FOUND, SKIPPING")

                            break

                        else:
                            
                            # Log according to project ID type
                            if umbrella == True:
                                #logger
                                logger = LoggerManager.log(user_session)
                                logger.debug(f"[GET-PUBLICATIONS]: ☂ {projectID} → {queried_accession_id} returned publication with id {pub_id}.")
                            elif component == True:
                                #logger
                                logger = LoggerManager.log(user_session)
                                logger.debug(f"[GET-PUBLICATIONS]: ☂ {umbrella} → component project {projectID} → {queried_accession_id} returned publication with id {pub_id}.")
                            else:
                                #logger
                                logger = LoggerManager.log(user_session)
                                logger.debug(f"[GET-PUBLICATIONS]: {projectID} → {queried_accession_id} returned publication with id {pub_id}.")
                        

                        # Project ID column
                        labels.append("project_id")
                        data.append(projectID)

                        # Queried accession, associated with input accession
                        labels.append("queried_accession_id")
                        data.append(queried_accession_id)

                        # Parse a selected list of fields with EPMC_tree_parser function.

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
    #does not support umbrella projects at the moment.
    #FUNCTION NOT INCLUDED IN THE PIPELINE! 

        for projectID in track(listOfProjectIDs, description="Getting text mined terms..."):      
            # Fetching local publications metadata file 
            publications_metadata = os.path.join(user_session, projectID, f'{projectID}_publications-metadata.tsv')

            if os.path.isfile(publications_metadata):
                metadata_df = pd.read_csv(publications_metadata, sep='\t', dtype=str)
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
                                        status_forcelist=[429, 500, 502, 503, 504])
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
                    dataframes.append(pd.read_csv(tsv_path, sep='\t', dtype=str).loc[:, 'project_id':])

            # stop if dataframes list is empty
            if not dataframes:
                print(f"\nError: couldn't create {user_session}_merged_publications-metadata.tsv: " + Color.BOLD + Color.RED + "no publications-metadata.tsv file found." + Color.END) 
                return

            merged_dataframe = pd.concat(dataframes).reset_index(drop=True)

            # Drop extra column 'Unnamed 0' if it exists
            if 'Unnamed: 0' in merged_dataframe.columns:
                merged_dataframe = merged_dataframe.drop('Unnamed: 0', axis=1)

            merged_dataframe.to_csv(os.path.join(user_session, f'{os.path.basename(user_session)}_merged_publications-metadata.tsv'), sep="\t", index=False)
            print("\n>>>"+ Color.BOLD + Color.GREEN + " DOWNLOAD PUBLICATIONS METADATA COMPLETED! " + Color.END + "<<<")
            print('You can find the', Color.UNDERLINE + f'{os.path.basename(user_session)}_merged_publications-metadata.tsv' + Color.END, 
                'here:', Color.BOLD + Color.YELLOW + f'{user_session}' + Color.END)
            logger = LoggerManager.log(user_session)
            logger.debug(f"[GET-PUBLICATIONS]: {os.path.basename(user_session)}_merged_publications-metadata.tsv created")
              

GetPublications = GetPublications('GetPublications')

