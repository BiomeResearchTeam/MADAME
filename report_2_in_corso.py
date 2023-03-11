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
import glob

def report_generation(user_session):
    """
    main function
    """
    
    while True:
        Utilities.clear() 
        title = Panel(Text("REPORT MODULE", style = "b magenta", justify="center"), style = "b magenta", expand=False, width = 300)
        rich_print(title)

        print("\nGenerate a report file about the information present in the downloaded metadata & publications files. \n\nChoose one of the following options:")
        print(" 1 - Use '*_merged_experiments-metadata.tsv' & '*_merged_publications-metadata.tsv' files present the current session")
        print(" 2 - Use '*_merged_experiments-metadata.tsv' & '*_merged_publications-metadata.tsv' files present in any other location of your computer")
        print("\n >>> Your current session is " + Color.BOLD + Color.YELLOW +f"{user_session}" + Color.END + " <<<\n")
        print(" --- If you want to return to the main menu digit: " + Color.BOLD + Color.PURPLE + "main menu" + Color.END + " ---\n")
        user_report_input = input("\n>> Enter your choice: ").strip().lower()
        
        if user_report_input in ("main menu"):
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
                if user_report_input == 1:
                    user_session = os.path.join("Downloads", user_session)
                    available_metadata_files(user_session) 

                if user_report_input == 2:
                    user_report_local(user_session)


def user_report_local(user_session):
    """
    user digit path to '*_merged_experiments-metadata.tsv' & '*_merged_publications-metadata.tsv' files. check if path exists, if it is so recall 'available_metadata_files' function
    """
    while True:
        Utilities.clear()
        title = Panel(Text("REPORT MODULE", style = "b magenta", justify="center"), style = "b magenta")
        rich_print(title)
        
        print("\nDigit the path to the folder containing '*_merged_experiments-metadata.tsv' & '*_merged_publications-metadata.tsv' files. \nThe report will be downloaded in the folder indicated.")
        print("\n >>> Your current session is " + Color.BOLD + Color.YELLOW +f"{user_session}" + Color.END + " <<<\n")
        print(" --- If you want to go back digit: " + Color.BOLD + Color.PURPLE + "back" + Color.END + " ---\n")
        user_path = input("\n>> Digit the path: ").strip()

        if user_path in ("back", "BACK", "Back"):
            return

        elif os.path.exists(user_path) == False:
            print(Color.BOLD + Color.RED + "Error, this path doesn't exist" + Color.END, "Maybe a typo? Try again")
            input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue")
            continue
        
        elif os.path.exists(user_path) == True:
            user_session = user_path
            available_metadata_files(user_session)



def available_metadata_files(user_session):
    """
    create list of available MADAME metadata files. check it and generate the report
    """
    metadata_files = ["_merged_experiments-metadata.tsv","_merged_publications-metadata.tsv"]
    possible_metadata_files = [file for file in os.listdir(user_session) if file.endswith("-metadata.tsv")]
    list_metadata_files = [file for file in possible_metadata_files if file.endswith(tuple(metadata_files))]
    list_metadata_files = sorted(list_metadata_files)
     
    available_metadata_files = len(list_metadata_files)

    if available_metadata_files == 0:
        print(Color.BOLD + Color.RED + "\nError found 0 file" + Color.END, "Is it the correct folder? Note that the files names must end with '_merged_experiments-metadata.tsv' and '_merged_publications-metadata.tsv'\n")
        input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")
    
    elif available_metadata_files == 1:
        print(Color.BOLD + Color.GREEN + "\nFound" + Color.END, f"{list_metadata_files[0]}")
        e_df_path = os.path.join(user_session, list_metadata_files[0])
        e_df = pd.read_csv (e_df_path, delimiter='\t', infer_datetime_format=True)
        report(user_session, e_df, p_df = None)
        final_screen(user_session)

    elif available_metadata_files == 2:
        print(Color.BOLD + Color.GREEN + "\nFound" + Color.END, f"{list_metadata_files[0]}")
        print(Color.BOLD + Color.GREEN + "\nFound" + Color.END, f"{list_metadata_files[1]}")
        e_df_path = os.path.join(user_session, list_metadata_files[0])
        e_df = pd.read_csv (e_df_path, delimiter='\t', infer_datetime_format=True)
        p_df_path = os.path.join(user_session, list_metadata_files[1])
        p_df = pd.read_csv (p_df_path, delimiter='\t', infer_datetime_format=True)
        report(user_session, e_df, p_df)
        final_screen(user_session)


#reports
def report(user_session, e_df, p_df = None): 
    """
    report generation based on how many '*_merged_<experiment or publication>-metadata.tsv' files are present in the folder.
    create a report folder that will contain all plots in png format, create a single html that will contain all plots 
    """
    color_palette_hex = ['#29186B', '#FFE657', 'rgb(145, 209, 96)', 'rgb(97, 189, 115)', 'rgb(71, 165, 130)', 'rgb(56, 140, 135)', 'rgb(39, 117, 137)', 'rgb(18, 92, 143)', 'rgb(22, 62, 155)', 'rgb(42, 30, 138)']
    color_palette = ['rgb(41, 24, 107)', 'rgb(42, 30, 138)', 'rgb(38, 41, 159)', 'rgb(22, 62, 155)', 
        'rgb(16, 79, 150)', 'rgb(18, 92, 143)', 'rgb(27, 105, 140)', 'rgb(39, 117, 137)', 'rgb(47, 129, 136)', 
        'rgb(56, 140, 135)', 'rgb(62, 153, 134)', 'rgb(71, 165, 130)', 'rgb(80, 177, 124)', 'rgb(97, 189, 115)', 
        'rgb(116, 200, 105)', 'rgb(145, 209, 96)', 'rgb(174, 217, 97)', 'rgb(255, 230, 87)']


    report_folder = (os.path.join(user_session, 'Report_images'))
    if not os.path.exists(report_folder):
        os.makedirs(report_folder)
    
    report_html = os.path.join(user_session,f'Report_{os.path.basename(user_session)}.html')
    
    with open(report_html, 'w+') as f:
        initial_table(report_folder, e_df, p_df, f)
        sample_number(report_folder, e_df, color_palette, f)
        pie_and_bar_charts(report_folder, e_df, color_palette_hex, f)
        projects_size(report_folder, e_df, f)
        IDs_dates(report_folder, e_df, f)
        geography(report_folder, p_df, f)


#report functions
#INITIAL TABLE
def initial_table(report_folder, e_df, p_df, f):
    """
    table of most relevant info extracted from metadata
    """
    
    first_column = ['Total number of projects with available metadata', 'Total number of projects with available data', 'Total number of samples', 'Total number of scientific names', 
        'Total number of library source','Total number of library strategies','Total number of instrument platforms',
        'Total number of library layouts', 'Year of the oldest project', 'Year of the most recent project', 'Total number of countries', 'Max total size']
    second_column = []
    
    
    for column in ['study_accession', 'fastq_bytes', 'run_accession','scientific_name', 'library_source','library_strategy','instrument_platform', 'library_layout', 'first_public', 'last_updated']:
        if pd.Series(column).isin(e_df.columns).all():
            if column == 'fastq_bytes':
                subset = e_df[['fastq_bytes','submitted_bytes','sra_bytes']]
                e_df['bytes_availability'] = subset.isna().all(axis=1) #check if the cells of all the columns are empty
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

            replacers = {'USA':'United States', 'United States America':'United States', 'American United States':'United States'}
            p_df['affiliation'] = p_df['affiliation'].replace(replacers) #problema con korea... bisogna capire se del nord o del sud, quindi tramite città?
            affiliation_list = p_df['affiliation'].tolist()
            country_list = []
            for affiliation in affiliation_list:
                for country in pycountry.countries: #extract the name of the country from a string, in this case the affiliation
                    if country.name in affiliation:
                        country_list.append(country.name)
            
            unique_country_list = list(set(country_list)) #remove duplicates
            country_number = len(unique_country_list)
            second_column.append(country_number)


    for column in ['sra_bytes']:
        if pd.Series(column).isin(e_df.columns).all():
            IDs =  e_df['study_accession'].unique().tolist()
            fastq_bytes_list = []
            submitted_bytes_list = []
            sra_bytes_list = []

            for id in IDs:
                fastq_bytes = Project.getProjectBytes(id, e_df, file_type = 'fastq')
                fastq_bytes_list.append(fastq_bytes)
                submitted_bytes = Project.getProjectBytes(id, e_df, file_type = 'submitted')
                submitted_bytes_list.append(submitted_bytes)
                sra_bytes = Project.getProjectBytes(id, e_df, file_type = 'sra')
                sra_bytes_list.append(sra_bytes)

            for bytes_list in [fastq_bytes_list, submitted_bytes_list, sra_bytes_list]:
                for item in bytes_list:
                    float(item)
            
            fastq = sum(fastq_bytes_list)
            submitted = sum(submitted_bytes_list)
            sra = sum(sra_bytes_list)

            total_bytes = {'fastq_bytes': fastq, 'submitted_bytes': submitted, 'sra_bytes': sra}
            total_bytes = sorted(total_bytes.items(), key=lambda x:x[1])
            size = Utilities.bytes_converter(total_bytes[2][1])
            value = f'{size} ({total_bytes[2][0]})'

            second_column.append(value)

    values = [first_column, second_column]

    fig = go.Figure(data=[go.Table(
    columnorder = [1,2],
    columnwidth = [100,80],
    header = dict(
        values = ['', 'Values'],
        line_color='#FFFFFF',
        line_width = 0,
        fill_color=['#FFFFFF','#FFE657'],
        align='center',
        font=dict(color='black', family='Times New Roman', size=30),
        height=60
    ),
    cells=dict(
        values=values,
        line_color='lightgrey',
        line_width = 2,
        fill_color=['#FFE657', '#FFFFFF'],
        align=['left', 'center'],
        font=dict(color='black', family='Times New Roman', size=30),
        height=45
        ))
    ])

    fig.update_layout(title_text='Summary information<br><br><br><br><br><br><br><br>\n', title_x=0.5, title_font = dict(family='Times New Roman', size=40))
    fig.write_html(os.path.join(report_folder, "Sample number.html"))
    f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    


def sample_number(report_folder, e_df, color_palette, f):
    
    sample_number_series = e_df.groupby(['study_accession'])['run_accession'].count()
    sample_number_df = pd.DataFrame(sample_number_series).reset_index()
    sample_number_df.columns = ['Project', 'Number of samples']
    fig = px.bar(sample_number_df, x="Project", y="Number of samples", color="Number of samples", 
        color_continuous_scale = color_palette, log_y=True)
    fig.update_layout(title_text='Number of samples', title_x=0.5, title_font = dict(family='Times New Roman', size=40),
                barmode='stack', legend_title_text="Number of samples<br>", legend=dict(title_font_family="Times New Roman", #font=dict(size= 20),
                bordercolor="lavenderblush", borderwidth=3))
    fig.update_xaxes(title_text= "project", title_font=dict(family='Times New Roman', size=25))
    fig.update_yaxes(title_text= "number of samples",title_font=dict(family='Times New Roman', size=25))
    fig.write_image(os.path.join(report_folder, "Sample number.png"), width=1920, height=1080)
    fig.write_html(os.path.join(report_folder, "Sample number.html"))
    f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
        

def pie_and_bar_charts(report_folder, e_df, color_palette_hex, f):
    
    for column in ['scientific_name', 'library_source','library_strategy','instrument_platform', 'library_layout']: ########BACKUP
        if pd.Series(column).isin(e_df.columns).all():
            library_layout_df = e_df[column].value_counts() #df for pie
            print(library_layout_df)
            df_pie = pd.DataFrame(library_layout_df).reset_index()
            column_name = column.capitalize().replace('_', ' ')
            df_pie.columns = [column_name, 'Counts']
            
            library_layout_IDs_df = e_df.groupby(['study_accession'])[column].value_counts() #df for bar
            df_bar = library_layout_IDs_df.rename('count').reset_index()
            column_name = column.capitalize().replace('_', ' ')
            df_bar.columns = ['Project', column_name, 'Counts']


# def pie_and_bar_charts(report_folder, e_df, color_palette_hex, f):
    
#     for column in ['scientific_name', 'library_source','library_strategy','instrument_platform', 'library_layout']: ########BACKUP
#         if pd.Series(column).isin(e_df.columns).all():
#             library_layout_df = e_df[column].value_counts() #df for pie
#             df_pie = pd.DataFrame(library_layout_df).reset_index()
#             column_name = column.capitalize().replace('_', ' ')
#             df_pie.columns = [column_name, 'Counts']
            
#             library_layout_IDs_df = e_df.groupby(['study_accession'])[column].value_counts() #df for bar
#             df_bar = library_layout_IDs_df.rename('count').reset_index()
#             column_name = column.capitalize().replace('_', ' ')
#             df_bar.columns = ['Project', column_name, 'Counts']

#             color_dictionary = dict(zip(df_bar[column_name].unique(), color_palette_hex)) #associate column values to color
#             df_bar['Color'] = df_bar[column_name].map(color_dictionary) #create a new column based on dictionary mapping another column
            
#             fig = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "bar"}]])
            
#             fig.add_trace(go.Pie(labels=df_pie[column_name], values=df_pie['Counts'], hole=0.6, 
#                 marker_colors= df_pie[column_name].map(color_dictionary), showlegend=False, 
#                 hovertemplate = "Layout: %{label} <br>Percentage of samples: %{percent}<extra></extra>"),#, textfont_size=20),
#                 row=1, col=1)

#             for c in df_bar[column_name].unique(): #to create the legend use loop for
#                 df_color= df_bar[df_bar[column_name] == c]
#                 fig.add_trace(go.Bar(x=df_color["Project"], y = df_color["Counts"], marker_color = df_color['Color'],
#                     text = df_color[column_name], textposition = "none", name = c, 
#                     showlegend = True, hovertemplate = "Layout: %{text} <br>Number of samples: %{y}<extra></extra>"),
#                     row=1, col=2)
                
#             fig.update_layout(title_text=f'{column_name}', title_x=0.5, title_font = dict(family='Times New Roman', size=40),
#                 barmode='stack', legend_title_text=f"{column_name}<br>", legend=dict(#title_font_family="Times New Roman",# font=dict(size= 20),
#                 bordercolor="lavenderblush", borderwidth=3))
#             fig.update_xaxes(title_text= "project", title_font=dict(family='Times New Roman', size=25))
#             fig.update_yaxes(title_text= "number of samples",title_font=dict(family='Times New Roman', size=25), type="log")
#             fig.write_image(os.path.join(report_folder, f"{column_name}.png"), width=1920, height=1080)
#             fig.write_html(os.path.join(report_folder, f"{column_name}.html"))
#             f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
#         else:
#             print(f'{column_name} column missing')
#######
    # for column in ['scientific_name', 'library_source','library_strategy','instrument_platform', 'library_layout']: ########BACKUP
    #     if pd.Series(column).isin(e_df.columns).all():
    #         library_layout_df = e_df[column].value_counts() #df for pie
    #         df_pie = pd.DataFrame(library_layout_df).reset_index()
    #         column_name = column.capitalize().replace('_', ' ')
    #         df_pie.columns = [column_name, 'Counts']

    #         fig_pie = px.pie(df_pie, values=df_pie['Counts'], names=df_pie[column_name], hole=0.6, color_discrete_sequence=px.colors.sequential.RdBu)
    #         fig_pie.write_image(os.path.join(report_folder, f"{column_name}.png"), width=1920, height=1080)
    #         fig_pie.write_html(os.path.join(report_folder, f"{column_name}.html"))
    #         f.write(fig_pie.to_html(full_html=False, include_plotlyjs='cdn'))

    #         library_layout_IDs_df = e_df.groupby(['study_accession'])[column].value_counts() #df for bar
    #         df_bar = library_layout_IDs_df.rename('count').reset_index()
    #         column_name = column.capitalize().replace('_', ' ')
    #         df_bar.columns = ['Project', column_name, 'Counts']

            
        
        
        # else:
        #     print(f'{column_name} column missing')


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
    fig.update_yaxes(title_text= "megabytes",title_font=dict(family='Times New Roman', size=25), type="log")
    fig.update_traces(hovertemplate = "Project: %{x} <br>Megabytes: %{y:,.3f}<br><extra></extra>")

    fig.write_image(os.path.join(report_folder, "Projects size.png"), width=1920, height=1080)
    fig.write_html(os.path.join(report_folder, "Projects size.html"))
    f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))


def IDs_dates(report_folder, e_df, f): #####################################C'è UN PROBLEMA CON L'ASSE Y
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
    
    try:
        p_df['affiliation'] = p_df['affiliation'].str.replace('USA','United States') #problema con korea... bisogna capire se del nord o del sud, quindi tramite città?
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




# #WORLD MAP #######DA MODIFICARE, SILENZIATO PERCHé NON FUNZIONAVA

# def alpha3code(column): #create a list of ISO3 starting from the column of interest
#         CODE=[]
#         for country in column:
#             try:
#                 code=pycountry.countries.get(name=country).alpha_3
#                 CODE.append(code)
#             except:
#                 CODE.append('None')
#         return CODE

# def geography(report_folder, p_df, f): 
    
#     # for column in ['affiliation']:
#     #     if pd.Series(column).isin(p_df.columns).all():
#     #         p_df['affiliation'] = p_df['affiliation'].str.replace('USA','United States') # pycountry non riconosce US o USA e quindi non lo include
            
#             #collapsed_p_df = p_df.groupby(['project_id', 'affiliation']).count()
#     try:
#         p_df['affiliation'] = p_df['affiliation'].str.replace('USA','United States') #attenzione: sostituire tutti quelli che immaginiamo possano essere scritti in un  modo che pycountry non voglia
#         # qui link: https://github.com/flyingcircusio/pycountry/blob/main/src/pycountry/databases/iso3166-1.json
#         # https://stackoverflow.com/questions/15377832/pycountries-convert-country-names-possibly-incomplete-to-countrycodes
#         country_list = []
#         affiliation_list = p_df['affiliation'].tolist()
#         for affiliation in affiliation_list:
#             print(affiliation)
#             for country in pycountry.countries: #extract the name of the country from a string, in this case the affiliation
#                 if country.name in affiliation:
#                     country_list.append(country.name) #punto debole: se non estrae paese da tutte le righe allora lunghezza di lista < della colonna
#                     print(pycountry.countries)
#                     print(country)
#                     print(country.name)

#         # dicts = {}
#         # keys = range(len(p_df.index))
#         # values = p_df['affiliation'].tolist()
#         # for i in keys:
#         #     for x in values:
#         #         for country in pycountry.countries: #extract the name of the country from a string, in this case the affiliation
#         #             if country.name in x:
#         #                 #country_list.append(country.name)
#         #                 dicts[i] = x

#         # print(dicts)    

#         # temp_df  = pd.DataFrame(country_list, columns =['affiliation'])
#         # print([i.name for i in list(pycountry.countries)])
#         # print(p_df.affiliation[~temp_df.affiliation.isin([i.name for i in list(pycountry.countries)])])
                

#         # print(country_list)
#         # print(p_df['project_id'])
#         p_df['country'] = country_list
#         pd.set_option('display.max_columns', None)
#         pd.set_option('display.max_rows', None)
#         # print(p_df)

#         collapsed_p_df = p_df.groupby(['project_id', 'country']).count() #CONTINUARE DA QUI: USARE COLLAPSED PER FARE GRAFICO
#         print(collapsed_p_df)

        
#         input =  country_list
#         c = Counter(input) #counter of countries
#         country_df = pd.DataFrame(c.items(), columns = ['country', 'count'])
#         country_number = country_df['country'].nunique()
#         country_df['CODE']=alpha3code(country_df.country) #call alpha3code to create ISO3 column
#         country_df.columns = ['Country', 'Count', 'CODE']

#         fig = px.scatter_geo(country_df, locations="CODE", color = 'Count', size="Count", 
#             color_continuous_scale=['rgb(41, 24, 107)', 'rgb(42, 30, 138)', 'rgb(38, 41, 159)', 'rgb(22, 62, 155)', 
#             'rgb(16, 79, 150)', 'rgb(18, 92, 143)', 'rgb(27, 105, 140)', 'rgb(39, 117, 137)', 'rgb(47, 129, 136)', 
#             'rgb(56, 140, 135)', 'rgb(62, 153, 134)', 'rgb(71, 165, 130)', 'rgb(80, 177, 124)', 'rgb(97, 189, 115)', 
#             'rgb(116, 200, 105)', 'rgb(145, 209, 96)', 'rgb(174, 217, 97)', 'rgb(255, 230, 87)'], opacity = 0.95, size_max=30,
#             hover_data = {'CODE':False,'Country':True,'Count': True})
            
#         fig.update_layout(
#             title = 'Map of publications', title_x=0.5,
#             title_font = dict(family='Times New Roman', size=40),
#             showlegend = True, coloraxis_colorbar=dict(title="Number of <br>publications", 
#             thicknessmode="pixels", thickness=20,
#             lenmode="pixels", len=500))
        
#         fig.update_coloraxes(colorbar_title_text="Number of <br>publications<br>", #colorbar_title_font_family='Times New Roman', colorbar_title_font_size=20, 
#             colorbar_dtick=1) #only integers number separated by 1

#         fig.update_geos(scope='world',
#             visible=False,
#             showcoastlines=True, coastlinecolor="#F6F6F4",
#             showocean=True, oceancolor='#98BAD8',
#             showland=True, landcolor="#F6F6F4", 
#             projection_type = 'natural earth')

#         fig.update_traces(marker=dict(line=dict(width=0)))

#         fig.write_image(os.path.join(report_folder, "Map of publications.png"), width=1920, height=1080)
#         fig.write_html(os.path.join(report_folder, "Map of publications.html"))
#         f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))

#     except TypeError:
#         print('"_merged_publications-metadata.tsv" file missing')
    


    
def final_screen(user_session):
    print(Color.BOLD + Color.GREEN + '\nReport successfully created.' + Color.END,'You can find the', Color.UNDERLINE + 'Report in HTML format' + Color.END, 
    'and the', Color.UNDERLINE + 'Report folder' + Color.END,'here:', Color.BOLD + Color.YELLOW + f'{os.path.basename(user_session)}' + Color.END)
    input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")