from Utilities import Color, Utilities
from metadata_retrievement_module import metadata_retrievement
from data_retrievement_module import data_retrievement
from publications_retrievement_module import publications_retrievement
import os

#from report_module import report_module

#/mnt/c/Users/fmgls/Desktop/MADAME/MADAME-master/PRJEB37496/PRJEB37496_experiments-metadata.tsv
#/mnt/c/Users/fmgls/Desktop/MADAME/MADAME-master/PRJEB37496/PRJEB37496_listOfProjectIDs.tsv


def main():

    #Utilities.createDirectory("Downloads")

    while True:
        Utilities.log()
        #Utilities.clear()
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

        print("\n\n Which module do you want to use? \n")
        print(" 1 - Metadata retrivement module: metadata search and download")
        print(" 2 - Data retrivement module: metadata-associated data download")
        print(" 3 - Pubblication retrivement module: metadata- and data- associated pubblications download")
        print("\n --- If you want to close MADAME digit: " + Color.BOLD + Color.PURPLE +"exit" + Color.END + " ---\n")
        while True:
            module_choice = input(">> Enter your option: ")
            if module_choice.isnumeric():
                module_choice = int(module_choice)
                if module_choice not in (1, 2, 3):
                    print("Error, enter a valid choice!\n")
                    continue
                break
            else:
                if module_choice in ("exit", "EXIT", "Exit"):
                    print(Color.BOLD + Color.PURPLE + "\nGood bye, see you soon!\n" + Color.END)
                    exit()
                else:
                    print("Wrong input, expected a numeric input or <exit> (without <>), try again.\n") 
        
        Utilities.clear()

        if module_choice == 1:            
            metadata_retrievement()
            #report_module()

        if module_choice == 2:
            data_retrievement()

        if module_choice == 3:
            publications_retrievement()



if __name__ == "__main__":
    main()