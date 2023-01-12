from Utilities import Color, Utilities

def report_module():
    title = " REPORT MODULE "
    print(Color.BOLD + Color.PURPLE + title.center(100, '-') + Color.END)
    print("\nMetadata files were sussessfully downloaded and you can find them in the download folder. Choose one of the following options: ")
    #create a download folder che conterrà tutti i projetti scaricati >> file di download dei metadati
    #raggruppare anche tutti i progetti che si scaricano sotto il nome della sessione >> farlo decidere allo user
    #quindi da modificare in metadata_retrivement_module_2 penso
    #creare listOfProjectIDs file così user lo può inserire nel modulo 2
    print(" 1 - Generate a report file on the information contained by the metadata files")
    print(" 2 - Main menu (to download sequences via the Module 2, or to exit)")
    user_report_input = int(input("\n>> Enter your choice: "))

    if user_report_input not in (1,2):
        print("Error, enter a valid choice!\n")
        return
    else:
        # if user_report_input == 1:
        #     report() 
        
        if user_report_input == 2:
            return


def report():
    return
