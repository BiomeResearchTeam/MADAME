import re
import os
import sys
import requests as rq
import pandas as pd
from Utilities import Utilities, Color
import time

# Class for getting the ID list from query or user input.
# It also has methods for printing accessions' details from ENA 
# and for getting a list containing only the available projects.

class GetIDlist:
    # Class attributes
    RUNS_PATTERN =  r'([E|D|S]RR[0-9]{6,})'
    SAMPLES_PATTERN = r'([E|D|S]RS[0-9]{6,})'
    STUDIES_PATTERN = r'([E|D|S]RP[0-9]{6,})'
    PROJECTS_PATTERN = r'(PRJ[E|D|N][A-Z][0-9]+)'

    
    def __init__(self, name): 
        self.name = name
    
    
    def Query(self, logger, user_session, user_query, data_type = "projects"):
    # Query EBI db. Default data_type is "projects".
    # It can also be set to: "runs", "samples", "studies".
        path = (os.path.join("Downloads", user_session))

        self.user_query = user_query
        self.data_type = data_type


        # Setting parameters - based on user's input
        if self.data_type == "runs":
            domain = "domain=sra-run&query="
            pattern = GetIDlist.RUNS_PATTERN
        elif self.data_type == "samples":
            domain = "domain=sra-sample&query="
            pattern = GetIDlist.SAMPLES_PATTERN
        elif self.data_type == "studies":
            domain = "domain=sra-study&query="
            pattern = GetIDlist.STUDIES_PATTERN
        elif self.data_type == "projects":
            domain = "domain=project&query="
            pattern = GetIDlist.PROJECTS_PATTERN
        
    
        # Query URL assembly
        url = "https://www.ebi.ac.uk/ena/browser/api/tsv/textsearch?"
        getlist = rq.get(url + domain + self.user_query.replace(" ", "%20"), allow_redirects=True)

        # String decoding
        self.queryresult = getlist.content.decode("utf-8", "ignore")

        # Search ID by regex pattern, resulting in listOfProjectIDs
        listOfProjectIDs = re.findall(pattern, self.queryresult)

        #logger.info(f"[QUERY-RETRIEVED-IDs]: {', '.join(listOfProjectIDs)}")

        Utilities.createDirectory(path)
        list_of_IDs = pd.DataFrame({"accession_ids":listOfProjectIDs})
        list_of_IDs.to_csv(os.path.join(path, '_listOfIDs.tsv'), sep="\t", index=False)

        return listOfProjectIDs



    def IDlistFromUserInput(self, logger, user_session, user_input):

        path = (os.path.join("Downloads", user_session))
    # Get ID list from a series of accession codes derived from user input.
    # Accession codes need to be entered separated by comma.
    
        user_input = user_input.replace(" ", "")
        submitted_list = list(user_input.split(","))

    ## TO ADD: ACCEPT ACCESSION CODES FROM FILES (CSV, TSV...)

        runs = []
        samples = []
        studies = []
        projects = []
        not_valid = []
       
        for accession in submitted_list:
            if re.match(GetIDlist.RUNS_PATTERN, accession):
                runs.append(accession)
            elif re.match(GetIDlist.SAMPLES_PATTERN, accession):
                samples.append(accession)
            elif re.match(GetIDlist.STUDIES_PATTERN, accession):
                studies.append(accession)
            elif re.match(GetIDlist.PROJECTS_PATTERN, accession):
                projects.append(accession)
            else: 
                not_valid.append(accession)
                
        # Error message
        if not_valid:
            print(f"\nWARNING - {not_valid} are" + Color.BOLD + Color.RED + " not valid accession codes" + Color.END)

        dictionaryOfProjectIDs = {"runs" : runs, "samples" : samples, "studies" : studies, "projects" : projects}
        
        Utilities.createDirectory(path)
        
        listOfProjectIDs = runs+samples+studies+projects
        list_of_IDs = pd.DataFrame({"accession_ids":listOfProjectIDs})
        list_of_IDs.to_csv(os.path.join(path, '_listOfIDs.tsv'), sep="\t", index=False)
    
        #logger.info(f"[USER-SUBMITTED-IDs]: runs[{', '.join(runs)}], samples[{', '.join(samples)}], studies[{', '.join(studies)}], projects[{', '.join(projects)}].")
        
        return listOfProjectIDs, dictionaryOfProjectIDs

    
    def QueryDetails(self, listOfProjectIDs):
    # Prints output for the query search. Has to be called after GetIDlist.Query()
        total_of_accessions = (len(listOfProjectIDs))

        if total_of_accessions == 0:
            print(f"\n>> There are " + Color.BOLD + Color.RED + f"no {self.data_type}" 
            + Color.END, f"for the query: '{self.user_query}'\n")
        else:
            print(f"\n>> For the query '{self.user_query}', a total of " + Color.BOLD + Color.GREEN + f"{total_of_accessions} {self.data_type}" + Color.END, f"was found:\n{self.queryresult}")

        # add 'return output' so as to save printed details in a nice format for the log

    def IDlistFromUserInputDetails(self, dictionaryOfProjectIDs):
    #Prints output for the user-submitted accessions. Has to be called after GetIDlist.IDlistFromUserInput()
        results = []

        def text_search():
            # For each accession type submitted, a different query to ENA db is needed.
            # Then, all results (without the first line) are joined together and printed.

            # Query URL assembling. 
            url = "https://www.ebi.ac.uk/ena/browser/api/tsv/textsearch?"
            get_details = rq.get(url + domain + "%20OR%20".join(accessions), allow_redirects=True)
            # String decoding
            converted = get_details.content.decode("utf-8", "ignore").split("\n")[1:-1]
            results.extend(converted)
        
        # Query ENA db only if accession codes are present, in each list.
        if dictionaryOfProjectIDs["runs"]:
            domain = "domain=sra-run&query="
            accessions = dictionaryOfProjectIDs["runs"]
            text_search()

        if dictionaryOfProjectIDs["samples"]:
            domain = "domain=sra-sample&query="
            accessions = dictionaryOfProjectIDs["samples"]
            text_search()

        if dictionaryOfProjectIDs["studies"]:
            domain = "domain=sra-study&query="
            accessions = dictionaryOfProjectIDs["studies"]
            text_search()
        
        if dictionaryOfProjectIDs["projects"]:
            domain = "domain=project&query="
            accessions = dictionaryOfProjectIDs["projects"]
            text_search()

        if len(results) == 0:
            print('Please try again\n')
            time.sleep(2)
            
        else:
            joined_results = "\n".join(results)
            print("\n" + Color.BOLD + "Details of entered accessions:" + Color.END 
            + f"\naccession\tdescription\n{joined_results}")

        # add 'return output' so as to save printed details in a nice format for the log


GetIDlist = GetIDlist('GetIDlist') 