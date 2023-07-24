import re
import io
import requests as rq
from Utilities import Color, Utilities
import time
import pandas as pd

# Class for getting the ID list from query or user input/file and for printing accessions details

class GetIDlist:
    # Class attributes - single accession
    RUNS_PATTERN =  r'(?<!\S)[E|D|S]RR[0-9]{6,}(?!\d|\S)'
    EXPERIMENTS_PATTERN = r'(?<!\S)[E|D|S]RX[0-9]{6,}(?!\d|\S)'
    SAMPLES_PATTERN = r'(?<!\S)[E|D|S]RS[0-9]{6,}(?!\d|\S)'
    BIOSAMPLES_PATTERN = r'(?<!\S)SAM[E|D|N][A-Z]?[0-9]+(?!\d|\S)'
    STUDIES_PATTERN = r'(?<!\S)[E|D|S]RP[0-9]{6,}(?!\d|\S)'
    PROJECTS_PATTERN = r'(?<!\S)PRJ[E|D|N][A-Z][0-9]+(?!\d|\S)'

    # Class attributes - accessions range
    RUNS_RANGE_PATTERN = r'(?<!\S)([E|D|S])RR[0-9]{6,}-\1RR[0-9]{6,}(?!\d|\S)'
    EXPERIMENTS_RANGE_PATTERN = r'(?<!\S)([E|D|S])RX[0-9]{6,}-\1RX[0-9]{6,}(?!\d|\S)'
    SAMPLES_RANGE_PATTERN = r'(?<!\S)([E|D|S])RS[0-9]{6,}-\1RS[0-9]{6,}(?!\d|\S)'
    BIOSAMPLES_RANGE_PATTERN = r'(?<!\S)(SAM[E|D|N][A-Z]?)[0-9]+-\1[0-9]+(?!\d|\S)'
    
 
    def __init__(self, name): 
        self.name = name
    
    
    def Query(self, user_session, user_query, data_type = "projects"):
    # Query EBI db. Default data_type is "projects".
    # It can also be set to: "runs", "samples", "studies".

        self.user_query = user_query
        self.data_type = data_type

        # Setting parameters - based on user's input
        if self.data_type == "runs":
            domain = "domain=sra-run&query="
        elif self.data_type == "experiments":
            domain = "domain=sra-experiment&query="
        elif self.data_type == "samples":
            domain = "domain=sra-sample&query="
        elif self.data_type == "studies":
            domain = "domain=sra-study&query="
        elif self.data_type == "projects":
            domain = "domain=project&query="
        
        # Query URL assembly
        url = "https://www.ebi.ac.uk/ena/browser/api/tsv/textsearch?"
        getlist = rq.get(url + domain + self.user_query.replace(" ", "%20"), allow_redirects=True)

        # String decoding for returning self.queryresult, also to be used later in QueryDetails
        self.queryresult = getlist.content.decode("utf-8", "ignore")

        # Fetch accession IDs from first column of ENA's tsv response
        queryresult_df = pd.read_csv(io.StringIO(self.queryresult), sep='\t')
        listOfAccessionIDs = queryresult_df['accession'].unique().tolist()

        logger = Utilities.log("IDlist", user_session)
        logger.debug(f'[QUERY-ON-ENA]: "{user_query}" - {data_type}')
        logger.debug(f"[ACCESSION-IDS-FOUND]: {listOfAccessionIDs}")

        return listOfAccessionIDs


    def IDlistFromUserInput(self, user_session, user_input):

    # Check the accession codes derived from user input or file. 
    # -> input list must be a clean one (no duplicates, whitespaces, nonetype)
    # Returns: 1) a list of valid accessions, checked with regex patterns
    #          2) a dictionary of accessions separated by type, for logger and printing details purposes
    # Prints appropriate errors message for invalid accessions

        # Single accession lists
        runs = []
        experiments = []
        samples = []
        biosamples = []  
        studies = []
        projects = []

        # Accessions range lists
        runs_range = []
        experiments_range = []
        samples_range = []
        biosamples_range = []
        
        # Invalid accessions lists
        not_valid_single = []
        not_valid_range = []
        not_valid_range_pattern = r'^[a-zA-Z0-9]+-[a-zA-Z0-9]+$' # checked last, it is still written as a range but the string didn't match any of the specified patterns.

        for accession in user_input:

            # Single accession (check against regex)
            if re.match(GetIDlist.RUNS_PATTERN, accession):
                runs.append(accession)
            elif re.match(GetIDlist.EXPERIMENTS_PATTERN, accession):
                experiments.append(accession)
            elif re.match(GetIDlist.SAMPLES_PATTERN, accession):
                samples.append(accession)
            elif re.match(GetIDlist.BIOSAMPLES_PATTERN, accession):
                biosamples.append(accession)
            elif re.match(GetIDlist.STUDIES_PATTERN, accession):
                studies.append(accession)
            elif re.match(GetIDlist.PROJECTS_PATTERN, accession):
                projects.append(accession)

            # Accessions range (two checks: regex, expand_accessions_range function)
            elif re.match(GetIDlist.RUNS_RANGE_PATTERN, accession):
                if self.expand_accessions_range(accession):
                    runs_range.append(accession)
                else:
                    not_valid_range.append(accession)
            elif re.match(GetIDlist.EXPERIMENTS_RANGE_PATTERN, accession):
                if self.expand_accessions_range(accession):
                    experiments_range.append(accession)
                else:
                    not_valid_range.append(accession)
            elif re.match(GetIDlist.SAMPLES_RANGE_PATTERN, accession):
                if self.expand_accessions_range(accession):
                    samples_range.append(accession)
                else:
                    not_valid_range.append(accession)
            elif re.match(GetIDlist.BIOSAMPLES_RANGE_PATTERN, accession):
                if self.expand_accessions_range(accession):
                    biosamples_range.append(accession)
                else:
                    not_valid_range.append(accession)
            
            elif re.match(not_valid_range_pattern, accession):
                not_valid_range.append(accession)
            else: 
                not_valid_single.append(accession)
                
        # Print appropriate error message, if necessary, and give the user time to read it and then proceed
        if not_valid_single and len(not_valid_single) == 1:
            print(f"\nWARNING - {not_valid_single} is" + Color.BOLD + Color.RED + " not a valid accession code" + Color.END)
        
        if not_valid_single and len(not_valid_single) > 1:
            print(f"\nWARNING - These accession codes are" + Color.BOLD + Color.RED + " not valid" + Color.END + ":")
            print(not_valid_single)

        if not_valid_range and len(not_valid_range) == 1:
            print(f"\nWARNING - {not_valid_range} is" + Color.BOLD + Color.RED + " not a valid accessions range" + Color.END)

        if not_valid_range and len(not_valid_range) > 1:
            print(f"\nWARNING - These accessions ranges are" + Color.BOLD + Color.RED + " not valid" + Color.END + ":")
            print(not_valid_range)

        # Give time to read the warnings  
        if not_valid_single or not_valid_range:
            input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")
        
        dictionaryOfAccessionIDs = {"runs" : runs, "experiments" : experiments, "samples" : samples, "biosamples" : biosamples, "studies" : studies, "projects" : projects, "runs_range" : runs_range, "experiments_range" : experiments_range, "samples_range" : samples_range, "biosamples_range" : biosamples_range}

        listOfAccessionIDs = runs+experiments+samples+biosamples+studies+projects+runs_range+experiments_range+samples_range+biosamples_range

        logger = Utilities.log("IDlist", user_session)        
        logger.debug(f"[USER-SUBMITTED-IDs]: runs[{', '.join(runs)}], samples[{', '.join(samples)}], studies[{', '.join(studies)}], projects[{', '.join(projects)}]")
        logger.debug(f"[ACCESSION-IDS-FOUND]: {listOfAccessionIDs}")

        return listOfAccessionIDs, dictionaryOfAccessionIDs

    
    def QueryDetails(self, user_session, listOfAccessionIDs):
    # Prints output for the query search. Has to be called after GetIDlist.Query()
           
        total_of_accessions = (len(listOfAccessionIDs))
        
        if total_of_accessions == 0:
            print(f"\n  >> There are " + Color.BOLD + Color.RED + f"no {self.data_type}" 
            + Color.END, f"for the query: '{self.user_query}'\n")
            logger = Utilities.log("IDlist", user_session)
            logger.debug(f"[QUERY-DETAILS]: no {self.data_type} found")

        else:
            print(f"\n  >> For the query '{self.user_query}', a total of " + Color.BOLD + Color.GREEN + f"{total_of_accessions} {self.data_type}" + Color.END, f"was found:\n{self.queryresult}")
            logger = Utilities.log("IDlist", user_session)
            logger.debug(f"[QUERY-DETAILS]: found {total_of_accessions} {self.data_type}:")
            for line in self.queryresult.split("\n"):
                if line != "" or "accession\tdescription":
                    logger.debug(f"[QUERY-DETAILS]: {line}")


    def IDlistFromUserInputDetails(self, dictionaryOfAccessionIDs):
    #Prints output for the user-submitted accessions. Has to be called after GetIDlist.IDlistFromUserInput()
        results = []

        def text_search(ena_domain):
            # For each accession type submitted, a different query to ENA db is needed.
            # Then, all results (without the first line) are joined together and printed.
            domain = f"domain={ena_domain}&query="
            # Query URL assembling. 
            url_base = "https://www.ebi.ac.uk/ena/browser/api/tsv/textsearch?"
            complete_url = url_base + domain + "%20OR%20".join(accessions)

            ####
            print("!!!URL=", complete_url)
            ####
            
            request = rq.get(complete_url, allow_redirects=True)
            # String decoding
            converted = request.content.decode("utf-8", "ignore").split("\n")[1:-1]
            results.extend(converted)
        
        # Query ENA db only if accession codes are present, check each list.
        if dictionaryOfAccessionIDs["runs"]:
            accessions = dictionaryOfAccessionIDs["runs"]
            text_search("sra-run")
        
        if dictionaryOfAccessionIDs["runs_range"]:
            for range in dictionaryOfAccessionIDs["runs_range"]:
                accessions = self.expand_accessions_range(range)
                text_search("sra-run")

        if dictionaryOfAccessionIDs["experiments"]:
            accessions = dictionaryOfAccessionIDs["experiments"]
            text_search("sra-experiment")

        if dictionaryOfAccessionIDs["experiments_range"]:
            for range in dictionaryOfAccessionIDs["experiments_range"]:
                accessions = self.expand_accessions_range(range)
                text_search("sra-experiment")

        if dictionaryOfAccessionIDs["samples"]:
            accessions = dictionaryOfAccessionIDs["samples"]
            text_search("sra-sample")

        if dictionaryOfAccessionIDs["samples_range"]:
            for range in dictionaryOfAccessionIDs["samples_range"]:
                accessions = self.expand_accessions_range(range)
                text_search("sra-sample")

        if dictionaryOfAccessionIDs["biosamples"]:
            accessions = dictionaryOfAccessionIDs["biosamples"]
            text_search("sra-sample")

        if dictionaryOfAccessionIDs["biosamples_range"]:
            for range in dictionaryOfAccessionIDs["biosamples_range"]:
                accessions = self.expand_accessions_range(range)
                text_search("sra-sample")

        if dictionaryOfAccessionIDs["studies"]:
            accessions = dictionaryOfAccessionIDs["studies"]
            text_search("sra-study")
        
        if dictionaryOfAccessionIDs["projects"]:
            accessions = dictionaryOfAccessionIDs["projects"]
            text_search("project")

        if len(results) == 0:
            print('Please try again\n')
            time.sleep(2)
            
        else:
            joined_results = "\n".join(results)
            print("\n" + Color.BOLD + "Details of entered accessions:" + Color.END 
            + f"\naccession\tdescription\n{joined_results}")


    def expand_accessions_range(self, accessions_range):
        # Takes an accessions range string such as "SRR16946893-SRR16946910" as input and 
        # returns a complete list of all the accessions in the range. If the range is not valid
        # (e.g. "SRR16946893-SRR16946800") it returns an empty list.


        letters = (re.search(r'[a-zA-Z]+', accessions_range)).group(0)
        numbers = list(map(int, re.findall(r'\d+', accessions_range)))  
        accessions_range_list = ([f'{letters}{number}' for number in range(numbers[0], numbers[1]+1)])

        return accessions_range_list


GetIDlist = GetIDlist('GetIDlist') 