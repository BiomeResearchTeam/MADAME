from Utilities import Color, Utilities
import os
from os import path
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot
import plotly.express as px
import numpy as np
from Project import Project
import pycountry
import matplotlib.pyplot as plt
import geopandas as gpd
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim
from collections import Counter
from pycountry_convert import country_alpha2_to_continent_code, country_name_to_country_alpha2


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

#WORLD MAP 
# def findGeocode(country):
#     geolocator = Nominatim(user_agent="your_app_name")
#     try:
#         # Geolocate the center of the country
#         loc = geolocator.geocode(country)
#         # And return latitude and longitude
#         return geolocator.geocode(country)
    
#     except GeocoderTimedOut:
#         # Return missing value
#         return findGeocode(country) 

def alpha3code(column):
        CODE=[]
        for country in column:
            try:
                code=pycountry.countries.get(name=country).alpha_3
            # .alpha_3 means 3-letter country code 
            # .alpha_2 means 2-letter country code
                CODE.append(code)
            except:
                CODE.append('None')
        return CODE

def geography(user_session, e_df, p_df):

    country_list = []
    affiliation_list = p_df['affiliation'].tolist()
    #print(affiliation_list)
    for affiliation in affiliation_list:
        for country in pycountry.countries:
            if country.name in affiliation:
                country_list.append(country.name)

    countries = {}
    for country in pycountry.countries:
        countries[country.name] = country.alpha_2
        codes = [countries.get(country, 'Unknown code') for country in country_list]
    
    input =  country_list
    c = Counter( input )
    print( c.items() )

    country_df = pd.DataFrame(c.items(), columns = ['country', 'count'])

    country_df['CODE']=alpha3code(country_df.country) #iso_3

    fig = px.scatter_geo(country_df, locations="CODE",
                     hover_name="country", size="count",
                     projection="natural earth")
    fig.write_image(os.path.join(user_session, "world_map.png"))
    

    



    # world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    # world.columns=['pop_est', 'continent', 'name', 'CODE', 'gdp_md_est', 'geometry']
    # merge=pd.merge(world,country_df,on='CODE')

    # merge.plot(column='country', scheme="quantiles",
    #        figsize=(25, 20),
    #        legend=True,cmap='coolwarm')
    # plt.title('2020 Jan-May Confirmed Case Amount in Different Countries',fontsize=25)
    # # # add countries names and numbers 
    # # for i in range(0,10):
    # #     plt.text(float(merge.longitude[i]),float(merge.latitude[i]),"{}\n{}".format(merge.name[i],merge.Confirmed_Cases[i]),size=10)
    # # plt.show()
    # plt.write_image(os.path.join(user_session, "world_map.png"))

    
    # create a column for code 
    
    





    

    #country_df['iso_alpha'] = codes
    

    # df = px.data.gapminder().query("year == 2007")
    # print(df)

    # fig = px.scatter_geo(country_df, locations="country",
    #     color="count", # which column to use to set the color of markers
    #     #hover_name="country", # column added to hover information
    #     size="count", # size of markers
    #     projection="natural earth")

    # fig.write_image(os.path.join(user_session, "world_map.png"))
    


    # print(country_df)            
    # longitude = []
    # latitude = []

    # for country in (country_df["country"]):
    #     if findGeocode(country) != None:
    #         loc = findGeocode(country)
            
    #         # coordinates returned from 
    #         # function is stored into
    #         # two separate list
    #         latitude.append(loc.latitude)
    #         longitude.append(loc.longitude)
       
    #     # if coordinate for a city not
    #     # found, insert "NaN" indicating 
    #     # missing value 
    #     else:
    #         latitude.append(np.nan)
    #         longitude.append(np.nan)

    # country_df["Longitude"] = longitude
    # country_df["Latitude"] = latitude
    
    # print(country_df)





    #limits = [(0,2),(3,10),(11,20),(21,50),(50,3000)]
#     colors = ["royalblue","crimson","lightseagreen","orange","lightgrey"]
#     cities = []
#     scale = 5000

#     fig = go.Figure()

#     # for i in range(len(country_list_unique)):
#     #     lim = country_list[i]
#     #     #country_df_df_sub = country_df[lim[0]:lim[1]]
#     fig.add_trace(go.Scattergeo(
#         locations = country_df['country'],
#         locationmode = 'country names',
#             # lon = df_sub['lon'],
#             # lat = df_sub['lat'],
#             # text = df_sub['text'],
#         marker = dict(
#             size = country_df['count'],
#             color = country_df['count'],
#             line_color='rgb(40,40,40)',
#             line_width=0.5,
#             sizemode = 'area'
#             )))

#     fig.update_layout(
#             title_text = 'Number of publication',
#             showlegend = True,
#             geo = dict(
#                 scope = 'world',
#                 landcolor = 'rgb(217, 217, 217)',
#             )
#         )
#     fig.write_image(os.path.join(user_session, "world_map.png"))
# # #fig.show()

    




#PROJECT SIZE & BYTES
def projects_bytes(user_session, e_df):
    IDs =  e_df['study_accession'].unique().tolist()
    ids_list = []
    bytes_list = []
    size_list = []

    for id in IDs:
        bytes = Project.getProjectBytes(id, e_df, file_type = 'fastq')
        bytes_list.append(bytes)
        ids_list.append(id)
    
    for bytes in bytes_list:
        size = Utilities.bytes_converter(bytes)
        size_list.append(size)

    df = pd.DataFrame({'Project': ids_list, 'Size' : size_list, 'Bytes' : bytes_list})
    file_name = os.path.join(user_session,'Project_size&bytes.xlsx')
    df.to_excel(file_name)

    fig = px.histogram(df, x="Project", y="Bytes")
    fig.write_image(os.path.join(user_session, "projects_size&bytes_bar.png"))



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
    projects_bytes(user_session, e_df)