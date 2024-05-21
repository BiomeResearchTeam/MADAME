import re
import io
import requests as rq
from Utilities import Color, LoggerManager
import time
import pandas as pd
from requests.adapters import HTTPAdapter, Retry
from user_agent import generate_user_agent
from rich import print as rich_print
from rich.console import Console
from rich.table import Table
from rich import box

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
        
        # Query 
        url = "https://www.ebi.ac.uk/ena/browser/api/tsv/textsearch?"
        headers = {"User-Agent": generate_user_agent()}

        s = rq.session()
        retries = Retry(total=5,
                        backoff_factor=0.1,
                        status_forcelist=[429, 500, 502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))
        
        getlist = s.get(url + domain + self.user_query.replace(" ", "%20"), headers=headers, allow_redirects=True)

        # String decoding for returning self.queryresult, also to be used later in QueryDetails
        self.queryresult = getlist.content.decode("utf-8", "ignore")

        # Fetch accession IDs from first column of ENA's tsv response
        queryresult_df = pd.read_csv(io.StringIO(self.queryresult), sep='\t', dtype=str)
        listOfAccessionIDs = queryresult_df['accession'].unique().tolist()

        logger = LoggerManager.log(user_session)
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

        logger = LoggerManager.log(user_session)        
        logger.debug(f"[USER-SUBMITTED-IDs]: runs[{', '.join(runs)}], samples[{', '.join(samples)}], studies[{', '.join(studies)}], projects[{', '.join(projects)}]")
        logger.debug(f"[ACCESSION-IDS-FOUND]: {listOfAccessionIDs}")

        return listOfAccessionIDs, dictionaryOfAccessionIDs

    
    def QueryDetails(self, user_session, listOfAccessionIDs, umbrella_projects=[]):
    # Prints output for the query search as a table with clickable accession links. Umbrella Projects, if present, are printed in yellow and next to the "☂" character.
           
        total_of_accessions = (len(listOfAccessionIDs))
        
        if total_of_accessions == 0:
            rich_print(f"\n  >> There are [bold red]no {self.data_type}[/bold red] for the query: '[rgb(255,0,255)]{self.user_query}[/rgb(255,0,255)]'\n")

            #logger
            logger = LoggerManager.log(user_session)
            logger.debug(f"[QUERY-DETAILS]: no {self.data_type} found")

        else:  
            rich_print(f"\n  >> For the query '[rgb(255,0,255)]{self.user_query}[/rgb(255,0,255)]', a total of [rgb(0,255,0)]{total_of_accessions}[/rgb(0,255,0)] {self.data_type} was found.\n")

            #logger
            logger = LoggerManager.log(user_session)
            logger.debug(f"[QUERY-DETAILS]: found {total_of_accessions} {self.data_type}:")

            df = pd.read_csv(io.StringIO(self.queryresult), sep='\t', dtype=str)
            table = Table(row_styles=["", "rgb(204,153,255)"], header_style="", box=box.ROUNDED)
            table.add_column("Accession", justify="left", no_wrap=True)
            table.add_column("Description", justify="left")

            for row in df.index:
                if df['accession'][row] in umbrella_projects:
                    table.add_row(f"[link=https://www.ebi.ac.uk/ena/browser/view/{df['accession'][row]}][yellow]☂ {df['accession'][row]}[/yellow][/link]", f"{df['description'][row]}")

                    #logger
                    logger.debug(f"[QUERY-DETAILS]: ☂ {df['accession'][row]} → {df['description'][row]}")

                else:
                    table.add_row(f"[link=https://www.ebi.ac.uk/ena/browser/view/{df['accession'][row]}]{df['accession'][row]}[/link]", f"{df['description'][row]}")

                    #logger
                    logger.debug(f"[QUERY-DETAILS]: {df['accession'][row]} → {df['description'][row]}")
                
            console = Console()
            console.print(table)

        return total_of_accessions

    def IDlistFromUserInputDetails(self, user_session, dictionaryOfAccessionIDs, umbrella_projects=[]):
    # Prints output for the user-submitted accessions as a table with clickable accession links. Umbrella Projects, if present, are printed in yellow and next to the "☂" character.

        results_dataframe = pd.DataFrame(columns=['accession','description'])
        request_response = [] 

        #logger
        logger = LoggerManager.log(user_session)

        def text_search(ena_domain, results_dataframe, request_response):

            # Spinner for showing MADAME is working (this process can be lenghty)
            console = Console()
            with console.status("\n⍗ Fetching details of entered accessions from ENA browser API, please wait...") as status:
                # For each accession type submitted, a different query to ENA db is needed.

                domain = f"domain={ena_domain}&query="

                # Query URL assembling. 
                url_base = "https://www.ebi.ac.uk/ena/browser/api/tsv/textsearch?"
                complete_url = url_base + domain + "%20OR%20".join(accessions)
                headers = {"User-Agent": generate_user_agent()}

                s = rq.session()
                retries = Retry(total=5,
                                backoff_factor=0.1,
                                status_forcelist=[429, 500, 502, 503, 504])
                s.mount('https://', HTTPAdapter(max_retries=retries))
                
                request = s.get(complete_url, headers=headers, allow_redirects=True)
                request_response.append(str(request.status_code))

                # String decoding
                decoded = request.content.decode("utf-8", "ignore")

                # Read the string as a pandas dataframe and merge with results_dataframe
                df = pd.read_csv(io.StringIO(decoded), sep='\t', dtype=str)
                if not df.empty:
                    results_dataframe = pd.concat([results_dataframe, df], ignore_index=True)

                    return results_dataframe
        
        # Query ENA db only if accession codes are present, check each list.
        if dictionaryOfAccessionIDs["runs"]:
            accessions = dictionaryOfAccessionIDs["runs"]
            results_dataframe = text_search("sra-run", results_dataframe, request_response)
        
        if dictionaryOfAccessionIDs["runs_range"]:
            for range in dictionaryOfAccessionIDs["runs_range"]:
                accessions = self.expand_accessions_range(range)
                results_dataframe = text_search("sra-run", results_dataframe, request_response)

        if dictionaryOfAccessionIDs["experiments"]:
            accessions = dictionaryOfAccessionIDs["experiments"]
            results_dataframe = text_search("sra-experiment", results_dataframe, request_response)

        if dictionaryOfAccessionIDs["experiments_range"]:
            for range in dictionaryOfAccessionIDs["experiments_range"]:
                accessions = self.expand_accessions_range(range)
                results_dataframe = text_search("sra-experiment", results_dataframe, request_response)

        if dictionaryOfAccessionIDs["samples"]:
            accessions = dictionaryOfAccessionIDs["samples"]
            results_dataframe = text_search("sra-sample", results_dataframe, request_response)

        if dictionaryOfAccessionIDs["samples_range"]:
            for range in dictionaryOfAccessionIDs["samples_range"]:
                accessions = self.expand_accessions_range(range)
                results_dataframe = text_search("sra-sample", results_dataframe, request_response)

        if dictionaryOfAccessionIDs["biosamples"]:
            accessions = dictionaryOfAccessionIDs["biosamples"]
            results_dataframe = text_search("sra-sample", results_dataframe, request_response)

        if dictionaryOfAccessionIDs["biosamples_range"]:
            for range in dictionaryOfAccessionIDs["biosamples_range"]:
                accessions = self.expand_accessions_range(range)
                results_dataframe = text_search("sra-sample", results_dataframe, request_response)

        if dictionaryOfAccessionIDs["studies"]:
            accessions = dictionaryOfAccessionIDs["studies"]
            results_dataframe = text_search("sra-study", results_dataframe, request_response)
        
        if dictionaryOfAccessionIDs["projects"]:
            accessions = dictionaryOfAccessionIDs["projects"]
            results_dataframe = text_search("project", results_dataframe, request_response)

        if results_dataframe.empty:
            print('Please try again\n')
            time.sleep(2)
            
        else:
            if request_response == "200":
                rich_print(f"\n  >> Details of [bold]entered accessions[/bold]:\n")

                table = Table(row_styles=["", "rgb(204,153,255)"], header_style="", box=box.ROUNDED)
                table.add_column("Accession", justify="left", no_wrap=True)
                table.add_column("Description", justify="left")

                for row in results_dataframe.index:
                    if results_dataframe['accession'][row] in umbrella_projects:
                        table.add_row(f"[link=https://www.ebi.ac.uk/ena/browser/view/{results_dataframe['accession'][row]}][yellow]☂ {results_dataframe['accession'][row]}[/yellow][/link]", f"{results_dataframe['description'][row]}")

                        #logger
                        logger.debug(f"[ACCESSION-DETAILS]: ☂ {results_dataframe['accession'][row]} → {results_dataframe['description'][row]}")

                    else:
                        table.add_row(f"[link=https://www.ebi.ac.uk/ena/browser/view/{results_dataframe['accession'][row]}]{results_dataframe['accession'][row]}[/link]", f"{results_dataframe['description'][row]}")

                        #logger
                        logger.debug(f"[ACCESSION-DETAILS]: {results_dataframe['accession'][row]} → {results_dataframe['description'][row]}")
                    
                console = Console()
                console.print(table)


    def expand_accessions_range(self, accessions_range):
        # Takes an accessions range string such as "SRR16946893-SRR16946910" as input and 
        # returns a complete list of all the accessions in the range. If the range is not valid
        # (e.g. "SRR16946893-SRR16946800") it returns an empty list.

        letters = (re.search(r'[a-zA-Z]+', accessions_range)).group(0)
        numbers = list(map(int, re.findall(r'\d+', accessions_range)))  
        accessions_range_list = ([f'{letters}{number}' for number in range(numbers[0], numbers[1]+1)])

        return accessions_range_list


GetIDlist = GetIDlist('GetIDlist') 