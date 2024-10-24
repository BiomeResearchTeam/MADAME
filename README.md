# MADAME
![madame_workflow](https://github.com/Biome-team/MADAME/assets/130676054/0283f38f-d188-4348-93ea-b98379d4c4b8)

Project overview
----------------
MADAME is a bioinformatic tool designed to facilitate and automatize data and metadata retrieval from ENA database.
This open-source user-friendly project, written in Python 3.11, enables users to enrich downloaded metadata with related publications and view the results through a report before downloading data. With its flexible workflow, MADAME helps users save time and resources.

MADAME has 4 principal FUNCTIONS:

* METADATA RETRIEVAL

* PUBLICATIONS RETRIEVAL

* REPORT GENERATION

* DATA RETRIEVAL

Installation instructions in a nutshell
-------------------------
Please look at __TUTORIAL.md__ file in this GitHub page for a step-by-step installation and example usage.

**1. DOWNLOAD Python 3:**

https://www.python.org/

\
**2. DOWNLOAD MADAME:**

From the [GitHub Docs page](https://docs.github.com/en/repositories/working-with-files/using-files/downloading-source-code-archives#downloading-source-code-archives-from-the-repository-view):

**3. DOWNLOAD enaBrowserTools:**

From the [enaBrowserTools GitHub page](https://github.com/enasequence/enaBrowserTools/tree/master):
Download [here](https://github.com/enasequence/enaBrowserTools/releases/latest) the latest release of enaBrowserTools and extract it to the preferred location on your computer. Navigate to enaBrowserTools folder. Now that you're inside the enaBrowserTools, give permissions to the folder containing scripts:
```
chmod 777 python3/
```
If you are using a Unix/Linux or Mac computer, we suggest you add the following command to your .bashrc file, where INSTALLATION_DIR is the location where you have saved the enaBrowserTools.
```
#enaBrowserTools
export PATH=$PATH:INSTALLATION_DIR/enaBrowserTools/python3
```
As last step, you need to compile the `enaBT_path.txt` in MADAME folder with the path of enaBrowserTools, like this:
```
INSTALLATION_DIR/enaBrowserTools/
```
\
**3. INSTALL EXTERNAL LIBRARIES:**

To install external libraries open a terminal (prompt for windows users) and navigate to the MADAME folder with the following:
```
cd path/to/MADAME
```
or for Windows users:
```
cd path\to\MADAME (windows-users)
```
\
Now that you are inside the MADAME folder, if you are a conda user (best option), run the following command:
```
conda env create -f requirements.yml
```

How to run MADAME
------------------
Open a terminal and go to the MADAME directory by running the entire path:

Linux and Mac:
```
cd path/to/MADAME  
```
Windows (prompt):
```
cd path\to\MADAME
```
Now that you are in the right directory, run the following command to start:
```
python main_madame.py
```
Operating instructions
----------------------

**Where do you want to work?**

Choose if you want to create a new folder inside MADAME/Downloads or use an already existing folder inside MADAME/Downloads. MADAME will download the results in the folder you indicated. 

**Which module do you want to use?**

MADAME

 1 - Metadata retrievement module: metadata search and download \
 2 - Publication retrievement module: metadata- and data- associated publications download \
 3 - Report module: explore metadata and publication retrivement outputs \
 4 - Data retrievement module: metadata-associated data download

**Module 1 - Metadata retrievement module: metadata search and download** \
Starting from a text query, or an accession list, or a file (CSV or TSV format) MADAME allows to fetch and download experiment and sample metadata as files in TSV format.

**Module 2 - Publication retrievement module: metadata- and data- associated publications download** \
Using the merged experiment metadata file from the previous module as input, MADAME searches for the related publications in ENA and in Europe PMC. The output is the found publications metadata in TSV format. 

**Module 3 - Report module: explore metadata and publication retrievement outputs** \
Starting from the merged experiment metadata file of the Module 1 and (optionally) the merged publications metadata file of the Module 2, MADAME allows users to visualize the downloaded metadata through the generation of a report. The report consists of plots and tables that users can also find in the "Report_images" folder as single plot in PNG format and single tables in XLSX format.

**Module 4 - Data retrievement module: metadata-associated data download** \
The merged experiment metadata file of the Module 1 is used as input to fetch and download data from ENA. As this module uses enaBrowserTools, it is necessary for users to have previously downloaded it. MADAME enables users to download data in FASTQ, SRA or SUBMITTED format.

Contacts
-----------------------------------------------------
* Name: __Sara Fumagalli__
* e-mail: __sara.fumagalli@unimib.it__

Credits and acknowledgments
---------------------------
* __Giulia Soletta__
* __Giulia Agostinetto__
