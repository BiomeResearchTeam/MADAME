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
