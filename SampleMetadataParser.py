import os
import pandas as pd
import xml.etree.ElementTree as ET
from rich.progress import track
from Utilities import Color

# Class for parsing sample metadata (from xml to tsv) using ElementTree.

class SampleMetadataParser:

    def __init__(self, name):
        self.name = name
    
    
    def runParseMetadata(self, listOfProjectIDs, user_session):
    # For each projectID in listOfProjectIDs, enters the project folder,
    # runs the parser on samples-metadata_xml's files, exits to main folder.
    # WARNING : it needs a list of the AVAILABLE PROJECTS (IDlist.getAvailableProjects(listOfProjectIDs))
        for projectID in track(listOfProjectIDs, description="Parsing samples metadata files..."):

            #### aggiungere altre info sul processo?
            path = os.path.join("Downloads", user_session, projectID)

            # Pass if .tsv parsed file already exists
            if os.path.isfile(os.path.join(path, f'{projectID}_parsed-samples-metadata.tsv')):
                pass 

            else:      
                self.sampleMetadataParser(user_session, projectID)

        print("Parsing was " + Color.BOLD + Color.GREEN + "successfully completed\n" + Color.END)


    def sampleMetadataParser(self, user_session, projectID):

        path = os.path.join("Downloads", user_session, projectID)
        ##################### CUSTOM PARSER START #####################

        def enaSampleIterator(tag_1, tag_2, tag_3=None, mode='value'): 
        # For convenience, three different options can be specified in the mode parameter,
        # each of them is processed differently. Output is appended to build 'labels' and 'data' lists.
        # Default option is 'value', there's also 'attribute' and 'couple'.

            if mode == 'value':
            # If TAG_2 exists, it will be appended to 'labels' and its value to 'data'.
            # <TAG_1>
            #     <TAG_2> VALUE </TAG_2>
            # </TAG_1>
                for children in root.iter(tag_1):
                    child = children.find(tag_2)
                    # verify if child exists, pass if it doesn't
                    if child is not None:
                        value = child.text
                        labels.append(tag_2)                  
                        data.append(value)
                    else:
                        pass
                                        
            elif mode == 'attribute':
            # If TAG_2's attribute exists, it will be appended to 'labels' and its value to 'data'.
            # <TAG_1>
            #     <TAG_2 attribute = "value"> .... </TAG_2>
            # </TAG_1>
                for attributes in root.iter(tag_1):
                    attribute = attributes.get(tag_2)
                    # verify if attribute exists, pass if it doesn't
                    if attribute is not None:
                        labels.append(tag_2)                  
                        data.append(attribute)
                    else:
                        pass
            
            elif mode == 'couple':
            # If TAG_2 exists, its VALUE_1 will be appended to 'labels' - otherwise, the string 'NA' is appended.
            # If TAG_3 exists, its VALUE_2 will be appended to 'data' - otherwise, the string 'NA' is appended.
            # <TAG_1>
            #     <TAG_2> VALUE_1 </TAG_2>
            #     <TAG_3> VALUE_2 </TAG_3>
            # </TAG_1>
                for child in root.iter(tag_1):
                    node_1 = child.find(tag_2)
                    node_2 = child.find(tag_3)
                    # verify if nodes exists, assign 'NA' if they don't
                    if node_1 is not None:
                        value_1 = node_1.text
                    else:
                        value_1 = 'NA'
                    #
                    if node_2 is not None:
                        value_2 = node_2.text
                    else:
                        value_2 = 'NA'

                    labels.append(value_1)
                    data.append(value_2)

            else:
                print("Enter a valid mode:\n•'value' (default)\n•'attribute'\n•'couple'") 

        ##################### CUSTOM PARSER END #####################

        # Build list of sample xml files, initialize empty dataframe 
        sample_xml_directory = os.path.join(path, "samples-metadata_xml")

        # Exit function if sample_xml_directory doesn't exist
        if not os.path.isdir(sample_xml_directory):
            return
         
        xml_files = os.listdir(sample_xml_directory)
        empty_df = []

        # Loops through xml files and parses them, using enaSampleIterator function for convenience.
        # 'labels' will be the first row, shared between metadata files of the same project.
        for xml in xml_files:
            tree = ET.parse(os.path.join(sample_xml_directory, xml))
            root = tree.getroot()
            labels = []
            data = []

            enaSampleIterator('SAMPLE','broker_name', mode='attribute') 
            enaSampleIterator('SAMPLE','center_name', mode='attribute')
            enaSampleIterator('IDENTIFIERS', 'PRIMARY_ID')   
            enaSampleIterator('IDENTIFIERS', 'EXTERNAL_ID')
            enaSampleIterator('IDENTIFIERS', 'SUBMITTER_ID')
            enaSampleIterator('SAMPLE', 'TITLE')
            enaSampleIterator('SAMPLE_NAME','TAXON_ID')
            enaSampleIterator('SAMPLE_NAME','SCIENTIFIC_NAME')
            enaSampleIterator('SAMPLE_NAME','COMMON_NAME')
            enaSampleIterator('SAMPLE', 'DESCRIPTION')
            enaSampleIterator('XREF_LINK', 'DB', 'ID', mode='couple')
            enaSampleIterator('SAMPLE_ATTRIBUTE', 'TAG', 'VALUE', mode='couple')

            # Build dictionary from labels and relative data
            dictionary = dict(zip(labels, data))
            empty_df.append(dictionary)

        # Convert into dataframe
        df = pd.DataFrame(empty_df)

        # Save as parsed-samples-metadata.tsv 
        df.to_csv(os.path.join(path, f"{projectID}_parsed-samples-metadata.tsv", sep='\t', index=None))

SampleMetadataParser = SampleMetadataParser("SampleMetadataParser") 