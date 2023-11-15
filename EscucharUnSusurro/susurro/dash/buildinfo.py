import os
from dotenv import load_dotenv
load_dotenv() 
Bearer = os.getenv('Bearer')
apiurl = os.getenv('apiurl')

import requests
from pprint import pprint
from datetime import datetime, timedelta
import sqlite3
num = ''
def getONU(num):
    url = f"{apiurl}/api/komp_assistant/onu/phone/{num}"

    payload = {}
    headers = {
    'Authorization': Bearer
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        data = response.json()
        #pprint(data)
        bcode_value = data.get("bcode")
        bname_value = data.get("bname")
        return bcode_value, bname_value
    else:
        bcode_value = None
        return None

def getPAP(num):
    url = f"{apiurl}/api/komp_assistant/phone/{num}"

    payload = {}
    headers = {
    'Authorization': Bearer
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        data = response.json()
        bcode_value = data.get("bcode")
        bname_value = data.get("bname")
        return bcode_value, bname_value
    else:
        bcode_value = None
        return None

def getbcode(num):
    try:
        bcode, bname = getPAP(num)
        if bcode == None:
            bcode, bname = getONU(num)
            if bcode == None:
                #print('Bcode not found for both PAP and ONU')
                return 'Not Found'
            else:
                #print('ONU', num, bcode)
                return 'ONU', num, bcode, bname
        else:
            #print('PAP', num, bcode)
            return 'PAP', num, bcode, bname
    except Exception as e:
        #print('Error: ',e)
        pass


def getresultsdict(time_period='all'):
    # Check the system date
    system_date = datetime.now().strftime('%Y-%m-%d')

    # Define the date condition based on the time period
    if time_period == 'today':
        date_condition = f"DATE(date) = '{system_date}'"
    elif time_period == 'last_week':
        last_week_start = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        date_condition = f"DATE(date) BETWEEN '{last_week_start}' AND '{system_date}'"
    else:  # Default to 'all'
        date_condition = "1=1"

    # Connect to the SQLite database
    conn = sqlite3.connect('../transcriptions.db')
    cursor = conn.cursor()

    # Initialize an empty dictionary to store results
    results_dict = {}

    # Retrieve unique contact numbers from the transcriptions table
    query = f"SELECT DISTINCT contact FROM transcriptions WHERE contact IS NOT NULL AND {date_condition};"
    cursor.execute(query)

    contacts = cursor.fetchall()
    #print(contacts)

    # Iterate over each contact number
    for contact in contacts:
        num = contact[0]

        # Use the getbcode function to get router, num, building code, and bname
        result = getbcode(num)

        if isinstance(result, tuple):
            router, num, buildingcode, bname = result
        else:
            buildingcode = router = bname = 'Not Exist'

        # Store the results in the dictionary
        results_dict[num] = {
            'router': router,
            'num': num,
            'buildingcode': buildingcode,
            'bname': bname
        }

    # Close the database connection
    conn.close()
    return results_dict


def getmymap():
    import folium
    import json
    import geopandas as gpd

    # Load GeoJSON data from the file
    with open('../geobank/network_plans.geojson', 'r') as f:
        geojson_data = json.load(f)

    # Create a Folium map centered at the average location of buildings
    # Load the GeoJSON file containing building data
    buildings_geojson = "../geobank/buildings.geojson"
    buildings_gdf = gpd.read_file(buildings_geojson)
    avg_latitude = buildings_gdf['geometry'].centroid.y.mean()
    avg_longitude = buildings_gdf['geometry'].centroid.x.mean()
    mymap = folium.Map(location=[avg_latitude, avg_longitude], zoom_start=14)


    # Add GeoJSON layer to the map with named polygons
    folium.GeoJson(
        geojson_data,
        name='geojson_layer',
        style_function=lambda feature: {
            'fillColor': 'transparent',
            'color': 'black',
            'weight': 2,
            'dashArray': '5, 5',
        },
        highlight_function=lambda x: {'weight': 3, 'color': 'blue'},
        tooltip=folium.GeoJsonTooltip(fields=['Name'], aliases=['Polygon Name'], labels=True, sticky=True),
    ).add_to(mymap)

    # # Load the GeoJSON file containing building data
    # buildings_geojson = "./geobank/buildings.geojson"
    # buildings_gdf = gpd.read_file(buildings_geojson)


    # Add small circle markers for each building
    for index, row in buildings_gdf.iterrows():
        name = row['name']
        lat, lon = row['geometry'].y, row['geometry'].x
        if name != "Untitled Path":
            folium.Circle(location=[lat, lon], radius=5, color='green', fill=True, fill_color='blue', popup=name).add_to(mymap)
    return mymap

def determineIconcolor(buildingcode):
    if 'KENKH' in buildingcode:
        iconcolor = 'blue'
    elif 'KENKS' in buildingcode:
        iconcolor = 'darkblue'
    elif 'KENKM' in buildingcode:
        iconcolor = 'purple'
    elif 'KEKRK' in buildingcode:
        iconcolor = 'cadetblue'
    elif 'KENKK' in buildingcode:
        iconcolor = 'gray'
    elif 'KENRG' in buildingcode:
        iconcolor = 'black'
    elif 'KENRZ' in buildingcode:
        iconcolor = 'beige'
    elif 'KEKRG' in buildingcode:
        iconcolor = 'lightblue'
    elif 'KENRK' in buildingcode:
        iconcolor = 'green'
    elif 'KENRL' in buildingcode:
        iconcolor = 'lightgray'
    elif 'KENRR' in buildingcode:
        iconcolor = 'darkblue'
    else:
        iconcolor = 'orange'
    return iconcolor   

def generate_plots():
    from dash import dcc, html
    import pandas as pd
    import plotly.express as px
    from wordcloud import WordCloud
    import base64
    from io import BytesIO
    from PIL import Image
    import numpy as np

    # Connect to the SQLite database
    conn = sqlite3.connect('/home/wambugumuchemi/projects/listen-write/EscucharUnSusurro/susurro/transcriptions.db')
    
    # Query for bar chart
    query = "SELECT DATE(date), issue_category, COUNT(*) AS count FROM transcriptions WHERE issue_category IS NOT NULL GROUP BY DATE(date), issue_category"
    df = pd.read_sql_query(query, conn)
    df_pivot = df.pivot(index='DATE(date)', columns='issue_category', values='count').fillna(0)
    
    # Query for pie chart
    cursor = conn.cursor()
    cursor.execute('SELECT issue_category FROM transcriptions')
    results = cursor.fetchall()
    category_counts = {}
    for result in results:
        category = result[0]
        category_counts[category] = category_counts.get(category, 0) + 1
    
    # Query for scatter plot
    query_scatter = "SELECT DATE(date), issue_category FROM transcriptions WHERE issue_category IS NOT NULL"
    df_scatter = pd.read_sql_query(query_scatter, conn)
    
    # Summary query for WordCloud
    wordcloud_query = "SELECT summary FROM transcriptions WHERE summary IS NOT NULL"
    summary_df = pd.read_sql_query(wordcloud_query, conn)
    
    # WordCloud
    wordcloud = WordCloud(background_color='white', width=800, height=400).generate(' '.join(summary_df['summary']))

    # Save WordCloud image to BytesIO object
    img_array = np.array(wordcloud.to_image())
    img_stream = BytesIO()

    # Convert the NumPy array to a PIL Image and save it
    Image.fromarray(img_array).save(img_stream, format='PNG')

    # Close the database connection
    conn.close()

    # Create bar chart
    fig_bar = px.bar(df_pivot, x=df_pivot.index, y=df_pivot.columns, barmode='stack')
    fig_bar.update_layout(title='Number of Issues per Category per Day', xaxis_title='Date', yaxis_title='Number of Issues')

    # Create pie chart
    fig_pie = px.pie(names=list(category_counts.keys()), values=list(category_counts.values()), title='Distribution of Issue Categories')

    # Create scatter plot
    fig_scatter = px.scatter(df_scatter, x='DATE(date)', y='issue_category', title='Issues Scatter Plot')

    # Create WordCloud
    encoded_image = base64.b64encode(img_stream.getvalue()).decode()
    fig_wordcloud = html.Img(src=f'data:image/png;base64,{encoded_image}', style={'width': '100%', 'height': '50%'})

    # Convert the Plotly figures to Div
    div = html.Div([
        dcc.Graph(figure=fig_bar),
        dcc.Graph(figure=fig_pie),
        dcc.Graph(figure=fig_scatter),
        fig_wordcloud
    ])

    return div




