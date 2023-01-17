from Utilities import Color, Utilities
import os
from os import path
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot
import plotly.express as px
import numpy as np
import pycountry


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
                    print(user_session)
                    
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
                        print(Color.BOLD + Color.RED + "\nError" + Color.END, "found too many files. Please choose a folder containing only 1 '*_merged_experiments-metadata.tsv'")
                    
                    

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
        collapsed_e_df = collapsed_e_df.sort_values(by=['first_public_year'], ascending=True)
        collapsed_e_df_f = collapsed_e_df[['study_accession', 'first_public_year']]
        collapsed_e_df_l = collapsed_e_df[['study_accession', 'last_updated_year']]
        # collapsed_e_dict_f = collapsed_e_df_f.set_index('study_accession')['first_public_year'].to_dict() #convert into dictionary
        # collapsed_e_dict_l = collapsed_e_df_l.set_index('study_accession')['last_updated_year'].to_dict()
        collapsed_e_list_f_y = collapsed_e_df_f.study_accession.values.tolist()
        collapsed_e_list_f_x = collapsed_e_df_f.first_public_year.values.tolist()
        collapsed_e_list_l_y = collapsed_e_df_l.study_accession.values.tolist()
        collapsed_e_list_l_x = collapsed_e_df_l.last_updated_year.values.tolist()

        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=collapsed_e_list_f_x,
            y=collapsed_e_list_f_y,
            marker=dict(color="crimson", size=12), #colore da modificare
            mode="markers",
            name="Year of first udate",
        ))
        
        fig.add_trace(go.Scatter(
            x= collapsed_e_list_l_x,
            y=collapsed_e_list_l_y ,
            marker=dict(color="gold", size=12), #colore da modificare
            mode="markers",
            name="Year of last update",
        ))

        fig.update_layout(title="Years of first and last update",
                        xaxis_title="Year",
                        yaxis_title="Projects")

        fig.write_image(os.path.join(user_session, "years_update.png"))

    else:
        pass
        

def publication_title(user_session, p_df):
    p_list_project = p_df.input_accession_id.values.tolist()
    p_list_title = p_df.title.values.tolist()
    d = {
        'Project': p_list_project,
        'Publication title': p_list_title
        }
    df = pd.DataFrame(data=d)
    file_name = os.path.join(user_session,'Publication_title.xlsx')
    df.to_excel(file_name)


def scientific_name_pie(user_session, e_df):
    col = ['scientific_name']
    if pd.Series(['scientific_name']).isin(e_df.columns).all():
        scientific_name_df = e_df['scientific_name'].value_counts()
        df = pd.DataFrame(scientific_name_df).reset_index()
        df.columns = ['Scientific name', 'Counts']
        fig = px.pie(df, values='Counts', names='Scientific name', color_discrete_sequence=px.colors.sequential.RdBu)
        fig.write_image(os.path.join(user_session, "scientific_name_pie.png"))
    else:
        pass


def scientific_name_bar(user_session, e_df):
    col = ['scientific_name']
    if pd.Series(['scientific_name']).isin(e_df.columns).all():
        scientific_name_IDs_df = e_df.groupby(['study_accession'])['scientific_name'].value_counts()
        df_bar = scientific_name_IDs_df.rename('count').reset_index()
        df_bar.columns = ['Project', 'Scientific name', 'Counts']
        fig = px.histogram(df_bar, x="Project", y="Counts",
                color='Scientific name',
                labels={'Counts':'Number of samples'},
                height=400)
        fig.write_image(os.path.join(user_session, "scientific_name_bar.png"))
    else:
        pass


def library_source(user_session, e_df):
    col = ['library_source']
    if pd.Series(['library_source']).isin(e_df.columns).all():
        library_source_df = e_df['library_source'].value_counts()
        df = pd.DataFrame(library_source_df).reset_index()
        df.columns = ['Library source', 'Counts']
        fig = px.pie(df, values='Counts', names='Library source', color_discrete_sequence=px.colors.sequential.RdBu)
        fig.write_image(os.path.join(user_session, "library_source_pie.png"))
    else:
        pass


def library_source_bar(user_session, e_df):
    col = ['library_source']
    if pd.Series(['library_source']).isin(e_df.columns).all():
        library_source_IDs_df = e_df.groupby(['study_accession'])['library_source'].value_counts()
        df_bar = library_source_IDs_df.rename('count').reset_index()
        df_bar.columns = ['Project', 'Library source', 'Counts']
        fig = px.histogram(df_bar, x="Project", y="Counts",
                color='Library source',
                labels={'Counts':'Number of samples'},
                height=400)
        fig.write_image(os.path.join(user_session, "library_source_bar.png"))
    else:
        pass


def library_strategy_pie(user_session, e_df):
    col = ['library_strategy']
    if pd.Series(['library_strategy']).isin(e_df.columns).all():
        library_strategy_df = e_df['library_strategy'].value_counts()
        df = pd.DataFrame(library_strategy_df).reset_index()
        df.columns = ['Library strategy', 'Counts']
        fig = px.pie(df, values='Counts', names='Library strategy', color_discrete_sequence=px.colors.sequential.RdBu)
        fig.write_image(os.path.join(user_session, "library_strategy_pie.png"))
    else:
        pass


def library_strategy_bar(user_session, e_df):
    col = ['library_strategy']
    if pd.Series(['library_strategy']).isin(e_df.columns).all():
        library_strategy_IDs_df = e_df.groupby(['study_accession'])['library_strategy'].value_counts()
        df_bar = library_strategy_IDs_df.rename('count').reset_index()
        df_bar.columns = ['Project', 'Library strategy', 'Counts']
        fig = px.histogram(df_bar, x="Project", y="Counts",
                color='Library strategy',
                labels={'Counts':'Number of samples'},
                height=400)
        fig.write_image(os.path.join(user_session, "library_strategy_bar.png"))
    else:
        pass


def instrument_platform_pie(user_session, e_df):
    col = ['instrument_platform']
    if pd.Series(['instrument_platform']).isin(e_df.columns).all():
        instrument_platform_df = e_df['instrument_platform'].value_counts()
        df = pd.DataFrame(instrument_platform_df).reset_index()
        df.columns = ['Instrument platform', 'Counts']
        fig = px.pie(df, values='Counts', names='Instrument platform', color_discrete_sequence=px.colors.sequential.RdBu)
        fig.write_image(os.path.join(user_session, "instrument_platform_pie.png"))
    else:
        pass


def instrument_platform_bar(user_session, e_df):
    col = ['instrument_platform']
    if pd.Series(['instrument_platform']).isin(e_df.columns).all():
        instrument_platform_IDs_df = e_df.groupby(['study_accession'])['instrument_platform'].value_counts()
        df_bar = instrument_platform_IDs_df.rename('count').reset_index()
        df_bar.columns = ['Project', 'Instrument platform', 'Counts']
        fig = px.histogram(df_bar, x="Project", y="Counts",
                color='Instrument platform',
                labels={'Counts':'Number of samples'},
                height=400)
        fig.write_image(os.path.join(user_session, "instrument_platform_bar.png"))
    else:
        pass


def library_layout_pie(user_session, e_df):
    col = ['library_layout']
    if pd.Series(['library_layout']).isin(e_df.columns).all():
        library_layout_df = e_df['library_layout'].value_counts()
        df = pd.DataFrame(library_layout_df).reset_index()
        df.columns = ['Library layout', 'Counts']
        fig = px.pie(df, values='Counts', names='Library layout', color_discrete_sequence=px.colors.sequential.RdBu)
        fig.write_image(os.path.join(user_session, "library_layout_pie.png"))
    else:
        pass


def library_layout_bar(user_session, e_df):
    col = ['library_layout']
    if pd.Series(['library_layout']).isin(e_df.columns).all():
        library_layout_IDs_df = e_df.groupby(['study_accession'])['library_layout'].value_counts()
        df_bar = library_layout_IDs_df.rename('count').reset_index()
        df_bar.columns = ['Project', 'Library layout', 'Counts']
        fig = px.histogram(df_bar, x="Project", y="Counts",
                color='Library layout',
                labels={'Counts':'Number of samples'},
                height=400)
        fig.write_image(os.path.join(user_session, "library_layout_bar.png"))
    else:
        pass


def geography(user_session, e_df, p_df):
    
    # p_df_id = p_df.sort_values(by=['input_accession_id'], ascending=True)
    # p_df_id = p_df_id[['input_accession_id', 'affiliation']]
    # e_df.rename(columns={'secondary_study_accession':'input_accession_id'}, inplace=True)
    # #print(e_df)
    # e_df_sort = e_df.sort_values(by=['input_accession_id'], ascending=True)

    p_id_list = p_df['input_accession_id'].tolist()
    e_df.rename(columns={'secondary_study_accession':'input_accession_id'}, inplace=True)
    print(p_id_list)
    e_df_filtered = e_df[e_df.input_accession_id.isin(p_id_list)]
    print(e_df_filtered)
    collapsed_e_df = e_df.groupby('study_accession')


    #print(e_df_sort)
    # merge_e_p_df = e_df[e_df.set_index('input_accession_id')].index.isin(p_df_id.set_index(['input_accession_id']).index)
    # print(merge_e_p_df)

    #joined = p_df_id.join(e_df.set_index(['study_accession']), on=['input_accession_id'], how='right')
    #print(joined)

    # merge = p_df_id.merge(e_df['input_accession_id'])
    # print(merge)

    # collapsed_e_df = e_df.groupby('input_accession_id').first().reset_index()
    # #print(collapsed_e_df)
    # merge = collapsed_e_df[collapsed_e_df['input_accession_id'].isin(p_df_id['input_accession_id'])]
    # print(merge)

    # p_df_id['study_accession'] = p_df_id.merge(e_df, on=['input_accession_id'], how='left')['study_accession']
    # print(p_df_id)

    # #merge_e_p_df = e_df_sort[e_df_sort.set_index('secondary_study_accession')].index.isin(p_df_id.set_index(['input_accession_id']).index)
    # print(e_df_sorted)

    #text = "United States (New York), United Kingdom (London)"

    # for country in pycountry.countries:
    #     if country.name in text:
    #         print(country.name)

def projects_bytes(user_session, e_df,):
    collapsed_e_df =  e_df['study_accession'].nunique()
    IDs = collapsed_e_df.to_list()
    for id in IDs:
        return




#report
def report_ep(user_session, e_df, p_df):
    IDs_number(e_df)
    sample_number(user_session, e_df)
    IDs_dates(user_session, e_df)
    publication_title(user_session, p_df)
    scientific_name_pie(user_session, e_df)
    scientific_name_bar(user_session, e_df)
    library_source(user_session, e_df)
    library_source_bar(user_session, e_df)
    library_strategy_pie(user_session, e_df)
    library_strategy_bar(user_session, e_df)
    instrument_platform_pie(user_session, e_df)
    instrument_platform_bar(user_session, e_df)
    library_layout_pie(user_session, e_df)
    library_layout_bar(user_session, e_df)
    geography(user_session, e_df, p_df)