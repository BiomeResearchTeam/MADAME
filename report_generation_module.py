from Utilities import Color, Utilities
import os
from os import path
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from Project import Project
import pycountry
from collections import Counter
from plotly.subplots import make_subplots #vediamo se serve


def report_generation(user_session):
    while True:
        Utilities.clear() 
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
            print(Color.BOLD + Color.RED + "Wrong input" + Color.END, "expected a numeric input or <main menu> (without <>)\n")
            input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue")

        elif user_report_input.isnumeric() == True:
            user_report_input = int(user_report_input)
            if user_report_input not in (1,2):
                print(Color.BOLD + Color.RED +"Error" + Color.END,"enter a valid choice!")
                input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue")

            else:

                if user_report_input == (1):
                    user_session = os.path.join("Downloads", user_session)
                    
                    file_count = check_files(user_session)
                    if file_count == 0:
                        print(Color.BOLD + Color.RED + "\nError" + Color.END, "found 0 file. Is it the correct folder? Note that the file names must end with '_merged_experiments-metadata.tsv' and '_merged_publications-metadata.tsv'\n")
                        input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue")

                    if file_count == 1:
                        merged_experiments = check_file_experiments(user_session)
                        e_df = read_experiments(user_session, merged_experiments)
                        experiment_report(user_session, e_df)
                        final_screen(user_session)


                    if file_count == 2:
                        merged_experiments = check_file_experiments(user_session)
                        e_df = read_experiments(user_session, merged_experiments)
                        merged_publications = check_file_publications(user_session)
                        p_df = read_publications(user_session, merged_publications)
                        experiment_report(user_session, e_df)
                        publication_report(user_session, p_df)
                        final_screen(user_session)

                    if file_count > 2:
                        print(Color.BOLD + Color.RED + "\nError" + Color.END, "found too many files. Please choose a folder containing only 1 '*_merged_experiments-metadata.tsv'")
                        input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue")
                    
                    

                if user_report_input == (2):
                    user_report_local_path = user_report_local()
                    file_count = check_files(user_report_local_path)
                    if file_count == 0:
                        print(Color.BOLD + Color.RED + "\nError" + Color.END, "found 0 file. Is it the correct folder? Note that the file names must end with '_merged_experiments-metadata.tsv' and '_merged_publications-metadata.tsv'\n")
                        input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue")

                    if file_count == 1:
                        merged_experiments = check_file_experiments(user_report_local_path)
                        e_df = read_experiments(user_report_local_path, merged_experiments)
                        experiment_report(user_session, e_df)
                        final_screen(user_session)

                    if file_count == 2:
                        merged_experiments = check_file_experiments(user_report_local_path)
                        e_df = read_experiments(user_report_local_path, merged_experiments)
                        merged_publications = check_file_publications(user_report_local_path)
                        p_df = read_publications(user_report_local_path, merged_publications)
                        experiment_report(user_session, e_df)
                        publication_report(user_session, p_df)
                        final_screen(user_session)

                    if file_count > 2:
                        print(Color.BOLD + Color.RED + "\nError" + Color.END, "found too many files. Please choose a folder containing only 1 '*_merged_experiments-metadata.tsv' & 1 '*_merged_publications-metadata.tsv' ")
                        input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue")
                    

def user_report_local():
    Utilities.clear()
    while True:
        title = " REPORT MODULE "
        print(Color.BOLD + Color.PURPLE + title.center(100, '-') + Color.END)
        print("\nEnter the path for '*_merged_experiments-metadata.tsv' & '*_merged_publications-metadata.tsv' files. \nThe report will be downloaded in the folder indicated.")
        print("\n --- If you want to return to the main menu digit: " + Color.BOLD + Color.PURPLE + "main menu" + Color.END + " ---\n") #verificare se è vero o se torna al report
        user_report_local_path = input("\n>> Digit the path: ").strip()
                            
        if path.isdir(user_report_local_path) == False:
            if path.isfile(user_report_local_path) == True:
                print(Color.BOLD + Color.RED + "Error" + Color.END, "Please digit the path for the folder containing '*_merged_experiments-metadata.tsv' & '*_merged_publications-metadata.tsv' files\n")
                input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue")
                return
            else:
                print(Color.BOLD + Color.RED + "Folder not found." + Color.END, " Maybe a typo? Try again\n")
                input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue")
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


def sample_number(user_session, e_df, color_palette):
    sample_number_series = e_df.groupby(['study_accession'])['run_accession'].count()
    sample_number_df = pd.DataFrame(sample_number_series).reset_index()
    sample_number_df.columns = ['Project', 'Number of samples']
    fig = px.bar(sample_number_df, x="Project", y="Number of samples", color_discrete_sequence=color_palette).update_layout(yaxis_title="Number of samples") 
    fig.write_image(os.path.join(user_session, "sample_number.png"))


def IDs_dates(user_session, e_df):
    cols = ['first_public', 'last_updated']
    if pd.Series(['first_public', 'last_updated']).isin(e_df.columns).all():
        e_df['first_public'] = pd.to_datetime(e_df['first_public'],  errors='coerce', infer_datetime_format=True) #convert into datatype
        e_df['last_updated'] = pd.to_datetime(e_df['last_updated'], errors='coerce', infer_datetime_format=True)
        e_df['first_public_year'] = e_df['first_public'].dt.year #create a new column with only year
        e_df['last_updated_year'] = e_df['last_updated'].dt.year
        collapsed_e_df = e_df.groupby('study_accession').first().reset_index()
        collapsed_e_df = collapsed_e_df.sort_values(by=['first_public_year'], ascending=True)
        collapsed_e_df_f = collapsed_e_df[['study_accession', 'first_public_year']]
        collapsed_e_df_l = collapsed_e_df[['study_accession', 'last_updated_year']]
        collapsed_e_list_f_x = collapsed_e_df_f.study_accession.values.tolist()
        collapsed_e_list_f_y = collapsed_e_df_f.first_public_year.values.tolist()
        collapsed_e_list_l_x = collapsed_e_df_l.study_accession.values.tolist()
        collapsed_e_list_l_y = collapsed_e_df_l.last_updated_year.values.tolist()

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=collapsed_e_list_f_x,
            y=collapsed_e_list_f_y,
            marker=dict(color='rgb(41, 24, 107)', size=30),
            mode="markers",
            name="Year of first update",
            opacity=0.9
        ))
        
        fig.add_trace(go.Scatter(
            x= collapsed_e_list_l_x,
            y=collapsed_e_list_l_y ,
            marker=dict(color='rgb(255, 230, 87)', size=30),
            mode="markers",
            name="Year of last update",
            opacity=0.9
        ))

        fig.update_layout(title="Years of first and last update",
                        xaxis_title="Projects",
                        yaxis_title="Year")
        
        fig.update_yaxes(type="category", categoryorder='category ascending') #make years as categorical and sort them

        fig.write_image(os.path.join(user_session, "years_update.png"))

    else:
        pass
        

def publication_title(user_session, p_df,color_palette):
    p_list_project = p_df.input_accession_id.values.tolist()
    p_list_title = p_df.title.values.tolist()
    d = {
        'Project': p_list_project,
        'Publication title': p_list_title
        }
    df = pd.DataFrame(data=d)
    file_name = os.path.join(user_session,'Publication_title.xlsx')
    df.to_excel(file_name)


def scientific_name_pie(user_session, e_df, color_palette):
    col = ['scientific_name']
    if pd.Series(['scientific_name']).isin(e_df.columns).all():
        scientific_name_df = e_df['scientific_name'].value_counts()
        df = pd.DataFrame(scientific_name_df).reset_index()
        df.columns = ['Scientific name', 'Counts']
        fig = px.pie(df, values='Counts', names='Scientific name', color_discrete_sequence=color_palette)
        fig.write_image(os.path.join(user_session, "scientific_name_pie.png"))
    else:
        pass


def scientific_name_bar(user_session, e_df, color_palette):
    col = ['scientific_name']
    if pd.Series(['scientific_name']).isin(e_df.columns).all():
        scientific_name_IDs_df = e_df.groupby(['study_accession'])['scientific_name'].value_counts()
        df_bar = scientific_name_IDs_df.rename('count').reset_index()
        df_bar.columns = ['Project', 'Scientific name', 'Counts']
        fig = px.histogram(df_bar, x="Project", y="Counts",
                color='Scientific name', color_discrete_sequence=color_palette, 
                height=400).update_layout(yaxis_title="Number of samples")
        fig.write_image(os.path.join(user_session, "scientific_name_bar.png"))
    else:
        pass


def library_source(user_session, e_df, color_palette):
    col = ['library_source']
    if pd.Series(['library_source']).isin(e_df.columns).all():
        library_source_df = e_df['library_source'].value_counts()
        df = pd.DataFrame(library_source_df).reset_index()
        df.columns = ['Library source', 'Counts']
        fig = px.pie(df, values='Counts', names='Library source', color_discrete_sequence=color_palette)
        fig.write_image(os.path.join(user_session, "library_source_pie.png"))
    else:
        pass


def library_source_bar(user_session, e_df, color_palette):
    col = ['library_source']
    if pd.Series(['library_source']).isin(e_df.columns).all():
        library_source_IDs_df = e_df.groupby(['study_accession'])['library_source'].value_counts()
        df_bar = library_source_IDs_df.rename('count').reset_index()
        df_bar.columns = ['Project', 'Library source', 'Counts']
        fig = px.histogram(df_bar, x="Project", y="Counts",
                color='Library source',
                color_discrete_sequence=color_palette,
                height=400).update_layout(yaxis_title="Number of samples")
        fig.write_image(os.path.join(user_session, "library_source_bar.png"))
    else:
        pass


def library_strategy_pie(user_session, e_df, color_palette):
    col = ['library_strategy']
    if pd.Series(['library_strategy']).isin(e_df.columns).all():
        library_strategy_df = e_df['library_strategy'].value_counts()
        df = pd.DataFrame(library_strategy_df).reset_index()
        df.columns = ['Library strategy', 'Counts']
        fig = px.pie(df, values='Counts', names='Library strategy', color_discrete_sequence=color_palette)
        fig.write_image(os.path.join(user_session, "library_strategy_pie.png"))
    else:
        pass


def library_strategy_bar(user_session, e_df, color_palette):
    col = ['library_strategy']
    if pd.Series(['library_strategy']).isin(e_df.columns).all():
        library_strategy_IDs_df = e_df.groupby(['study_accession'])['library_strategy'].value_counts()
        df_bar = library_strategy_IDs_df.rename('count').reset_index()
        df_bar.columns = ['Project', 'Library strategy', 'Counts']
        fig = px.histogram(df_bar, x="Project", y="Counts",
                color='Library strategy',
                color_discrete_sequence=color_palette,
                height=400).update_layout(yaxis_title="Number of samples")
        fig.write_image(os.path.join(user_session, "library_strategy_bar.png"))
    else:
        pass


def instrument_platform_pie(user_session, e_df, color_palette):#, color_palette): #
    col = ['instrument_platform']
    if pd.Series(['instrument_platform']).isin(e_df.columns).all():
        instrument_platform_df = e_df['instrument_platform'].value_counts()
        df = pd.DataFrame(instrument_platform_df).reset_index()
        df.columns = ['Instrument platform', 'Counts']
        fig = px.pie(df, values='Counts', names='Instrument platform', color_discrete_sequence=color_palette) #
        fig.write_image(os.path.join(user_session, "instrument_platform_pie.png"))
    else:
        pass


def instrument_platform_bar(user_session, e_df, color_palette):
    col = ['instrument_platform']
    if pd.Series(['instrument_platform']).isin(e_df.columns).all():
        instrument_platform_IDs_df = e_df.groupby(['study_accession'])['instrument_platform'].value_counts()
        df_bar = instrument_platform_IDs_df.rename('count').reset_index()
        df_bar.columns = ['Project', 'Instrument platform', 'Counts']
        fig = px.histogram(df_bar, x="Project", y="Counts",
                color='Instrument platform',
                color_discrete_sequence=color_palette,
                height=400).update_layout(yaxis_title="Number of samples")
        fig.write_image(os.path.join(user_session, "instrument_platform_bar.png"))
    else:
        pass


# def library_layout_pie(user_session, e_df, color_palette):     #ACCORPATA IN LIBRARY_LAYOUT SE TUTTO FUNZIONA ELIMINARE

#     col = ['library_layout']
#     if pd.Series(['library_layout']).isin(e_df.columns).all():
#         library_layout_df = e_df['library_layout'].value_counts()
#         df = pd.DataFrame(library_layout_df).reset_index()
#         df.columns = ['Library layout', 'Counts']
#         fig = px.pie(df, values='Counts', names='Library layout', color_discrete_sequence=color_palette) 
#         fig.write_image(os.path.join(user_session, "library_layout_pie.png")) 

#     else:
#         pass


# def library_layout_bar(user_session, e_df, color_palette, f):      #ACCORPATA IN LIBRARY_LAYOUT SE TUTTO FUNZIONA ELIMINARE
#     col = ['library_layout']
#     if pd.Series(['library_layout']).isin(e_df.columns).all():
#         library_layout_IDs_df = e_df.groupby(['study_accession'])['library_layout'].value_counts()
#         df_bar = library_layout_IDs_df.rename('count').reset_index()
#         df_bar.columns = ['Project', 'Library layout', 'Counts']
#         fig = px.histogram(df_bar, x="Project", y="Counts",
#                 color='Library layout',
#                 color_discrete_sequence=color_palette).update_layout(yaxis_title="Number of samples")
#         fig.write_image(os.path.join(user_session, "library_layout_bar.png"))
#         fig.write_html(os.path.join(user_session, "library_layout_bar.html"))
#         # with open('p_graph.html', 'a') as f:
#         f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))

#     else:
#         pass



def library_layout(user_session, e_df, color_palette_hex, f): #sistemare legenda, titolo, hoverdata e altri dettagli che non mi vengono in mente ora
    col = ['library_layout']
    if pd.Series(['library_layout']).isin(e_df.columns).all():
        library_layout_df = e_df['library_layout'].value_counts()
        df_pie = pd.DataFrame(library_layout_df).reset_index()
        df_pie.columns = ['Library layout', 'Counts']
        
        library_layout_IDs_df = e_df.groupby(['study_accession'])['library_layout'].value_counts() #SISTEMARE QUESTI DF, SONO RIPETIZIONI
        df_bar = library_layout_IDs_df.rename('count').reset_index()
        df_bar.columns = ['Project', 'Library layout', 'Counts']
        
        # list_llayout = list(df_bar['Library layout'])
        # print(list_llayout)
        # pd.factorize(list_llayout)
        # print(pd.factorize(list_llayout))
        # list_llayout_numbers = pd.factorize(list_llayout)[0]
        # print(list_llayout_numbers)

        color_dictionary = dict(zip(df_bar['Library layout'].unique(), color_palette_hex)) #associate column values to color
        # print(c)
        df_bar['Color'] = df_bar['Library layout'].map(color_dictionary) #create a new column based on the dictionary
        # print(df_bar)
        

        fig = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "bar"}]])

        fig.add_trace(go.Pie(labels=df_pie['Library layout'], values=df_pie['Counts'], hole=0.6, marker_colors= df_pie["Library layout"].map(color_dictionary)),
            row=1, col=1)
        
        fig.add_trace(go.Bar(x=df_bar["Project"], y = df_bar["Counts"], marker_color = df_bar['Color']),
             row=1, col=2)
        
        fig.update_layout(title_text="Side By Side Subplots")
        fig.write_image(os.path.join(user_session, "Side By Side Subplots.png"))
        fig.write_html(os.path.join(user_session, "Side By Side Subplots.html"))



#WORLD MAP 
def alpha3code(column): #create a list of ISO3 starting from the column of interest
        CODE=[]
        for country in column:
            try:
                code=pycountry.countries.get(name=country).alpha_3
                CODE.append(code)
            except:
                CODE.append('None')
        return CODE

def geography(user_session, p_df, f):
    country_list = []
    affiliation_list = p_df['affiliation'].tolist()
    for affiliation in affiliation_list:
        for country in pycountry.countries: #extract the name of the country from a string, in this case the affiliation
            if country.name in affiliation:
                country_list.append(country.name)
    
    input =  country_list
    c = Counter(input) #counter of countries
    country_df = pd.DataFrame(c.items(), columns = ['country', 'count'])
    country_df['CODE']=alpha3code(country_df.country) #call alpha3code to create ISO3 column


    # #PROVA: choropleth
    # fig = px.choropleth(country_df, locations="CODE",
    #     color="count", # lifeExp is a column of gapminder
    #     #hover_name="country", # column to add to hover information
    #     color_continuous_scale=px.colors.sequential.dense)

    # fig.write_image(os.path.join(user_session, "world_map_choro.png"))


    #ATTENZIONE: FUNZIONA! >> DA CAMBIARE COLORI. BUBBLE PLOT
    fig = px.scatter_geo(country_df, locations="CODE", color = 'count', size="count", 
        #color_continuous_scale = px.colors.sequential.haline, opacity = 0.95)
        color_continuous_scale=['rgb(41, 24, 107)', 'rgb(255, 230, 87)'], opacity = 0.95)

    fig.update_layout(
        title = 'Map of publications', title_x=0.5,
        title_font_size=25,
        title_font_family='Times New Roman',
        showlegend = True, 
        coloraxis_colorbar=dict(title="Number of <br>publications", #start a new line
        thicknessmode="pixels", thickness=20,
        lenmode="pixels", len=250))

    fig.update_coloraxes(colorbar_dtick=1) #only integers number separated by 1

    fig.update_geos(scope='world',
        visible=False,
        showcoastlines=True, coastlinecolor="#F6F6F4",
        showocean=True, oceancolor='#98BAD8',
        showland=True, landcolor="#F6F6F4", 
        projection_type = 'natural earth')

    fig.update_traces(marker=dict(
        line=dict(width=0)))

    fig.write_image(os.path.join(user_session, "world_map.png"))
    # fig.write_html(os.path.join(user_session, "world_map.html"))
    f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))


#PROJECT SIZE & BYTES
def projects_bytes(user_session, e_df, color_palette, f):
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

    user_readable_bytes = []
    for byte in bytes_list:
        user_readable_byte = byte/1024/1024
        user_readable_bytes.append(user_readable_byte)

    df['User_bites']=user_readable_bytes

    fig = px.histogram(df, x="Project", y="User_bites", color_discrete_sequence=color_palette)

    
    fig.update_layout(
        title = 'Project size', title_x=0.5,
        title_font_size=25,
        title_font_family='Times New Roman',
        yaxis_title="Bytes")
    
    
    fig.write_image(os.path.join(user_session, "projects_size&bytes_bar.png"))
    


    #BUBBLE PLOT
    fig = px.scatter(df, x='Project', y='User_bites', 
        size='User_bites', color='User_bites', size_max=100,
        color_continuous_scale = px.colors.sequential.haline, opacity = 0.95)
    
    fig.update_layout(
        title = 'Size of project', title_x=0.5,
        title_font_size=25,
        title_font_family='Times New Roman',
        yaxis_title="Megabyte",
        showlegend = True, 
        coloraxis_colorbar=dict(title="Megabyte",
        thicknessmode="pixels", thickness=20,
        lenmode="pixels", len=250))

    fig.write_image(os.path.join(user_session, "projects_size&bytes_bubble.png"))
    
    # with open('report_graph.html', 'a') as f:
    f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))

    fig.write_html(os.path.join(user_session, "projects_size&bytes_bubble.html"))
    

#reports
def experiment_report(user_session, e_df):
    
    color_palette =['rgb(41, 24, 107)', 'rgb(255, 230, 87)', 'rgb(62, 153, 134)', 'rgb(18, 92, 143)', 'rgb(145, 209, 96)']
    color_palette_hex =['#29186B', '#FFE657', '#3E9986', '#125C8F', '#91D160']
    with open(os.path.join(user_session,'report_graph.html'), 'a') as f:
        IDs_number(e_df)
        sample_number(user_session, e_df, color_palette)
        IDs_dates(user_session, e_df)
        scientific_name_pie(user_session, e_df, color_palette)
        scientific_name_bar(user_session, e_df, color_palette)
        library_source(user_session, e_df, color_palette)
        library_source_bar(user_session, e_df, color_palette)
        library_strategy_pie(user_session, e_df, color_palette)
        library_strategy_bar(user_session, e_df, color_palette)
        instrument_platform_pie(user_session, e_df, color_palette)
        instrument_platform_bar(user_session, e_df, color_palette)
        # library_layout_pie(user_session, e_df, color_palette)
        # library_layout_bar(user_session, e_df, color_palette, f)
        projects_bytes(user_session, e_df, color_palette, f)
        library_layout(user_session, e_df, color_palette_hex, f)

def publication_report(user_session, p_df):
    with open(os.path.join(user_session,'report_graph.html'), 'a') as f:
        color_palette =['rgb(41, 24, 107)', 'rgb(255, 230, 87)', 'rgb(62, 153, 134)', 'rgb(18, 92, 143)', 'rgb(145, 209, 96)']
        publication_title(user_session, p_df, color_palette)
        geography(user_session, p_df, f)
    
def final_screen(user_session):
    print(Color.BOLD + Color.GREEN + '\nReport was successfully created.' + Color.END,'You can find it here:', Color.BOLD + Color.YELLOW + f'{user_session}' + Color.END)
    input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue")



# def combine_plotly_figs_to_html(plotly_figs, html_fname, include_plotlyjs='cdn', 
#                                 separator=None, auto_open=False):
#     with open(html_fname, 'w') as f:
#         f.write(plotly_figs[0].to_html(include_plotlyjs=include_plotlyjs))
#         for fig in plotly_figs[1:]:
#             if separator:
#                 f.write(separator)
#             f.write(fig.to_html(full_html=False, include_plotlyjs=False))




    # n_colors = 20
    # colors = px.colors.sample_colorscale("turbo", [n/(n_colors -1) for n in range(n_colors)])
    # print(colors)