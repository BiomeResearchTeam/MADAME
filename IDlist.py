import requests as rq
import re
import sys
from Project import Project

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
    
    
    def Query(self, logger, user_query, data_type = "projects"):
    # Query EBI db. Default data_type is "projects".
    # It can also be set to: "runs", "samples", "studies".
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
        else:
            # Error message 
            print(f'❌   "{self.data_type}" is not a correct data type. Accepted data types are:')
            print('➡️  runs') 
            print('➡️  samples')
            print('➡️  studies')
            print('➡️  projects')
            print('Please try again.')
            sys.exit()
    
        # Query URL assembly
        url = "https://www.ebi.ac.uk/ena/browser/api/tsv/textsearch?"
        getlist = rq.get(url + domain + self.user_query.replace(" ", "%20"), allow_redirects=True)

        # String decoding
        self.queryresult = getlist.content.decode("utf-8", "ignore")

        # Search ID by regex pattern, resulting in listOfProjectIDs
        listOfProjectIDs = re.findall(pattern, self.queryresult)

        logger.info(f"[QUERY-RETRIEVED-IDs]: {', '.join(listOfProjectIDs)}")

        return listOfProjectIDs


    def IDlistFromUserInput(self, logger, user_input):
    # Get ID list from a series of accession codes derived from user input.
    # Accession codes needs to be entered separated by comma.
        submitted_list = user_input.split(",")

        runs = []
        samples = []
        studies = []
        projects = []
       
        for accession in submitted_list:
            if re.match(GetIDlist.PROJECTS_PATTERN, accession):
                runs.append(accession)
            elif re.match(GetIDlist.SAMPLES_PATTERN, accession):
                samples.append(accession)
            elif re.match(GetIDlist.STUDIES_PATTERN, accession):
                studies.append(accession)
            elif re.match(GetIDlist.PROJECTS_PATTERN, accession):
                projects.append(accession)
            else: 
                # Error message
                print(f'WARNING - {accession} is not a valid accession code!')

        listOfProjectIDs = {"enaDataGet" : runs, "enaGroupGet" : [samples, studies, projects]}
        # In this case the output is a dictionary, not a list!
        # Use keys and indexes to access different accession types:
        # ["enaDataGet"] ---> runs
        # ["enaGroupGet"][0] ---> samples
        # ["enaGroupGet"][1] ---> studies
        # ["enaGroupGet"][2] ---> projects

        logger.info(f"[USER-SUBMITTED-IDs]: runs[{', '.join(runs)}], samples[{', '.join(samples)}], studies[{', '.join(studies)}], projects[{', '.join(projects)}].")
        
        return listOfProjectIDs

    
    def QueryDetails(self, listOfProjectIDs):
    # Prints output for the query search. Has to be called after GetIDlist.Query()
        total_of_accessions = (len(listOfProjectIDs))

        if total_of_accessions == 0:
            output = print(f"❌   I couldn't find anything for your query: '{self.user_query}'.")
        else:
            output = print(f"✔️   For your query '{self.user_query}', I found a total of {total_of_accessions} {self.data_type}:\n{self.queryresult}")

        return output

    def IDlistFromUserInputDetails(self, listOfProjectIDs):
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
        if listOfProjectIDs["enaDataGet"]:
            domain = "domain=sra-run&query="
            accessions = listOfProjectIDs["enaDataGet"]
            text_search()

        if listOfProjectIDs["enaGroupGet"][0]:
            domain = "domain=sra-sample&query="
            accessions = listOfProjectIDs["enaGroupGet"][0]
            text_search()

        if listOfProjectIDs["enaGroupGet"][1]:
            domain = "domain=sra-study&query="
            accessions = listOfProjectIDs["enaGroupGet"][1]
            text_search()
        
        if listOfProjectIDs["enaGroupGet"][2]:
            domain = "domain=project&query="
            accessions = listOfProjectIDs["enaGroupGet"][2]
            text_search()
        
        joined_results = "\n".join(results)
        output = print(f"📑   Details of entered accessions:\naccession\tdescription\n{joined_results}")

        return output

    def getAvailableProjects(self, logger, listOfProjectIDs):
    # Input is the full list of project IDs, output is the list of the available projects.
    # This list is needed for all steps after getting a listOfProjectIDs.

        list_of_available_projects = []

        for projectID in listOfProjectIDs:
            project = Project(projectID) 
            if project.getProjectAvailability(projectID) == True:
                list_of_available_projects.append(projectID)

        listOfProjectIDs = list_of_available_projects
        logger.info(f"Available projects: {listOfProjectIDs}")

        return listOfProjectIDs
    