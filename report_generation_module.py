from Utilities import Color, Utilities, LoggerManager
from Project import Project
import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import pycountry
from collections import Counter
from rich import print as rich_print
from rich.panel import Panel
from rich.text import Text
from rich.progress import track
from rich.progress import Progress, BarColumn
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import squarify 
import plotly.io as pio
import random

def report_generation(user_session):
    """
    main function
    """
    while True:
        Utilities.clear() 

        box = Panel(Text.assemble("Generate a report file about the information present in the downloaded metadata & publications files.\n\nChoose one of the following options:\n1 - Use '*_merged_experiments-metadata.tsv' & '*_merged_publications-metadata.tsv' files present the current session\n2 - Use '*_merged_experiments-metadata.tsv' & '*_merged_publications-metadata.tsv' files present in any other location of your computer\n\n>>> Your current session is ", (f"{user_session}", "rgb(255,255,0)"), " <<<\n\n--- If you want to return to the main menu digit: ", ("back", "rgb(255,0,255)")," ---", style = None, justify="left"), title=Text.assemble((" ◊", "rgb(0,255,0)"), " REPORT GENERATION MODULE ", ("◊ ", "rgb(0,255,0)")), border_style= "rgb(255,0,255)", padding= (0,1))
        rich_print(box)

        user_report_input = input("\n  >> Enter your choice: ").strip().lower()
        
        if user_report_input in ("back"):
            return
        
        elif user_report_input.isnumeric() == False:
            print(Color.BOLD + Color.RED + "Wrong input" + Color.END, "expected a numeric input or <back> (without <>)\n")
            input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")

        elif user_report_input.isnumeric() == True:
            user_report_input = int(user_report_input)
            if user_report_input not in (1,2):
                print(Color.BOLD + Color.RED +"Error" + Color.END,"enter a valid choice!")
                input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")
            
            else:
                if user_report_input == 1:
                    user_session = os.path.join(user_session)
                    available_metadata_files(user_session)
                    for file in os.listdir(os.path.join('Downloads', user_session)):
                        if file in f'Report_{user_session}.html':
                            return
                        else:
                            continue

                if user_report_input == 2:
                    user_report_local(user_session)
                    for file in os.listdir(os.path.join('Downloads', user_session)):
                        if file in f'Report_{user_session}.html':
                            return
                        else:
                            continue


def user_report_local(user_session):
    """
    user digit path to '*_merged_experiments-metadata.tsv' & '*_merged_publications-metadata.tsv' files. check if path exists, if it is so recall 'available_metadata_files' function
    """
    while True:
        Utilities.clear()

        box = Panel(Text.assemble("Digit the path to the folder containing '*_merged_experiments-metadata.tsv' & '*_merged_publications-metadata.tsv' files.\n\nThe report will be downloaded in the folder indicated.\n\n>>> Your current session is ", (f"{user_session}", "rgb(255,255,0)"), " <<<\n\n--- If you want to return to the REPORT GENERATION menu digit: ", ("back", "rgb(255,0,255)")," ---", style = None, justify="left"), title=Text.assemble((" ◊", "rgb(0,255,0)"), " REPORT GENERATION MODULE ", ("◊ ", "rgb(0,255,0)")), border_style= "rgb(255,0,255)", padding= (0,1))
        rich_print(box)

        user_path = input("\n  >> Digit the path: ").strip()

        if user_path.lower() in ("back"):
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
    possible_metadata_files = [file for file in os.listdir(os.path.join('Downloads', user_session)) if file.endswith("-metadata.tsv")]
    list_metadata_files = [file for file in possible_metadata_files if file.endswith(tuple(metadata_files))]
    list_metadata_files = sorted(list_metadata_files)
     
    available_metadata_files = len(list_metadata_files)

    if available_metadata_files == 0:
        print(Color.BOLD + Color.RED + "\nError found 0 file" + Color.END, "Is it the correct folder? Note that the files names must end with '_merged_experiments-metadata.tsv' and '_merged_publications-metadata.tsv'\n")
        input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")
    
    elif available_metadata_files == 1:
        print(Color.BOLD + Color.GREEN + "\nFound" + Color.END, f"{list_metadata_files[0]}")
        f1_path = os.path.join('Downloads', user_session, list_metadata_files[0])
        f1_df = pd.read_csv (f1_path, delimiter='\t', infer_datetime_format=True, dtype=str)#
        if 'study_accession' in f1_df:
            e_df = f1_df
            logger = LoggerManager.log(user_session)
            logger.debug(f"Found {list_metadata_files[0]}")
            report(user_session, e_df, p_df=None)
            final_screen(user_session)
        else:
            print(Color.BOLD + Color.RED + "\nError the found file seems to lack some of the expected information" + Color.END, f" Is it the correct file? Try again")
            input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")

    elif available_metadata_files == 2:
        print(Color.BOLD + Color.GREEN + "\nFound" + Color.END, f"{list_metadata_files[0]}")
        print(Color.BOLD + Color.GREEN + "Found" + Color.END, f"{list_metadata_files[1]}")
        f1_path = os.path.join('Downloads', user_session, list_metadata_files[0])
        f1_df = pd.read_csv(f1_path, delimiter='\t', infer_datetime_format=True, dtype=str)#
        f2_path = os.path.join('Downloads', user_session, list_metadata_files[1])
        f2_df = pd.read_csv(f2_path, delimiter='\t', infer_datetime_format=True, dtype=str)#
        if 'study_accession' in f1_df:
            e_df = f1_df
            p_df = f2_df
        else:
            p_df = f1_df
            e_df = f2_df
        logger = LoggerManager.log(user_session)
        logger.debug(f"Found {list_metadata_files[0]} and {list_metadata_files[1]}")
        report(user_session, e_df, p_df)
        final_screen(user_session)

#reports
def report(user_session, e_df, p_df): 
    """
    report generation based on how many '*_merged_<experiment or publication>-metadata.tsv' files are present in the folder.
    create a report folder that will contain all plots in png format, create a single html that will contain all plots 
    """
    
    #set e_df by creating the column to refer in plots generating. If PRJ is missing, consider [D,E,S]RP
    e_df['grouping_col'] = e_df['study_accession']
    e_df.loc[e_df['grouping_col'].isna(), 'grouping_col'] = e_df['secondary_study_accession']

    
    color_palette_rgb = ['rgb(41, 24, 107)', 'rgb(42, 30, 138)', 'rgb(38, 41, 159)', 'rgb(22, 62, 155)', 
        'rgb(16, 79, 150)', 'rgb(18, 92, 143)', 'rgb(27, 105, 140)', 'rgb(39, 117, 137)', 'rgb(47, 129, 136)', 
        'rgb(56, 140, 135)', 'rgb(62, 153, 134)', 'rgb(71, 165, 130)', 'rgb(80, 177, 124)', 'rgb(97, 189, 115)', 
        'rgb(116, 200, 105)', 'rgb(145, 209, 96)', 'rgb(174, 217, 97)', 'rgb(255, 210, 11)']
    color_palette_hex = ['#29186b', '#2a1e8a', '#26299f', '#163e9b', '#104f96', '#125c8f', '#1b698c', '#277589', '#2f8188', '#388c87', '#3e9986', '#47a582',
                         '#50b17c', '#61bd73', '#74c869', '#91d160', '#aed961', '#ffd20b']
    
    color_palette_scale = px.colors.make_colorscale(color_palette_rgb)
    color_palette_rgb_r = list(reversed(color_palette_rgb))
    color_palette_hex_r =list(reversed(color_palette_hex))
    color_palette_scale_rgb_r = px.colors.make_colorscale(color_palette_rgb_r)

    report_folder = (os.path.join('Downloads', user_session, 'Report_images'))
    if not os.path.exists(report_folder):
        os.makedirs(report_folder)
    
    report_html = os.path.join('Downloads', user_session,f'Report_{user_session}.html')
    plot_functions = [initial_table, sample_number, pie_and_bar_charts, treemap, projects_size, IDs_dates, geography, wordcloud]
    with open(report_html, 'w+') as f:
        for plot in track(plot_functions, description="Generating plots..."):
            plot(report_folder, e_df, p_df, color_palette_rgb, f)     


#report functions
#INITIAL TABLE
def initial_table(report_folder, e_df, p_df, color_palette_rgb, f):
    """
    table of most relevant info extracted from metadata
    """

    first_column = ['Total number of projects with available metadata', 'Total number of projects with available data', 'Total number of samples', 'Total number of scientific names', 
        'Total number of library source','Total number of library strategies','Total number of instrument platforms',
        'Total number of library layouts', 'Year of the oldest project', 'Year of the most recent project', 'Max total size', 'Total number of countries']
    second_column = []
    
    
    for column in ['grouping_col', 'fastq_bytes', 'run_accession','scientific_name', 'library_source','library_strategy','instrument_platform', 'library_layout', 'first_public', 'last_updated']:#
        if pd.Series(column).isin(e_df.columns).all():
            if column == 'fastq_bytes':
                subset = e_df[['fastq_bytes','submitted_bytes','sra_bytes']]
                e_df['bytes_availability'] = subset.isna().all(axis=1) #check if the cells of all the columns are empty
                non_available_data_projs = e_df.query("bytes_availability==True")["study_accession"].tolist() #get project corresponding to empty cells
                non_available_data_projs_norep = [*set(non_available_data_projs)] #remove replicates
                all_data_projs = e_df['grouping_col'].nunique()#
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


    for column in ['sra_bytes']:
        if pd.Series(column).isin(e_df.columns).all():
            IDs =  e_df['grouping_col'].unique().tolist()#
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

            total_bytes = {'fastq': fastq, 'submitted': submitted, 'sra': sra}
            total_bytes = sorted(total_bytes.items(), key=lambda x:x[1])
            size = Utilities.bytes_converter(total_bytes[2][1])
            value = f'{size} ({total_bytes[2][0]})'

            second_column.append(value)


    if p_df is not None:
        for column in ['affiliation']:
            if pd.Series(column).isin(p_df.columns).all():
                replace_countries = {'USA': 'United States', 'South Korea': 'Korea, Republic of', 'South Corea': 'Korea, Republic of', 'South korea': 'Korea, Republic of', 'Korea':'Korea, Republic of' }
                p_df['affiliation'] = p_df['affiliation'].replace(replace_countries, regex=True)
                country_list = []
                affiliation_list = p_df['affiliation'].tolist()
                for affiliation in affiliation_list:
                    try:
                        for country in pycountry.countries:
                            if country.name in affiliation:
                                country_list.append(country.name)
                    except TypeError:
                        pass
                unique_country_list = list(set(country_list))
                country_number = len(unique_country_list)
                second_column.append(country_number)
    else:
        second_column.append(' ')


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

    df_dict = {'index': first_column, 'values': second_column}
    df = pd.DataFrame(df_dict)
    file_name = os.path.join(report_folder,'summary_table.xlsx')
    df.to_excel(file_name, index=False)


def sample_number(report_folder, e_df, p_df, color_palette_rgb, f):
    """
    generate bar chart
    """
    color_palette_scale = px.colors.make_colorscale(color_palette_rgb)
    color_palette_rgb_r = list(reversed(color_palette_rgb))
    color_palette_scale_rgb_r = px.colors.make_colorscale(color_palette_rgb_r)

    sample_number_series = e_df.groupby(['grouping_col'])['run_accession'].count()#
    sample_number_df = pd.DataFrame(sample_number_series).reset_index()
    sample_number_df.columns = ['Project', 'Number of samples']
    sample_number_df = sample_number_df.sort_values("Number of samples", ascending=False)
    fig = px.bar(sample_number_df, x="Project", y="Number of samples", log_y=True,
                 color="Number of samples", color_continuous_scale = color_palette_scale_rgb_r)
    fig.update_layout(title_text='Number of samples', title_x=0.5, title_font = dict(family='Times New Roman', size=40),
                barmode='stack', legend_title_text="Number of samples<br>", legend=dict(title_font_family="Times New Roman", #font=dict(size= 20),
                bordercolor="lavenderblush", borderwidth=3))
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)'})
    fig.update_xaxes(title_text= "project", title_font=dict(family='Times New Roman', size=25))
    fig.update_yaxes(title_text= "number of samples",title_font=dict(family='Times New Roman', size=25))
    fig.write_image(os.path.join(report_folder, "Sample number.png"), width=1920, height=1080)
    fig.write_html(os.path.join(report_folder, "Sample number.html"))
    f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))


def pie_and_bar_charts(report_folder, e_df, p_df, color_palette_rgb, f):
    """
    generate pie chart and bar chart
    """
    color_palette_scale = px.colors.make_colorscale(color_palette_rgb)

    for column in ['scientific_name', 'library_source','library_strategy','instrument_platform', 'library_layout']:
        if pd.Series(column).isin(e_df.columns).all():
            column_count_df = e_df[column].value_counts() #df for pie
            df_pie = pd.DataFrame(column_count_df).reset_index()
            column_name = column.capitalize().replace('_', ' ')
            df_pie.columns = [column_name, 'Count']

            column_count_IDs_df = e_df.groupby(['grouping_col'])[column].value_counts() #df for bar            #
            df_bar = column_count_IDs_df.rename('count').reset_index()
            column_name = column.capitalize().replace('_', ' ')
            df_bar.columns = ['Project', column_name, 'Count']

            n_colors = len(df_pie)
            if  n_colors == 1:
                colors = px.colors.sample_colorscale(color_palette_scale, [n for n in range(n_colors)]) 
            if n_colors > 1 and n_colors < 15:
                colors = px.colors.sample_colorscale(color_palette_scale, [n/(n_colors -1) for n in range(n_colors)])
            if n_colors >= 15:
                colors = [random.choice(color_palette_scale) for n in range(n_colors)]
                colors = [n[1] for n in colors]
            

            df_pie = df_pie.sort_values("Count", ascending=False)
            df_pie["Percentage"] = (df_pie["Count"]/df_pie["Count"].sum())*100
            df_pie["Percentage"] = df_pie["Percentage"].apply(lambda x: '{:.1f}%'.format(x))
            file_name = os.path.join(report_folder,f'{column_name} table.xlsx')
            df_pie.to_excel(file_name, index=False)

            if len(df_pie.index) > 10: #prevent complex pie chart
                df_pie_copy = df_pie
                df_pie_rare = df_pie.iloc[10:,]
                df_pie_copy.drop(df_pie.iloc[10:,].index, inplace = True)

                df_pie_rare = df_pie_rare.sum().to_frame().T #sum alla rows into one, make it in dataframe, and traspose rows into columns
                df_pie_rare.at[0, f'{column_name}'] = 'Other'

                df_pie = pd.concat([df_pie, df_pie_rare])

            fig = px.pie(df_pie, values=df_pie['Count'], names=df_pie[column_name], hole=0.6, 
                    color_discrete_sequence = colors) 
            
            names = [item[:25] for item in df_pie[column_name]]
            # for i, elem in enumerate(fig.data[0].labels): #to prevent long labels #pie
            #     fig.data[0].labels[i] = fig.data[0].labels[i][:25]
            
            fig.update_layout(title_text=f'{column_name}', title_x=0.5, title_font = dict(family='Times New Roman', size=40))
            fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)'})
            fig.write_image(os.path.join(report_folder, f"{column_name}_pie.png"), width=1920, height=1080)
            fig.write_html(os.path.join(report_folder, f"{column_name}_pie.html"))
            f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))

            df_bar = df_bar.sort_values("Count", ascending=False)
            names = [item[:25] for item in df_bar[column_name]] #to prevent long labels #bar
            fig = fig = px.bar(df_bar, x="Project", y="Count", color=names,
                    color_discrete_sequence = colors, log_y=True)
            fig.update_layout(title_text=f'{column_name}', title_x=0.5, title_font = dict(family='Times New Roman', size=40),
                    legend=dict(groupclick='toggleitem'))

            fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)'}) #plot with transparent background
            fig.write_image(os.path.join(report_folder, f"{column_name}_bar.png"), width=1920, height=1080)
            fig.write_html(os.path.join(report_folder, f"{column_name}_bar.html"))
            f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))

def treemap(report_folder, e_df, p_df, color_palette_rgb, f):

    color_palette_hex = ['#29186b', '#2a1e8a', '#26299f', '#163e9b', '#104f96', '#125c8f', '#1b698c', '#277589', '#2f8188', '#388c87', '#3e9986', '#47a582',
                         '#50b17c', '#61bd73', '#74c869', '#91d160', '#aed961', '#ffd20b']
    color_palette_hex_r =list(reversed(color_palette_hex))

    df_bar = e_df[['scientific_name']]
    df_bar = df_bar.groupby(['scientific_name']).value_counts().rename('count').reset_index()
    total_scientific_name = df_bar['count'].sum()
    df_bar['percentage'] = round((df_bar['count']/total_scientific_name)*100, 2).astype(str) + '%'
    df_bar.to_excel(os.path.join(report_folder, "df_bar.xlsx"))
    average = df_bar['count'].mean()

    fig = px.treemap(df_bar, path=[px.Constant("Scientific names"), df_bar['scientific_name']], values= df_bar['count'], color = df_bar['count'],
            color_continuous_scale=color_palette_hex_r)

    percents = df_bar.percentage.tolist()
    fig.data[0].customdata = np.column_stack([percents])
    fig.update_traces(hovertemplate='Scientific name=%{label}<br>Count=%{value}<br>Percentage=%{customdata[0]}<extra></extra>')
    fig.update_traces(marker=dict(colorscale=color_palette_hex_r, cornerradius=5))
    fig.update_layout(margin = dict(t=60, l=25, r=25, b=25))
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)'})

    fig.update_layout(
            title = 'Treemap of scientific names', title_x=0.5,
            title_font = dict(family='Times New Roman', size=40))

    df_bar.to_excel(os.path.join(report_folder, "Treemap.xlsx"))
    fig.write_image(os.path.join(report_folder, "Treemap.png"), width=1920, height=1080)
    fig.write_html(os.path.join(report_folder, "Treemap.html"))
    f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))

#PROJECT SIZE & BYTES
def projects_size(report_folder, e_df, p_df, color_palette_rgb, f):
    """
    generate bubble plot based on fastq bytes for each project
    """
    color_palette_rgb_r = list(reversed(color_palette_rgb))
    color_palette_scale_rgb_r = px.colors.make_colorscale(color_palette_rgb_r)

    IDs =  e_df['grouping_col'].unique().tolist()#
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
    

    user_Megabytes = []
    for byte in bytes_list:
        user_bytes = byte/1024/1024
        user_Megabytes.append(user_bytes)

    df['User_Megabytes']=user_Megabytes
    df.to_excel(file_name)
   
    #BUBBLE PLOT
    fig = px.scatter(df, x='Project', y='User_Megabytes', size='User_Megabytes',
                 color='User_Megabytes', size_max=150, color_continuous_scale = color_palette_scale_rgb_r, 
                 opacity = 0.8)

    fig.update_layout(title = 'Project size', title_x=0.5, title_font = dict(family='Times New Roman', size=40),
        showlegend = True, coloraxis_colorbar=dict(title="Megabyte", 
        thicknessmode="pixels", thickness=20,
        lenmode="pixels", len=500))
    
    fig.update_coloraxes(colorbar_title_text="Megabyte")#, colorbar_title_font_family='Times New Roman', colorbar_title_font_size=20)
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)'})
    fig.update_xaxes(title_text= "project", title_font=dict(family='Times New Roman', size=25))
    fig.update_yaxes(title_text= "megabytes",title_font=dict(family='Times New Roman', size=25), type="log")
    fig.update_traces(hovertemplate = "Project: %{x} <br>Megabytes: %{y:,.1f}<br><extra></extra>", marker_sizemin=10)
    fig.write_image(os.path.join(report_folder, "Projects size.png"), width=1920, height=1080)
    fig.write_html(os.path.join(report_folder, "Projects size.html"))
    f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))



def IDs_dates(report_folder, e_df, p_df, color_palette_rgb, f):
    """
    generate bubble plot based on first and last update year for each project
    """
    if pd.Series(['first_public', 'last_updated']).isin(e_df.columns).all():
        collapsed_e_df = e_df.groupby('grouping_col').first().reset_index() #
        collapsed_e_df = collapsed_e_df.sort_values(by=['first_public'], ascending=True)
        collapsed_e_df_f = collapsed_e_df[['grouping_col', 'first_public_year']] #
        collapsed_e_df_l = collapsed_e_df[['grouping_col', 'last_updated_year']] #
        collapsed_e_list_f_x = collapsed_e_df_f.grouping_col.values.tolist() #
        collapsed_e_list_f_y = collapsed_e_df_f.first_public_year.values.tolist()
        collapsed_e_list_l_x = collapsed_e_df_l.grouping_col.values.tolist() #
        collapsed_e_list_l_y = collapsed_e_df_l.last_updated_year.values.tolist()
        
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
                    legend_title_text="Updates<br>", #legend=dict(#title_font_family="Times New Roman", #font=dict(size= 20),
                    #bordercolor="lavenderblush", borderwidth=3),
                    hovermode='x') #to see both hover labels
        fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)'})
        fig.update_xaxes(title_text= "project", title_font=dict(family='Times New Roman', size=25))
        fig.update_yaxes(title_text= "year",title_font=dict(family='Times New Roman', size=25),
            type="category", categoryorder='category ascending') #make years as categorical and sort them
        fig.write_image(os.path.join(report_folder, "Years update.png"), width=1920, height=1080)
        fig.write_html(os.path.join(report_folder, "Years update.html"))
        f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))

    else:
        print('first_public and last_updated columns missing')



#WORLD MAP
def alpha3code(column):
    """
    create a list of ISO3 starting from the column of interest
    """
    CODE=[]
    for country in column:
        try:
            code=pycountry.countries.get(name=country).alpha_3
            CODE.append(code)
        except:
            CODE.append('None')
    return CODE

def geography(report_folder, e_df, p_df, color_palette_rgb, f):
    """
    generate a bubble world map indicating each project's country
    https://github.com/flyingcircusio/pycountry/blob/main/src/pycountry/databases/iso3166-1.json
    https://stackoverflow.com/questions/15377832/pycountries-convert-country-names-possibly-incomplete-to-countrycodes
    """

    color_palette_rgb_r = list(reversed(color_palette_rgb))
    color_palette_scale_rgb_r = px.colors.make_colorscale(color_palette_rgb_r)

    try:
        replace_countries = {'USA': 'United States', 'South Korea': 'Korea, Republic of', 'South Corea': 'Korea, Republic of', 
                             'South korea': 'Korea, Republic of', 'Korea':'Korea, Republic of', 'Brasil': 'Brazil', 'Perugia': 'Italy',
                             'Indiana': '', 'New Jersey':'United States', 'Georgia.':'Georgia', 'Georgia':'GA'}
        p_df['affiliation'] = p_df['affiliation'].replace(replace_countries, regex=True)
        country_list = []
        affiliation_list = p_df['affiliation'].tolist()
        for affiliation in affiliation_list:
            try:
                for country in pycountry.countries: #extract the name of the country from a string, in this case the affiliation
                    if country.name in affiliation:
                        country_list.append(country.name)
            except TypeError:
                pass
        
        input =  country_list
        c = Counter(input) #counter of countries
        country_df = pd.DataFrame(c.items(), columns = ['country', 'count'])
        country_df['CODE']=alpha3code(country_df.country) #call alpha3code to create ISO3 column
        country_df.columns = ['Country', 'Count', 'CODE']

        fig = px.scatter_geo(country_df, locations="CODE", color = 'Count', size="Count", 
            color_continuous_scale=color_palette_scale_rgb_r , opacity = 0.95, size_max=30,
            hover_data = {'CODE':False,'Country':True,'Count': True})
            
        fig.update_layout({'geo': {'resolution': 50}},
            title = 'Map of publications', title_x=0.5,
            title_font = dict(family='Times New Roman', size=40),
            showlegend = True, coloraxis_colorbar=dict(title="Number of <br>publications", 
            thicknessmode="pixels", thickness=20,
            lenmode="pixels", len=500))
        
        min_val = country_df['Count'].min()
        max_val = country_df['Count'].max()
        tickvals = np.linspace(min_val, max_val, num=5, dtype=int)

        fig.update_coloraxes(colorbar_title_text="Number of <br>publications<br>", #colorbar_title_font_family='Times New Roman', colorbar_title_font_size=20, 
            colorbar_dtick=1, colorbar_tickvals=tickvals) #only integers number separated by 1

        fig.update_geos(scope='world',
            visible=False,
            showcoastlines=True, coastlinecolor="#F6F6F4",
            showocean=True, oceancolor='#98BAD8',
            showland=True, landcolor="#F6F6F4", 
            projection_type = 'natural earth')

        fig.update_traces(marker=dict(line=dict(width=0)), marker_sizemin=10)
        fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)'})

        fig.write_image(os.path.join(report_folder, "Map of publications.png"), width=1920, height=1080)
        fig.write_html(os.path.join(report_folder, "Map of publications.html"))
        f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))

    except TypeError:
        print('"merged_publications-metadata.tsv" file missing: NO world map generated')    


def wordcloud(report_folder, e_df, p_df, color_palette_rgb, f): 
    
    color_palette_hex = ['#29186b', '#2a1e8a', '#26299f', '#163e9b', '#104f96', '#125c8f', '#1b698c', '#277589', '#2f8188', '#388c87', '#3e9986', '#47a582',
                         '#50b17c', '#61bd73', '#74c869', '#91d160', '#aed961', '#ffd20b']
    color_palette_hex_r =list(reversed(color_palette_hex))
    try:
        titles = list(p_df['title'])
        text = ' '.join(titles)
        colormap = LinearSegmentedColormap.from_list("custom_colormap", color_palette_hex_r) #create customed colormap for worldcloud
        wordcloud = WordCloud(width=1920, height=1080, background_color="white", colormap = colormap).generate(text)
        fig = plt.figure(figsize=(16, 9))
        plt.axis("off")
        plt.tight_layout()
        plt.imshow(wordcloud, interpolation='bilinear')

        layout = go.Layout(
        title={'text': "Wordcloud of projects-associated publications titles", 'x':0.5},
        title_font=dict(family='Times New Roman', size=40),
        hovermode=False)

        fig = go.Figure(data=go.Image(z=wordcloud.to_array()), layout=layout)
        fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)'})
        fig.write_image(os.path.join(report_folder, "WordCloud.png"), width=1920, height=1080)
        fig.write_html(os.path.join(report_folder, "WordCloud.html"))
        f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    except TypeError:
        print('"merged_publications-metadata.tsv" file missing: NO wordcloud generated')   


def final_screen(user_session):
    logger = LoggerManager.log(user_session)
    logger.debug(f"[REPORT-GENERATION-COMPLETED]: You can find the Report file in HTML format and the Report folder here: Downloads/{user_session}")
    print(Color.BOLD + Color.GREEN + '\nReport successfully created.' + Color.END,'You can find the', Color.UNDERLINE + 'Report file in HTML format' + Color.END, 
    'and the', Color.UNDERLINE + 'Report folder' + Color.END,'here:', Color.BOLD + Color.YELLOW + f'Downloads/{user_session}' + Color.END)
    input("\nPress " + Color.BOLD + Color.PURPLE + f"ENTER" + Color.END + " to continue ")
    return