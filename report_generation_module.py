from Utilities import Color, Utilities
import os

def report_generation(user_session):
    title = " REPORT MODULE "
    print(Color.BOLD + Color.PURPLE + title.center(100, '-') + Color.END)
    
    print("\nGenerate a report file about the information contained in the downloaded metadata & publications files. Choose one of the following options:")
    print(" 1 - Use '*_merged_experiments-metadata.tsv' & '*_merged_publications-metadata.tsv' files present in a folder created by MADAME")
    print(" 2 - Use '*_merged_experiments-metadata.tsv' & '*_merged_publications-metadata.tsv' files present in any other location")
    print(" --- If you want to return to the main menu digit: " + Color.BOLD + Color.PURPLE + "main menu" + Color.END + " ---\n")
    user_report_input = input("\n>> Enter your choice: ").strip()

    while True: 
        
        if user_report_input.isnumeric():
            user_report_input = int(user_report_input)
            if user_report_input not in (1,2):
                print("Error, enter a valid choice!\n")
                return
        
        else:
            if user_report_input in ("main menu", "MAIN MENU", "Main menu"):
                return
            else: 
                print("Wrong input, expected a numeric input, or <main menu> (without <>). Try again.\n")


    
        # if user_report_input == (1):
        #     report() 
        
        # if user_report_input == (2):
        #     return


def report():
    return



def IDs_number():
    return


# user_session = os.getcwd() #per fare prove
# report_generation(user_session) #per fare prove