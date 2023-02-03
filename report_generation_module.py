from Utilities import Color, Utilities
import os
from os import path
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from Project import Project
import pycountry
from collections import Counter
from plotly.subplots import make_subplots
import numpy as np
from rich import print as rich_print
from rich.panel import Panel
from rich.text import Text


def report_generation(user_session):
    
    color_palette_hex = ['#29186B', '#FFE657', 'rgb(145, 209, 96)', 'rgb(97, 189, 115)', 'rgb(71, 165, 130)', 'rgb(56, 140, 135)', 'rgb(39, 117, 137)', 'rgb(18, 92, 143)', 'rgb(22, 62, 155)', 'rgb(42, 30, 138)']
    
    while True:
        Utilities.clear() 
        # title = " REPORT MODULE "
        # print(Color.BOLD + Color.PURPLE + title.center(100, '-') + Color.END)
        title = Panel(Text("REPORT MODULE", style = "b magenta", justify="center"), style = "b magenta")
        rich_print(title)

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
            input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")

        elif user_report_input.isnumeric() == True:
            user_report_input = int(user_report_input)
            if user_report_input not in (1,2):
                print(Color.BOLD + Color.RED +"Error" + Color.END,"enter a valid choice!")
                input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")

            else:

                if user_report_input == (1):
                    user_session = os.path.join("Downloads", user_session)
                    
                    report_folder = (os.path.join(user_session, 'Report_images'))
                    if not os.path.exists(report_folder):
                        os.makedirs(report_folder)
                    
                    file_count = check_files(user_session)
                    if file_count == 0:
                        print(Color.BOLD + Color.RED + "\nError" + Color.END, "found 0 file. Is it the correct folder? Note that the file names must end with '_merged_experiments-metadata.tsv' and '_merged_publications-metadata.tsv'\n")
                        input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")

                    if file_count == 1:
                        merged_experiments = check_file_experiments(user_session)
                        e_df = read_experiments(user_session, merged_experiments)
                        report(user_session, report_folder, color_palette_hex ,e_df, p_df = None)
                        final_screen(user_session)


                    if file_count == 2:
                        merged_experiments = check_file_experiments(user_session)
                        e_df = read_experiments(user_session, merged_experiments)
                        merged_publications = check_file_publications(user_session)
                        p_df = read_publications(user_session, merged_publications)
                        report(user_session, report_folder, color_palette_hex ,e_df, p_df)
                        final_screen(user_session)

                    if file_count > 2:
                        print(Color.BOLD + Color.RED + "\nError" + Color.END, "found too many files. Please choose a folder containing only 1 '*_merged_experiments-metadata.tsv'")
                        input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")
                    
                    

                if user_report_input == (2):
                    user_report_local_path = user_report_local(user_session)
                    if user_report_local_path == 0:
                        break
                    file_count = check_files(user_report_local_path)
                    if file_count == 0:
                        print(Color.BOLD + Color.RED + "\nError" + Color.END, "found 0 file. Is it the correct folder? Note that the file names must end with '_merged_experiments-metadata.tsv' and '_merged_publications-metadata.tsv'\n")
                        input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")

                    if file_count == 1:
                        merged_experiments = check_file_experiments(user_report_local_path)
                        e_df = read_experiments(user_report_local_path, merged_experiments)
                        report(user_session, report_folder, color_palette_hex ,e_df, p_df = None)
                        final_screen(user_session)

                    if file_count == 2:
                        merged_experiments = check_file_experiments(user_report_local_path)
                        e_df = read_experiments(user_report_local_path, merged_experiments)
                        merged_publications = check_file_publications(user_report_local_path)
                        p_df = read_publications(user_report_local_path, merged_publications)
                        report(user_session, report_folder, color_palette_hex ,e_df, p_df)
                        final_screen(user_session)

                    if file_count > 2:
                        print(Color.BOLD + Color.RED + "\nError" + Color.END, "found too many files. Please choose a folder containing only 1 '*_merged_experiments-metadata.tsv' & 1 '*_merged_publications-metadata.tsv' ")
                        input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")
                    

def user_report_local(user_session):
    Utilities.clear()
    while True:
        # title = " REPORT MODULE "
        # print(Color.BOLD + Color.PURPLE + title.center(100, '-') + Color.END)
        title = Panel(Text("REPORT MODULE", style = "b magenta", justify="center"), style = "b magenta")
        rich_print(title)
        
        print("\nEnter the path for '*_merged_experiments-metadata.tsv' & '*_merged_publications-metadata.tsv' files. \nThe report will be downloaded in the folder indicated.")
        print("\n >>> Your current session is " + Color.BOLD + Color.YELLOW +f"{user_session}" + Color.END + " <<<\n")
        print(" --- If you want to return to the main menu digit: " + Color.BOLD + Color.PURPLE + "main menu" + Color.END + " ---\n") #verificare se è vero o se torna al report
        user_report_local_path = input("\n>> Digit the path: ").strip()

        if user_report_local_path in ("main menu", "MAIN MENU", "Main menu"):
            return 0
                            
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


#report functions
#INITIAL TABLE
def initial_table(report_folder, e_df, p_df, f):

    first_column = ['Total number of projects with available metadata', 'Total number of projects with available data', 'Total number of samples', 'Total number of scientific names', 
        'Total number of library source','Total number of library strategies','Total number of instrument platforms',
        'Total number of library layouts', 'Year of the oldest project', 'Year of the most recent project', 'Total number of countries']
    second_column = []
    
    
    for column in ['study_accession', 'fastq_bytes', 'run_accession','scientific_name', 'library_source','library_strategy','instrument_platform', 'library_layout', 'first_public', 'last_updated']:
        if pd.Series(column).isin(e_df.columns).all():
            if column == 'fastq_bytes':
                subset = e_df[['fastq_bytes','submitted_bytes','sra_bytes']]
                e_df['bytes_availability'] = subset.isna().all(axis=1) #check for empty cells
                non_available_data_projs = e_df.query("bytes_availability==True")["study_accession"].tolist() #get project corresponding to empty cells
                non_available_data_projs_norep = [*set(non_available_data_projs)] #remove replicates
                all_data_projs = e_df['study_accession'].nunique()
                available_data_projs =  all_data_projs- len(non_available_data_projs_norep)
                second_column.append(available_data_projs)
            elif column == 'run_accession':
                value = e_df[column].count()
                second_column.append(value)
            elif column == 'first_public':
                e_df['first_public'] = pd.to_datetime(e_df['first_public'],  errors='coerce', infer_datetime_format=True)
                e_df['first_public_year'] = e_df['first_public'].dt.year
                value_f = e_df['first_public_year'].min()
                second_column.append(value_f)
            elif column == 'last_updated':
                e_df['last_updated'] = pd.to_datetime(e_df['last_updated'],  errors='coerce', infer_datetime_format=True)
                e_df['last_updated_year'] = e_df['last_updated'].dt.year
                value_l = e_df['last_updated_year'].max()
                second_column.append(value_l)
            else:
                value = e_df[column].nunique()
                second_column.append(value)

    for column in ['affiliation']:
        if pd.Series(column).isin(p_df.columns).all():
            country_list = []
            affiliation_list = p_df['affiliation'].tolist()
            for affiliation in affiliation_list:
                for country in pycountry.countries: #extract the name of the country from a string, in this case the affiliation
                    if country.name in affiliation:
                        country_list.append(country.name)
            
            input =  country_list
            c = Counter(input) #counter of countries
            country_df = pd.DataFrame(c.items(), columns = ['country', 'count'])
            country_number = country_df['country'].nunique()
            second_column.append(country_number)



    values = [first_column, second_column]


    fig = go.Figure(data=[go.Table(
    columnorder = [1,2],
    columnwidth = [200,200],
    header = dict(
        values = [['DESCRIPTION'],
                    ['<b></b>']],
        line_color='#29186B',
        line_width = 3,
        fill_color='#29186B',
        align=['center','center'],
        font=dict(color='white', family='Times New Roman', size=30),
        height=40
    ),
    cells=dict(
        values=values,
        line_color='lavender',
        line_width = 3,
        fill_color='white',
        align=['center', 'center'],
        font=dict(color='black', family='Times New Roman', size=25),
        height=35
        ))
    ])

    fig.update_layout(title_text='Summary information<br><br><br><br><br><br><br><br>', title_x=0.5, title_font = dict(family='Times New Roman', size=40))
    fig.write_html(os.path.join(report_folder, "Sample number.html"))
    f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    


def sample_number(report_folder, e_df, f):
    sample_number_series = e_df.groupby(['study_accession'])['run_accession'].count()
    sample_number_df = pd.DataFrame(sample_number_series).reset_index()
    sample_number_df.columns = ['Project', 'Number of samples']
    fig = px.bar(sample_number_df, x="Project", y="Number of samples", color="Number of samples", 
        color_continuous_scale = ['rgb(41, 24, 107)', 'rgb(42, 30, 138)', 'rgb(38, 41, 159)', 'rgb(22, 62, 155)', 
        'rgb(16, 79, 150)', 'rgb(18, 92, 143)', 'rgb(27, 105, 140)', 'rgb(39, 117, 137)', 'rgb(47, 129, 136)', 
        'rgb(56, 140, 135)', 'rgb(62, 153, 134)', 'rgb(71, 165, 130)', 'rgb(80, 177, 124)', 'rgb(97, 189, 115)', 
        'rgb(116, 200, 105)', 'rgb(145, 209, 96)', 'rgb(174, 217, 97)', 'rgb(255, 230, 87)'])
    fig.update_layout(title_text='Number of samples', title_x=0.5, title_font = dict(family='Times New Roman', size=40),
                barmode='stack', legend_title_text="Number of samples<br>", legend=dict(#title_font_family="Times New Roman",#, font=dict(size= 20),
                bordercolor="lavenderblush", borderwidth=3))
    fig.update_xaxes(title_text= "project", title_font=dict(family='Times New Roman', size=25))
    fig.update_yaxes(title_text= "number of samples",title_font=dict(family='Times New Roman', size=25))
    fig.write_image(os.path.join(report_folder, "Sample number.png"), width=1920, height=1080)
    fig.write_html(os.path.join(report_folder, "Sample number.html"))
    f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
        

def pie_and_bar_charts(report_folder, e_df, color_palette_hex, f):
    
    for column in ['scientific_name', 'library_source','library_strategy','instrument_platform', 'library_layout']:
        if pd.Series(column).isin(e_df.columns).all():
            library_layout_df = e_df[column].value_counts() #df for pie
            df_pie = pd.DataFrame(library_layout_df).reset_index()
            column_name = column.capitalize().replace('_', ' ')
            df_pie.columns = [column_name, 'Counts']
            
            library_layout_IDs_df = e_df.groupby(['study_accession'])[column].value_counts() #df for bar
            df_bar = library_layout_IDs_df.rename('count').reset_index()
            column_name = column.capitalize().replace('_', ' ')
            df_bar.columns = ['Project', column_name, 'Counts']

            color_dictionary = dict(zip(df_bar[column_name].unique(), color_palette_hex)) #associate column values to color
            df_bar['Color'] = df_bar[column_name].map(color_dictionary) #create a new column based on dictionary mapping another column
            
            fig = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "bar"}]])
            
            fig.add_trace(go.Pie(labels=df_pie[column_name], values=df_pie['Counts'], hole=0.6, 
                marker_colors= df_pie[column_name].map(color_dictionary), showlegend=False, 
                hovertemplate = "Layout: %{label} <br>Percentage of samples: %{percent}<extra></extra>"),#, textfont_size=20),
                row=1, col=1)

            for c in df_bar[column_name].unique(): #to create the legend use loop for
                df_color= df_bar[df_bar[column_name] == c]
                fig.add_trace(go.Bar(x=df_color["Project"], y = df_color["Counts"], marker_color = df_color['Color'],
                    text = df_color[column_name], textposition = "none", name = c, 
                    showlegend = True, hovertemplate = "Layout: %{text} <br>Number of samples: %{y}<extra></extra>"),
                    row=1, col=2)
                
            fig.update_layout(title_text=f'{column_name}', title_x=0.5, title_font = dict(family='Times New Roman', size=40),
                barmode='stack', legend_title_text=f"{column_name}<br>", legend=dict(#title_font_family="Times New Roman",# font=dict(size= 20),
                bordercolor="lavenderblush", borderwidth=3))
            fig.update_xaxes(title_text= "project", title_font=dict(family='Times New Roman', size=25))
            fig.update_yaxes(title_text= "number of samples",title_font=dict(family='Times New Roman', size=25))
            fig.write_image(os.path.join(report_folder, f"{column_name}.png"), width=1920, height=1080)
            fig.write_html(os.path.join(report_folder, f"{column_name}.html"))
            f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
        else:
            print(f'{column_name} column missing')


#PROJECT SIZE & BYTES
def projects_size(report_folder, e_df, f):
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
    file_name = os.path.join(report_folder,'Project_size.xlsx')
    df.to_excel(file_name)

    user_Megabytes = []
    for byte in bytes_list:
        user_bytes = byte/1024/1024
        user_Megabytes.append(user_bytes)

    df['User_Megabytes']=user_Megabytes

    #HISTOGRAM >> da eliminare se basta bubble
    # fig = px.histogram(df, x="Project", y="User_bites", color_discrete_sequence=color_palette)
    # fig.update_layout(
    #     title = 'Project size', title_x=0.5,
    #     title_font_size=25,
    #     title_font_family='Times New Roman',
    #     yaxis_title="Bytes")
    # fig.write_image(os.path.join(user_session, "projects_size&bytes_bar.png"))
   
    #BUBBLE PLOT
    fig = px.scatter(df, x='Project', y='User_Megabytes', 
        size='User_Megabytes', color='User_Megabytes', size_max=100,
        color_continuous_scale = ['rgb(41, 24, 107)', 'rgb(42, 30, 138)', 'rgb(38, 41, 159)', 'rgb(22, 62, 155)', 
        'rgb(16, 79, 150)', 'rgb(18, 92, 143)', 'rgb(27, 105, 140)', 'rgb(39, 117, 137)', 'rgb(47, 129, 136)', 
        'rgb(56, 140, 135)', 'rgb(62, 153, 134)', 'rgb(71, 165, 130)', 'rgb(80, 177, 124)', 'rgb(97, 189, 115)', 
        'rgb(116, 200, 105)', 'rgb(145, 209, 96)', 'rgb(174, 217, 97)', 'rgb(255, 230, 87)'], opacity = 0.8)

    fig.update_layout(title = 'Project size', title_x=0.5, title_font = dict(family='Times New Roman', size=40),
        showlegend = True, coloraxis_colorbar=dict(title="Megabyte", 
        thicknessmode="pixels", thickness=20,
        lenmode="pixels", len=500))
    
    fig.update_coloraxes(colorbar_title_text="Megabyte")#, colorbar_title_font_family='Times New Roman', colorbar_title_font_size=20) #nuovo
    fig.update_xaxes(title_text= "project", title_font=dict(family='Times New Roman', size=25))
    fig.update_yaxes(title_text= "megabytes",title_font=dict(family='Times New Roman', size=25))
    fig.update_traces(hovertemplate = "Project: %{x} <br>Megabytes: %{y:,.3f}<br><extra></extra>")

    fig.write_image(os.path.join(report_folder, "Projects size.png"), width=1920, height=1080)
    fig.write_html(os.path.join(report_folder, "Projects size.html"))
    f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))


def IDs_dates(report_folder, e_df, f):
    cols = ['first_public', 'last_updated']
    if pd.Series(['first_public', 'last_updated']).isin(e_df.columns).all():
        # e_df['first_public'] = pd.to_datetime(e_df['first_public'],  errors='coerce', infer_datetime_format=True) #convert into datatype
        # e_df['last_updated'] = pd.to_datetime(e_df['last_updated'], errors='coerce', infer_datetime_format=True)
        # e_df['first_public_year'] = e_df['first_public'].dt.year #create a new column with only year
        # e_df['last_updated_year'] = e_df['last_updated'].dt.year
        collapsed_e_df = e_df.groupby('study_accession').first().reset_index()
        collapsed_e_df = collapsed_e_df.sort_values(by=['first_public'], ascending=True)
        collapsed_e_df_f = collapsed_e_df[['study_accession', 'first_public']]
        collapsed_e_df_l = collapsed_e_df[['study_accession', 'last_updated']]
        collapsed_e_list_f_x = collapsed_e_df_f.study_accession.values.tolist()
        collapsed_e_list_f_y = collapsed_e_df_f.first_public.values.tolist()
        collapsed_e_list_l_x = collapsed_e_df_l.study_accession.values.tolist()
        collapsed_e_list_l_y = collapsed_e_df_l.last_updated.values.tolist()

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=collapsed_e_list_f_x,
            y=collapsed_e_list_f_y,
            marker=dict(color='rgb(41, 24, 107)', size=30, 
                line=dict(color='rgb(41, 24, 107)', width=10)),
            mode="markers",
            name="Year of first update",
            opacity=0.65,
            hovertemplate = "<b>First update </b><br>Project: %{x} <br>Year: %{y}<br><extra></extra>"
        ))
        
        fig.add_trace(go.Scatter(
            x= collapsed_e_list_l_x,
            y=collapsed_e_list_l_y,
            marker=dict(color='rgb(250, 214, 0)', size=30, 
                line=dict(color='rgb(250, 214, 0)', width=10)),
            mode="markers",
            name="Year of last update",
            opacity=0.65,
            hovertemplate = "<b>Last update </b><br>Project: %{x} <br>Year: %{y}<br><extra></extra>"
        ))

        fig.update_layout(title_text="Year of first and last update", title_x=0.5, title_font = dict(family='Times New Roman', size=40),
                    legend_title_text="Updates<br>", legend=dict(#title_font_family="Times New Roman", #font=dict(size= 20),
                    bordercolor="lavenderblush", borderwidth=3),
                    hovermode='x') #to see both hover labels
        fig.update_xaxes(title_text= "project", title_font=dict(family='Times New Roman', size=25))
        fig.update_yaxes(title_text= "year",title_font=dict(family='Times New Roman', size=25),
            type="category", categoryorder='category ascending') #make years as categorical and sort them
        fig.write_image(os.path.join(report_folder, "Years update.png"), width=1920, height=1080)
        fig.write_html(os.path.join(report_folder, "Years update.html"))
        f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))

    else:
        print('first_public and last_updated columns missing')


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

def geography(report_folder, p_df, f):
    
    # for column in ['affiliation']:
    #     if pd.Series(column).isin(p_df.columns).all():
    #         p_df['affiliation'] = p_df['affiliation'].str.replace('USA','United States') # pycountry non riconosce US o USA e quindi non lo include
            
            #collapsed_p_df = p_df.groupby(['project_id', 'affiliation']).count()





    try:
        p_df['affiliation'] = p_df['affiliation'].str.replace('USA','United States') #attenzione: sostituire tutti quelli che immaginiamo possano essere scritti in un  modo che pycountry non voglia
        # qui link: https://github.com/flyingcircusio/pycountry/blob/main/src/pycountry/databases/iso3166-1.json
        country_list = []
        affiliation_list = p_df['affiliation'].tolist()
        for affiliation in affiliation_list:
            for country in pycountry.countries: #extract the name of the country from a string, in this case the affiliation
                if country.name in affiliation:
                    country_list.append(country.name)


        print(country_list)
        print(p_df['project_id'])
        p_df['country'] = country_list
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        print(p_df)

        collapsed_p_df = p_df.groupby(['project_id', 'country']).count() #CONTINUARE DA QUI: USARE COLLAPSED PER FARE GRAFICO

        
        input =  country_list
        c = Counter(input) #counter of countries
        country_df = pd.DataFrame(c.items(), columns = ['country', 'count'])
        country_number = country_df['country'].nunique()
        country_df['CODE']=alpha3code(country_df.country) #call alpha3code to create ISO3 column
        country_df.columns = ['Country', 'Count', 'CODE']

        fig = px.scatter_geo(country_df, locations="CODE", color = 'Count', size="Count", 
            color_continuous_scale=['rgb(41, 24, 107)', 'rgb(42, 30, 138)', 'rgb(38, 41, 159)', 'rgb(22, 62, 155)', 
            'rgb(16, 79, 150)', 'rgb(18, 92, 143)', 'rgb(27, 105, 140)', 'rgb(39, 117, 137)', 'rgb(47, 129, 136)', 
            'rgb(56, 140, 135)', 'rgb(62, 153, 134)', 'rgb(71, 165, 130)', 'rgb(80, 177, 124)', 'rgb(97, 189, 115)', 
            'rgb(116, 200, 105)', 'rgb(145, 209, 96)', 'rgb(174, 217, 97)', 'rgb(255, 230, 87)'], opacity = 0.95, size_max=30,
            hover_data = {'CODE':False,'Country':True,'Count': True})
            

        fig.update_layout(
            title = 'Map of publications', title_x=0.5,
            title_font = dict(family='Times New Roman', size=40),
            showlegend = True, coloraxis_colorbar=dict(title="Number of <br>publications", 
            thicknessmode="pixels", thickness=20,
            lenmode="pixels", len=500))
        
        fig.update_coloraxes(colorbar_title_text="Number of <br>publications<br>", #colorbar_title_font_family='Times New Roman', colorbar_title_font_size=20, 
            colorbar_dtick=1) #only integers number separated by 1

        fig.update_geos(scope='world',
            visible=False,
            showcoastlines=True, coastlinecolor="#F6F6F4",
            showocean=True, oceancolor='#98BAD8',
            showland=True, landcolor="#F6F6F4", 
            projection_type = 'natural earth')

        fig.update_traces(marker=dict(line=dict(width=0)))

        fig.write_image(os.path.join(report_folder, "Map of publications.png"), width=1920, height=1080)
        fig.write_html(os.path.join(report_folder, "Map of publications.html"))
        f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))

    except TypeError:
        print('"_merged_publications-metadata.tsv" file missing')
    

#reports
def report(user_session, report_folder, color_palette_hex ,e_df, p_df = None):
    report_html = os.path.join(user_session,f'Report_{os.path.basename(user_session)}.html')
    
    with open(report_html, 'w+') as f:

        initial_table(report_folder, e_df, p_df, f)
        sample_number(report_folder, e_df, f)
        pie_and_bar_charts(report_folder, e_df, color_palette_hex, f)
        projects_size(report_folder, e_df, f)
        IDs_dates(report_folder, e_df, f)
        geography(report_folder, p_df, f)
    
def final_screen(user_session):
    print(Color.BOLD + Color.GREEN + '\nReport successfully created.' + Color.END,'You can find the', Color.UNDERLINE + 'Report in HTML format' + Color.END, 
    'and the', Color.UNDERLINE + 'Report folder' + Color.END,'here:', Color.BOLD + Color.YELLOW + f'{os.path.basename(user_session)}' + Color.END)
    input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")
    return




#######################################################################################PUò SERVIRE?############################################################################################
# def publication_title(user_session, p_df,color_palette):
#     p_list_project = p_df.input_accession_id.values.tolist()
#     p_list_title = p_df.title.values.tolist()
#     d = {
#         'Project': p_list_project,
#         'Publication title': p_list_title
#         }
#     df = pd.DataFrame(data=d)
#     file_name = os.path.join(user_session,'Publication_title.xlsx')
#     df.to_excel(file_name)

################################################################VECCHIO MATERIALE SOSTITUITO DA PIE_AND_BAR_CHARTS############################################################################
# def scientific_name_pie(user_session, e_df, color_palette):
#     col = ['scientific_name']
#     if pd.Series(['scientific_name']).isin(e_df.columns).all():
#         scientific_name_df = e_df['scientific_name'].value_counts()
#         df = pd.DataFrame(scientific_name_df).reset_index()
#         df.columns = ['Scientific name', 'Counts']
#         fig = px.pie(df, values='Counts', names='Scientific name', color_discrete_sequence=color_palette)
#         fig.write_image(os.path.join(user_session, "scientific_name_pie.png"))
#     else:
#         pass


# def scientific_name_bar(user_session, e_df, color_palette):
#     col = ['scientific_name']
#     if pd.Series(['scientific_name']).isin(e_df.columns).all():
#         scientific_name_IDs_df = e_df.groupby(['study_accession'])['scientific_name'].value_counts()
#         df_bar = scientific_name_IDs_df.rename('count').reset_index()
#         df_bar.columns = ['Project', 'Scientific name', 'Counts']
#         fig = px.histogram(df_bar, x="Project", y="Counts",
#                 color='Scientific name', color_discrete_sequence=color_palette, 
#                 height=400).update_layout(yaxis_title="Number of samples")
#         fig.write_image(os.path.join(user_session, "scientific_name_bar.png"))
#     else:
#         pass


# def library_source(user_session, e_df, color_palette):
#     col = ['library_source']
#     if pd.Series(['library_source']).isin(e_df.columns).all():
#         library_source_df = e_df['library_source'].value_counts()
#         df = pd.DataFrame(library_source_df).reset_index()
#         df.columns = ['Library source', 'Counts']
#         fig = px.pie(df, values='Counts', names='Library source', color_discrete_sequence=color_palette)
#         fig.write_image(os.path.join(user_session, "library_source_pie.png"))
#     else:
#         pass


# def library_source_bar(user_session, e_df, color_palette):
#     col = ['library_source']
#     if pd.Series(['library_source']).isin(e_df.columns).all():
#         library_source_IDs_df = e_df.groupby(['study_accession'])['library_source'].value_counts()
#         df_bar = library_source_IDs_df.rename('count').reset_index()
#         df_bar.columns = ['Project', 'Library source', 'Counts']
#         fig = px.histogram(df_bar, x="Project", y="Counts",
#                 color='Library source',
#                 color_discrete_sequence=color_palette,
#                 height=400).update_layout(yaxis_title="Number of samples")
#         fig.write_image(os.path.join(user_session, "library_source_bar.png"))
#     else:
#         pass


# def library_strategy_pie(user_session, e_df, color_palette):
#     col = ['library_strategy']
#     if pd.Series(['library_strategy']).isin(e_df.columns).all():
#         library_strategy_df = e_df['library_strategy'].value_counts()
#         df = pd.DataFrame(library_strategy_df).reset_index()
#         df.columns = ['Library strategy', 'Counts']
#         fig = px.pie(df, values='Counts', names='Library strategy', color_discrete_sequence=color_palette)
#         fig.write_image(os.path.join(user_session, "library_strategy_pie.png"))
#     else:
#         pass


# def library_strategy_bar(user_session, e_df, color_palette):
#     col = ['library_strategy']
#     if pd.Series(['library_strategy']).isin(e_df.columns).all():
#         library_strategy_IDs_df = e_df.groupby(['study_accession'])['library_strategy'].value_counts()
#         df_bar = library_strategy_IDs_df.rename('count').reset_index()
#         df_bar.columns = ['Project', 'Library strategy', 'Counts']
#         fig = px.histogram(df_bar, x="Project", y="Counts",
#                 color='Library strategy',
#                 color_discrete_sequence=color_palette,
#                 height=400).update_layout(yaxis_title="Number of samples")
#         fig.write_image(os.path.join(user_session, "library_strategy_bar.png"))
#     else:
#         pass


# def instrument_platform_pie(user_session, e_df, color_palette):#, color_palette): #
#     col = ['instrument_platform']
#     if pd.Series(['instrument_platform']).isin(e_df.columns).all():
#         instrument_platform_df = e_df['instrument_platform'].value_counts()
#         df = pd.DataFrame(instrument_platform_df).reset_index()
#         df.columns = ['Instrument platform', 'Counts']
#         fig = px.pie(df, values='Counts', names='Instrument platform', color_discrete_sequence=color_palette) #
#         fig.write_image(os.path.join(user_session, "instrument_platform_pie.png"))
#     else:
#         pass


# def instrument_platform_bar(user_session, e_df, color_palette):
#     col = ['instrument_platform']
#     if pd.Series(['instrument_platform']).isin(e_df.columns).all():
#         instrument_platform_IDs_df = e_df.groupby(['study_accession'])['instrument_platform'].value_counts()
#         df_bar = instrument_platform_IDs_df.rename('count').reset_index()
#         df_bar.columns = ['Project', 'Instrument platform', 'Counts']
#         fig = px.histogram(df_bar, x="Project", y="Counts",
#                 color='Instrument platform',
#                 color_discrete_sequence=color_palette,
#                 height=400).update_layout(yaxis_title="Number of samples")
#         fig.write_image(os.path.join(user_session, "instrument_platform_bar.png"))
#     else:
#         pass

# def instrument_platform(report_folder, e_df, color_palette_hex, f): ########colonne check
#     col = ['instrument_platform']
#     if pd.Series(['instrument_platform']).isin(e_df.columns).all():
#         instrument_platform_df = e_df['instrument_platform'].value_counts()
#         df_pie = pd.DataFrame(instrument_platform_df).reset_index()
#         df_pie.columns = ['Instrument platform', 'Counts']

#         instrument_platform_IDs_df = e_df.groupby(['study_accession'])['instrument_platform'].value_counts()
#         df_bar = instrument_platform_IDs_df.rename('count').reset_index()
#         df_bar.columns = ['Project', 'Instrument platform', 'Counts']

#         color_dictionary = dict(zip(df_bar['Instrument platform'].unique(), color_palette_hex)) #associate column values to color
#         df_bar['Color'] = df_bar['Instrument platform'].map(color_dictionary) #create a new column based on dictionary mapping another column

#         fig = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "bar"}]])

#         fig.add_trace(go.Pie(labels=df_pie["Instrument platform"], values=df_pie['Counts'], hole=0.6, 
#             marker_colors= df_bar['Color'], showlegend=False, hovertemplate = "Layout: %{label} <br>Percentage of samples: %{percent}<extra></extra>", textfont_size=20),
#             row=1, col=1)

#         for c in df_bar['Instrument platform'].unique(): #to create the legend use loop for
#             df_color= df_bar[df_bar['Instrument platform'] == c]
#             fig.add_trace(go.Bar(x=df_color["Project"], y = df_color["Counts"], marker_color = df_color['Color'],
#                 text = df_color['Instrument platform'], textposition = "none", name = c, 
#                 showlegend = True, hovertemplate = "Layout: %{text} <br>Number of samples: %{y}<extra></extra>"),
#                 row=1, col=2)

#         fig.update_layout(title_text="Instrument platform", title_x=0.5, title_font = dict(family='Times New Roman', size=40),
#                 barmode='stack', legend_title_text="Instrument platform<br>", legend=dict(title_font_family="Times New Roman", font=dict(size= 20),
#                 bordercolor="lavenderblush", borderwidth=3))
#         fig.update_xaxes(title_text= "project", title_font=dict(family='Times New Roman', size=25))
#         fig.update_yaxes(title_text= "number of samples",title_font=dict(family='Times New Roman', size=25))
#         fig.write_image(os.path.join(report_folder, "Instrument platform.png"), width=1920, height=1080)
#         fig.write_html(os.path.join(report_folder, "Instrument platform.html"))
#     else:
#         print('Instrument platform column missing')
    

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


# #library_layout
# def library_layout(report_folder, e_df, color_palette_hex, f):
#     col = ['library_layout']
#     if pd.Series(['library_layout']).isin(e_df.columns).all():
#         library_layout_df = e_df['library_layout'].value_counts()
#         df_pie = pd.DataFrame(library_layout_df).reset_index()
#         df_pie.columns = ['Library layout', 'Counts']
        
#         library_layout_IDs_df = e_df.groupby(['study_accession'])['library_layout'].value_counts()
#         df_bar = library_layout_IDs_df.rename('count').reset_index()
#         df_bar.columns = ['Project', 'Library layout', 'Counts']

#         color_dictionary = dict(zip(df_bar['Library layout'].unique(), color_palette_hex)) #associate column values to color
#         df_bar['Color'] = df_bar['Library layout'].map(color_dictionary) #create a new column based on dictionary mapping another column
        
#         fig = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "bar"}]])
        
#         fig.add_trace(go.Pie(labels=df_pie["Library layout"], values=df_pie['Counts'], hole=0.6, 
#         marker_colors= df_pie["Library layout"].map(color_dictionary), showlegend=False, 
#         hovertemplate = "Layout: %{label} <br>Percentage of samples: %{percent}<extra></extra>", textfont_size=20),
#             row=1, col=1)

#         for c in df_bar['Library layout'].unique(): #to create the legend use loop for
#             df_color= df_bar[df_bar['Library layout'] == c]
#             fig.add_trace(go.Bar(x=df_color["Project"], y = df_color["Counts"], marker_color = df_color['Color'],
#             text = df_color['Library layout'], textposition = "none", name = c, 
#             showlegend = True, hovertemplate = "Layout: %{text} <br>Number of samples: %{y}<extra></extra>"),
#             row=1, col=2)
            
#         fig.update_layout(title_text="Library layout", title_x=0.5, title_font = dict(family='Times New Roman', size=40),
#                 barmode='stack', legend_title_text="Library layout<br>", legend=dict(title_font_family="Times New Roman", font=dict(size= 20),
#                 bordercolor="lavenderblush", borderwidth=3))
#         fig.update_xaxes(title_text= "project", title_font=dict(family='Times New Roman', size=25))
#         fig.update_yaxes(title_text= "number of samples",title_font=dict(family='Times New Roman', size=25))
#         fig.write_image(os.path.join(report_folder, "Library layout.png"), width=1920, height=1080)
#         fig.write_html(os.path.join(report_folder, "Library layout.html"))
#     else:
#         print('library_layout column missing')