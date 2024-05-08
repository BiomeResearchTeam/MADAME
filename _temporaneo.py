from Utilities import Color

# BACKUP LOGO
def madame_logo():

    print("\n")
    print(Color.PURPLE + "                                                           ##############" + Color.END)
    print(Color.PURPLE + "                                                       #####################" + Color.END)       
    print(Color.PURPLE + "                                                    ##########################" + Color.END)  
    print(Color.PURPLE + "                                                  #############################" + Color.END) 
    print(Color.PURPLE + "                                                 ###############################" + Color.END) 
    print(Color.PURPLE + "                                           ####  ###############################" + Color.END) 
    print(Color.PURPLE + "                                          ######################################" + Color.END) 
    print(Color.PURPLE + "                                         #######################################" + Color.END)  
    print(Color.PURPLE + "                                         ######################################(" + Color.END)  
    print(Color.PURPLE + "                                         ########################################" + Color.END)  
    print(Color.PURPLE + "##     ##     ###     #######       ###  ###" + Color.GREEN + "##" + Color.PURPLE + "#####" + Color.GREEN + "##" + Color.PURPLE + "##" + Color.GREEN + "########" + Color.PURPLE + "##################" + Color.END)  
    print(Color.PURPLE + "###   ###    ## ##    ##    ##     ## ##  ##" + Color.GREEN + "###" + Color.PURPLE + "###" + Color.GREEN + "###" + Color.PURPLE + "##" + Color.GREEN + "##" + Color.PURPLE + "##########################" + Color.END)
    print(Color.PURPLE + "#### ####   ##   ##   ##     ##   ##   ##  #" + Color.GREEN + "####" + Color.PURPLE + "#" + Color.GREEN + "####" + Color.PURPLE + "##" + Color.GREEN + "##" + Color.PURPLE + "########################" + Color.END)
    print(Color.PURPLE + "## ### ##  ##     ##  ##     ##  ##     ##  " + Color.GREEN + "##" + Color.PURPLE + "#" + Color.GREEN + "###" + Color.PURPLE + "#" + Color.GREEN + "##" + Color.PURPLE + "##" + Color.GREEN + "######" + Color.PURPLE + "###################)" + Color.END)
    print(Color.PURPLE + "##     ##  #########  ##     ##  #########  " + Color.GREEN + "##" + Color.PURPLE + "#####" + Color.GREEN + "##" + Color.PURPLE + "##" + Color.GREEN + "##" + Color.PURPLE + "######################)" + Color.END)
    print(Color.PURPLE + "##     ##  ##     ##  ##    ##   ##     ##  " + Color.GREEN + "##     ##  ##" + Color.PURPLE + "######################" + Color.END)
    print(Color.PURPLE + "##     ##  ##     ##  #######    ##     ##  " + Color.GREEN + "##     ##  ########" + Color.PURPLE + "#######**######" + Color.END)
    print(Color.PURPLE + "                                                     ################     ***" + Color.END)
    print(Color.PURPLE + "                                                   #################" + Color.END)



# test doppie barre semplici 
def bars():
    from rich.progress import Progress
    from time import sleep

    with Progress() as pb:
        t1 = pb.add_task('inner', total=10)
        t2 = pb.add_task('outer', total=30)

        for i in range(30):
            for j in range(10):
                print(f"Verbose info! {i, j}")
                sleep(0.1)
                pb.update(task_id=t1, completed=j + 1)
            pb.update(task_id=t2, completed=i + 1)



def panel():
    from rich import print
    from rich.panel import Panel
    print(Panel("[bold center purple]DATA retrieval MODULE"))
    print("[link https://google.com]:computer: GitHub")

    from rich import print
    from rich.panel import Panel
    from rich.text import Text
    title = Panel(Text("DATA retrieval MODULE", style = "b magenta", justify="center"), style = "b magenta")
    print(title)


def prova():
    import pandas as pd
    lista1 = [1, 2, 3, 4]
    lista2 = ["pesca", "banana", "mela", "pera"]
    dic1 = {"numeri":lista1, "frutta":lista2}

    df = pd.DataFrame(dic1)


    dic2 = {"a": "b",1:"uno", 2:"due", 3:"tre", 4:"quattrr", 5:"ci"}

    df['ancora_numeri'] = 'segnaposto'

    for key in dic2.keys():
        df.loc[df['numeri'] == key, 'ancora_numeri'] = dic2[key]

    print(df)

def per_giulia_g():
    from Utilities import Utilities
    import pandas as pd
    from Project import Project

    accessions = ['PRJEB11484', 'PRJEB14474', 'PRJEB24007', 'PRJEB40938', 'PRJEB41002', 'PRJEB46174', 'PRJNA256117', 'PRJNA541082', 'PRJNA544954', 'PRJNA575544', 'PRJNA610453', 'PRJNA672813', 'PRJNA737285', 'PRJNA747635']
    sum = 0
    df = pd.read_csv("/home/gsoletta/MADAME/Downloads/giulia/giulia_merged_experiments-metadata.tsv", sep="\t")

    for id in accessions:
        bytes = Project.getProjectBytes(id, df, "fastq")
        print(id)
        print(Utilities.bytes_converter(bytes))
        sum = sum + bytes

    print("")
    print("TOTAL")
    print(Utilities.bytes_converter(sum))

import requests as rq
from requests.adapters import HTTPAdapter, Retry
from user_agent import generate_user_agent
import io
import pandas as pd
def getAccessionAvailability(accessionID):
    # Check the accession ID availability based on its metadata availability

        s = rq.session()
        retries = Retry(total=5,
                        backoff_factor=0.1,
                        status_forcelist=[429, 500, 502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        url = f"https://www.ebi.ac.uk/ena/portal/api/filereport?accession={accessionID}&result=read_run&fields=study_accession,sample_accession,experiment_accession,run_accession,tax_id,scientific_name,fastq_ftp,submitted_ftp,sra_ftp&format=tsv&download=true&limit=0"
        headers = {"User-Agent": generate_user_agent()}


        download = s.head(url, headers=headers)
        print(int(download.headers['Content-Length']))




        getAccessionAvailability('ERP104155')
        getAccessionAvailability('ERR164409')


def bug():

    import pandas as pd
    data = '~/MADAME/Downloads/apriltest/apriltest_merged_experiments-metadata.tsv'
    df = pd.read_csv(data, sep='\t', keep_default_na=False)
    lista = df['study_accession'].unique()
    print(len(lista))


#bug()

def altro():
    import os
    import pandas as pd

    root = '/home/gsoletta/MADAME/Downloads/apriltest/'
    dirlist = [ item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item)) ]

    for dir in dirlist:
        filename = f'{dir}_experiments-metadata.tsv'
        df = pd.read_csv(os.path.join(root, dir, filename), sep='\t', keep_default_na=False)
        lista = df['study_accession'].unique()
        print(f'numero di accession project dentro {dir}: ', len(lista))

def ecc():
    from rich.panel import Panel
    from rich.text import Text
    from rich import print as rich_print
    from rich.console import Console

    console = Console()
    box = console.print(Panel(("Instead of holding data, umbrella projects group together multiple projects that are part of the same research motivation or collaboration.\nMore info on [link=https://ena-docs.readthedocs.io/en/latest/retrieval/ena-project.html]ENA's documentation here[/link]."), title=(":umbrella: Umbrella Projects - Info Box"), border_style= "rgb(255,255,0)", padding= (0,1), width= 80, title_align="left"))

    rich_print("\n[rgb(255,0,255)]How[/rgb(255,0,255)] do you want to proceed? Choose one of the following options:\n\n1 - Exclude umbrella projects\n2 - Include umbrella projects")



    rich_print(f"[rgb(255,0,255)]Available accessions → [/rgb(255,0,255)]", end="")
    lista = ["mela", "pera", "banana"]
    for i in lista[:-1]:
        print(f"{i}, ", end="")
    else:
        print(lista[-1])

    print()

    from IDlist import GetIDlist

    GetIDlist.Query("prova", "cat microbiome", "projects")
    queryresult = GetIDlist.queryresult

    df = pd.read_csv(io.StringIO(queryresult), sep='\t', dtype=str)

    from rich.console import Console
    from rich.table import Table
    from rich import box
    
    table = Table(row_styles=["", "rgb(204,153,255)"], header_style="rgb(255,0,255)", box=box.ROUNDED)

    table.add_column("Accession", justify="left", no_wrap=True)
    table.add_column("Description", justify="left")

    for row in df.index:
        table.add_row(f"[link=https://www.ebi.ac.uk/ena/browser/view/{df['accession'][row]}]{df['accession'][row]}[/link]", f"{df['description'][row]}")

    table.add_row(f"[link=https://www.ebi.ac.uk/ena/browser/view/][yellow]☂ ombrello[yellow][/link]", f"descrizione")

    console = Console()
    console.print(table)

