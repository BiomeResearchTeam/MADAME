from Utilities import Color, Utilities
import os
from os import path
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot
import plotly.express as px

def report_generation(user_session):
    while True:
        title = " REPORT MODULE "
        print(Color.BOLD + Color.PURPLE + title.center(100, '-') + Color.END)
        print("\nGenerate a report file about the information present in the downloaded metadata & publications files. \n\nChoose one of the following options:")
        print(" 1 - Use '*_merged_experiments-metadata.tsv' & '*_merged_publications-metadata.tsv' files present the current session")
        print(" 2 - Use '*_merged_experiments-metadata.tsv' & '*_merged_publications-metadata.tsv' files present in any other location of your computer")
        print("\n >>> Your current session is " + Color.BOLD + Color.YELLOW +f"{user_session}" + Color.END + " <<<\n")
        print(" --- If you want to return to the main menu digit: " + Color.BOLD + Color.PURPLE + "main menu" + Color.END + " ---\n")
        user_report_input = input("\n>> Enter your choice: ").strip()
        
        if user_report_input in ("main menu", "MAIN MENU", "Main menu"):
            return

        elif user_report_input.isnumeric() == False:
            print(Color.BOLD + Color.RED + "\nWrong input" + Color.END, "expected a numeric input or <main menu> (without <>)\n\n")

        elif user_report_input.isnumeric() == True:
            user_report_input = int(user_report_input)
            if user_report_input not in (1,2):
                print("Error, enter a valid choice!\n")
                return

            else:

                if user_report_input == (1):
                    user_session = os.path.join("Downloads", user_session)
                    
                    file_count = check_files(user_session)
                    if file_count == 0:
                        print(Color.BOLD + Color.RED + "\nError" + Color.END, "found 0 file. Is it the correct folder?\n")

                    if file_count == 1:
                        merged_experiments = check_file_experiments(user_session)
                        e_df = read_experiments(user_session, merged_experiments)

                    if file_count == 2:
                        merged_experiments = check_file_experiments(user_session)
                        e_df = read_experiments(user_session, merged_experiments)
                        merged_publications = check_file_publications(user_session)
                        p_df = read_publications(user_session, merged_publications)
                        report_ep(user_session, e_df, p_df)

                    if file_count > 2:
                        print(Color.BOLD + Color.RED + "\nError" + Color.END, "found too many files. Please choose a folder containing only 1 '*_merged_experiments-metadata.tsv' & 1 '*_merged_publications-metadata.tsv' ")
                    
                    

                if user_report_input == (2):
                    user_report_local_path = user_report_local()
                    file_count = check_files(user_report_local_path)
                    if file_count == 0:
                        print(Color.BOLD + Color.RED + "\nError" + Color.END, "found 0 file. Is it the correct folder?\n")

                    if file_count == 1:
                        merged_experiments = check_file_experiments(user_report_local_path)
                        e_df = read_experiments(user_report_local_path, merged_experiments)

                    if file_count == 2:
                        merged_experiments = check_file_experiments(user_report_local_path)
                        e_df = read_experiments(user_report_local_path, merged_experiments)
                        merged_publications = check_file_publications(user_report_local_path)
                        p_df = read_publications(user_report_local_path, merged_publications)

                    if file_count > 2:
                        print(Color.BOLD + Color.RED + "\nError" + Color.END, "found too many files. Please choose a folder containing only 1 '*_merged_experiments-metadata.tsv' & 1 '*_merged_publications-metadata.tsv' ")
                    

def user_report_local():
    Utilities.clear()
    while True:
        print("Enter the path for '*_merged_experiments-metadata.tsv' & '*_merged_publications-metadata.tsv' files. \nThe report will be downloaded in the folder indicated.")
        print("\n --- If you want to return to the main menu digit: " + Color.BOLD + Color.PURPLE + "main menu" + Color.END + " ---\n") #verificare se è vero o se torna al report
        user_report_local_path = input("\n>> Digit the path: ").strip()
                            
        if path.isdir(user_report_local_path) == False:
            if path.isfile(user_report_local_path) == True:
                print(Color.BOLD + Color.RED + "Error. " + Color.END, "Please digit the path for the folder containing '*_merged_experiments-metadata.tsv' & '*_merged_publications-metadata.tsv' files\n\n")
                return
            else:
                print(Color.BOLD + Color.RED + "Folder not found." + Color.END, " Maybe a typo? Try again\n\n")
                return
        else:
            return user_report_local_path



#check files
def check_files(user_session):
    count = 0
    for file in os.listdir(user_session):
        if file.endswith(("_merged_experiments-metadata.tsv", "_merged_publications-metadata.tsv")):
            print(Color.BOLD + Color.GREEN + "Found" + Color.END, f"{file}")
            count += 1   
    return count    

def check_file_experiments(user_session):
    for file in os.listdir(user_session):
        if file.endswith("_merged_experiments-metadata.tsv"):
            return file
        
def check_file_publications(user_session):
    for file in os.listdir(user_session):
        if file.endswith("_merged_publications-metadata.tsv"):
            return file



#open tsv
def read_experiments(user_session, merged_experiments):
    path = os.path.join(user_session, merged_experiments)
    e_df = pd.read_csv (path, delimiter='\t', infer_datetime_format=True)
    return e_df

def read_publications(user_session, merged_publications):
    path = os.path.join(user_session, merged_publications)
    p_df = pd.read_csv (path, delimiter='\t', infer_datetime_format=True)
    return p_df



#functions for report
def IDs_number(e_df):
    IDs_number = e_df['study_accession'].nunique()
    print('Number of projects:', IDs_number)
    return IDs_number

def sample_number(user_session, e_df):
    sample_number_series = e_df.groupby(['study_accession'])['run_accession'].count()
    sample_number_df = pd.DataFrame(sample_number_series).reset_index()
    sample_number_df.columns = ['Project', 'Number of samples']
    fig = px.bar(sample_number_df, x="Project", y="Number of samples") #non va colore...
    fig.write_image(os.path.join(user_session, "sample_number.png"))


def IDs_dates(user_session, e_df):
    
    cols = ['first_public', 'last_updated']
    if pd.Series(['first_public', 'last_updated']).isin(e_df.columns).all():
        e_df['first_public'] = pd.to_datetime(e_df['first_public'],  errors='coerce', infer_datetime_format=True) #convert into datatyoe
        e_df['last_updated'] = pd.to_datetime(e_df['last_updated'], errors='coerce', infer_datetime_format=True)
        e_df['first_public_year'] = e_df['first_public'].dt.year #select only year
        e_df['last_updated_year'] = e_df['last_updated'].dt.year
        collapsed_e_df = e_df.groupby('study_accession').first().reset_index()
        collapsed_e_df_f = collapsed_e_df[['study_accession', 'first_public_year']]
        collapsed_e_df_l = collapsed_e_df[['study_accession', 'last_updated_year']]
        collapsed_e_dict_f = collapsed_e_df_f.set_index('study_accession')['first_public_year'].to_dict() #convert into dictionary
        collapsed_e_dict_l = collapsed_e_df_l.set_index('study_accession')['last_updated_year'].to_dict()
        print(collapsed_e_dict_f)
        print(collapsed_e_dict_l)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=collapsed_e_dict_f.keys(),
            y=collapsed_e_dict_f.values(),
            marker=dict(color="crimson", size=12),
            mode="markers",
            name="Year of first udate",
        ))
        
        fig.add_trace(go.Scatter(
            x=collapsed_e_dict_l.keys(),
            y=collapsed_e_dict_l.values(),
            marker=dict(color="gold", size=12),
            mode="markers",
            name="Year of last update",
        ))

        fig.update_layout(title="Years of first and last update",
                        xaxis_title="Year",
                        yaxis_title="Projects")

    else:
        print('qui')
        pass
        
        # IDs_dates_f = e_df[['study_accession', 'first_public']]
        # IDs_dates_f.groupby(['study_accession'])['first_public']


# schools = ["Brown", "NYU", "Notre Dame", "Cornell", "Tufts", "Yale",
#            "Dartmouth", "Chicago", "Columbia", "Duke", "Georgetown",
#            "Princeton", "U.Penn", "Stanford", "MIT", "Harvard"]

# fig = go.Figure()
# fig.add_trace(go.Scatter(
#     x=[72, 67, 73, 80, 76, 79, 84, 78, 86, 93, 94, 90, 92, 96, 94, 112],
#     y=schools,
#     marker=dict(color="crimson", size=12),
#     mode="markers",
#     name="Women",
# ))

# fig.add_trace(go.Scatter(
#     x=[92, 94, 100, 107, 112, 114, 114, 118, 119, 124, 131, 137, 141, 151, 152, 165],
#     y=schools,
#     marker=dict(color="gold", size=12),
#     mode="markers",
#     name="Men",
# ))

# fig.update_layout(title="Gender Earnings Disparity",
#                   xaxis_title="Annual Salary (in thousands)",
#                   yaxis_title="School")

# fig.show()
    


#report
def report_ep(user_session, e_df, p_df):
    IDs_number(e_df)
    sample_number(user_session, e_df)
    IDs_dates(user_session, e_df)
    return