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

def prova_range():

    import re

    str_list = 'ERS4202782-ERS4202689'
    # chr: il primo match di qualsiasi gruppo di lettere in str_list
    chr = (re.search(r'[a-zA-Z]+', str_list)).group(0)
    # ranges: una lista di due elementi, il primo numero e il secondo numero del range str_list. [4202782, 4202789]
    # è solo un findall di tutti i numeri dentro str, con int applicato su entrambi
    ranges = list(map(int, re.findall(r'\d+', str_list)))  
    # # per la nuova lista assembla chr e i per ogni i nel range che parte 
    # # dal primo numero fino al secondo + 1 per comprenderlo
    new_list = ([f'{chr}{i}' for i in range(ranges[0], ranges[1]+1)])

    print(new_list)

# if range is not valid an empty list is returned :)

prova_range()

