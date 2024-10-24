MADAME step-by-step tutorial and example usage
=======

Please, for any doubt or issue, contact us through github issue messages or sending an e-mail to sara.fumagalli@unimib.it

Before starting
---------------------
Install MADAME following these steps:
1. Download Python 3 if you haven’t already at https://www.python.org/
2. Download MADAME:
    * Download [ZIP](https://github.com/Biome-team/MADAME/archive/refs/heads/master.zip) from MADAME GitHub home page, then decompress it\
    or 
    * Use git from command line: `git clone https://github.com/Biome-team/MADAME`

3. We suggest to install Conda or Miniconda - here you can find how to install Miniconda3: https://conda.io/projects/conda/en/latest/user-guide/install/index.html

4. Once Miniconda is installed, create the conda environment with the command below:
```
conda create -f requirements.yml
```
5. Download EnaBrowserTools:
Download [here](https://github.com/enasequence/enaBrowserTools/releases/latest) the latest release of enaBrownserTools and extract it to the preferred location on your computer. Navigate to enaBrowserTools folder. Now that you're inside the enaBrowserTools, give permissions to the folder containing scripts:
```
chmod 777 python3/
```
If you are using a Linux or Mac computer, add the following command to your `.bashrc` file, where INSTALLATION_DIR is the location where you have saved the enaBrowserTools.
```
#enaBrowserTools
export PATH=$PATH:INSTALLATION_DIR/enaBrowserTools/python3
```
As last step, you need to compile the `enaBT_path.txt` in MADAME folder with the path of enaBrowserTools, like this:
```
INSTALLATION_DIR/enaBrowserTools/
```

Run MADAME
---------------------

Activate the conda environment with:
```
conda activate madame
```

Run the script below to run the tool:
```
python main_madame.py
``` 

MADAME asks you to choose the folder where you want to work. MADAME will download the results of your work there.
![madame_2](https://github.com/Biome-team/MADAME/assets/130676054/561cb8e3-45b3-408d-b5e2-33a67d256956)

Now you are in the main menu. A new session must start with the Module 1 because its output is the input of all the other modules. Note that you can change the folder where you are working.
![madame_3](https://github.com/Biome-team/MADAME/assets/130676054/1d45f00a-2697-4d38-8e20-55d771c0c953)
-->**To follow the tutorial, digit 1**

Module 1 - Metadata retrievement module: metadata search and download
---------------------
Choose which input method you prefer
![madame_4](https://github.com/Biome-team/MADAME/assets/130676054/c50c73bb-bd47-46a7-a35e-634534ecaff9)
-->**To follow the tutorial, digit 1**

Digit the text query and choose between projects, runs, experiments, samples or studies
![madame_5](https://github.com/Biome-team/MADAME/assets/130676054/f6c41dfe-d6d7-4dba-b82a-da4ae9f53a8e)
-->**To follow the tutorial, digit naval microbiome and then projects**

Let's see what MADAME found:
![madame_6](https://github.com/Biome-team/MADAME/assets/130676054/b141946f-7c60-472e-bed2-f6f50bd6018a)
-->**Press enter**

Choose which metadata you want to download
![madame_7](https://github.com/Biome-team/MADAME/assets/130676054/cb16c297-938d-4607-81ed-8bce04498dab)
-->**To follow the tutorial, digit 1**

Here the download:
![madame_8](https://github.com/Biome-team/MADAME/assets/130676054/42c8cf5c-135c-4150-97c3-ff12b882d186)
-->**Press enter to go to main menu**

Module 2 - Publications retrievement module: publications and related metadata search
---------------------

Now digit 2 to start publication retrieval module
![madame_3](https://github.com/Biome-team/MADAME/assets/130676054/d107aa7a-c14b-430b-b2c6-e321ea43fefd)

Indicate where `merged experiment metadata` is in your computer. The option 2 allows the user to use a `merged experiment metadata` that has been previously moved from MADAME/Downloads/GitHub. This can happen if the user wanted to explore or manipulate the metadata file outside the MADAME folder
![madame_9](https://github.com/Biome-team/MADAME/assets/130676054/2994521d-0f2e-4821-bdac-b3df686d1565)
-->**To follow the tutorial, digit 1**

And see the results:
![madame_10](https://github.com/Biome-team/MADAME/assets/130676054/242cf5e5-5d3e-4412-8aef-f1f4d1d1479f)
-->**Press enter to go to main menu**

Module 3 - Report generation module: metadata visualization
---------------------

Now digit 3 to visualize what we downloaded in the previous modules:
![madame_3](https://github.com/Biome-team/MADAME/assets/130676054/d107aa7a-c14b-430b-b2c6-e321ea43fefd)

For the generation of the report only the `merged experiment metadata` (from the Module 1) is needed. However user can also submit `merged publications metadata` to MADAME in order to expande the number of plots generated. Furthermore, user can submit files present in different location of his computer.
![madame_11](https://github.com/Biome-team/MADAME/assets/130676054/ecc2d3d4-f706-4627-a0c9-be1bf142b1f4)
-->**To follow the tutorial, digit 1**

Here the results:
![madame_12](https://github.com/Biome-team/MADAME/assets/130676054/dd21f363-1a77-4e81-b725-3c9983daea8d)

Let's see some plots:
1) Scatter plot of projects size
![madame_16](https://github.com/Biome-team/MADAME/assets/130676054/16ba8314-ab93-4e25-b361-33e4da4fa785)

2) Word map of publications based on author's affiliation. This is an example of plot that MADAME can generate only if the merged publications metadata is given as input
![madame_17](https://github.com/Biome-team/MADAME/assets/130676054/4ff5da6c-6d03-454d-9ea9-d628ccb0e33f)

3) Wordcloud of the titles of the publications found. Another example of plot that MADAME can generate only if the merged publications metadata is given as input
![madame_18](https://github.com/Biome-team/MADAME/assets/130676054/f75d6706-4672-4574-9bff-e62f1192251b)

4) Donut chart of scientific name
![madame_19](https://github.com/Biome-team/MADAME/assets/130676054/5a5502b7-023a-4519-b5db-69404b538326)

5) Bar chart of library source
![madame_20](https://github.com/Biome-team/MADAME/assets/130676054/0136244a-3436-466d-b407-e25b48f7904c)

Module 4 - Data retrievement module: data search and download
---------------------

Finally digit 4 for data download
![madame_3](https://github.com/Biome-team/MADAME/assets/130676054/d107aa7a-c14b-430b-b2c6-e321ea43fefd)

Choose the input file:
![madame_13](https://github.com/Biome-team/MADAME/assets/130676054/aebf6242-6ecd-4397-a8e7-d9d4cce7f624)
-->**To follow the tutorial, digit 1**

And now choose the data format:
![madame_14](https://github.com/Biome-team/MADAME/assets/130676054/6d2ee97b-e96c-4045-aa15-0ed934eea836)
-->**To follow the tutorial, digit fastq**

MADAME calculates your free space and asks if you want to continue:
![madame_15](https://github.com/Biome-team/MADAME/assets/130676054/98292ec9-fea2-459d-a76e-d2845253a22e)
-->**We digited yes**


At the end this is what GitHub folder includes:
- a folder for each project found
- the `listOfAccessionIDs.tsv` from Module 1 which include the list of accession found and available on ENA
- the `merged experiment metadata` from Module 1 (which derived from the merge of experiment metadata of all projects found)
- the `merged publications metadata` from Module 2 (which derived from the merge of publication metadata of all projects found)
- the HTML report
- the report images folder
- a log file with all the choices made by users and possible issues 
![madame_21](https://github.com/Biome-team/MADAME/assets/130676054/d86c8013-da99-4faa-b15a-29c14080ad1a)


This is how a project folder looks like:
- the `project-metadata.xml` from Module 1
- the `experiment metadata` from Module 1
- the folder `samples-metadata_xml` which MADAME parses from Module 1 into `parsed-samples-metadata.tsv`
- the `publications metadata` from Module 2
- data folder from Module 4
![madame_22](https://github.com/Biome-team/MADAME/assets/130676054/76a5767f-e3da-4bce-98cc-4c9a93534209)


The data folder includes data organized into run folders:
![madame_23](https://github.com/Biome-team/MADAME/assets/130676054/fb30e555-f510-4f34-a4d9-f2f15e131c74)

Ok our work is finished here. Bye!!
![madame_24](https://github.com/Biome-team/MADAME/assets/130676054/607beaeb-4e7e-4440-adcd-d64093c3aa6e)
