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
    print(Panel("[bold center purple]DATA RETRIEVEMENT MODULE"))
    print("[link https://google.com]:computer: GitHub")

    from rich import print
    from rich.panel import Panel
    from rich.text import Text
    title = Panel(Text("DATA RETRIEVEMENT MODULE", style = "b magenta", justify="center"), style = "b magenta")
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
