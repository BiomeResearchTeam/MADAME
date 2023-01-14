from Utilities import Color, Utilities
import os

def report_generation(user_session):
    title = " REPORT MODULE "
    print(Color.BOLD + Color.PURPLE + title.center(100, '-') + Color.END)
    print(f"\nMetadata files were sussessfully downloaded and you can find them in the {user_session}")
    print("Choose one of the following options:")
    print(" 1 - Generate a report file about the information contained in the metadata files")
    print(" 2 - Return to the main menu")
    user_report_input = int(input("\n>> Enter your choice: "))

    if user_report_input not in (1,2):
        print("Error, enter a valid choice!\n")
        return
    else:
        # if user_report_input == (1):
        #     report() 
        
        if user_report_input == (2):
            return


def report():
    return



user_session = os.getcwd() #per fare prove
report_generation(user_session) #per fare prove