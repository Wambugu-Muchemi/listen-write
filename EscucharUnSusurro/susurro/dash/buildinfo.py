import os
from dotenv import load_dotenv
load_dotenv() 
Bearer = os.getenv('Bearer')
apiurl = os.getenv('apiurl')

import requests
from pprint import pprint
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
# result = getbcode(num)
# #print(result)
# if isinstance(result, tuple):
#     #print("Result is a tuple")
#     router, num, buildingcode, bname = result
# else:
#     #print("Result is not a tuple")
#     buildingcode = 'Not Exist'
def getresultsdict():
    import sqlite3
    from pprint import pprint

    # Connect to the SQLite database
    conn = sqlite3.connect('../transcriptions.db')
    cursor = conn.cursor()

    # Initialize an empty dictionary to store results
    results_dict = {}

    # Retrieve unique contact numbers from the transcriptions table
    cursor.execute("SELECT DISTINCT contact FROM transcriptions WHERE contact IS NOT NULL;")
    # cursor.execute("SELECT DISTINCT contact FROM transcriptions WHERE contact IS NOT NULL AND (substr(date, 1, 10) = '2023-10-28' AND issue_category = 'Router Technical Problem');")


    contacts = cursor.fetchall()

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