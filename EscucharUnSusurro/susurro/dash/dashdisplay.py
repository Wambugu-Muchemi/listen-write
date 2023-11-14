import dash
from dash import dcc, html
import folium
from dash.dependencies import Input, Output
from folium.plugins import MarkerCluster
from buildinfo import *
import xml.etree.ElementTree as ET
from buildinfo import *
import folium
import json
import geopandas as gpd

app = dash.Dash(__name__)

results_dict = getresultsdict()

with open('../geobank/network_plans.geojson', 'r') as f:
    geojson_data = json.load(f)

buildings_geojson = "../geobank/buildings.geojson"
buildings_gdf = gpd.read_file(buildings_geojson)
avg_latitude = buildings_gdf['geometry'].centroid.y.mean()
avg_longitude = buildings_gdf['geometry'].centroid.x.mean()
mymap = folium.Map(location=[avg_latitude, avg_longitude], zoom_start=14)

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

marker_cluster = MarkerCluster().add_to(mymap)

for index, row in buildings_gdf.iterrows():
    name = row['name']
    lat, lon = row['geometry'].y, row['geometry'].x
    if name != "Untitled Path":
        folium.CircleMarker(location=[lat, lon], radius=5, color='green', fill=True, fill_color='blue', popup=name).add_to(marker_cluster)

tree = ET.parse('../geobank/doc.kml')
root = tree.getroot()

for num, user_info in results_dict.items():
    router = user_info['router']
    buildingcode = user_info['buildingcode']
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

    bname = user_info['bname']

    if buildingcode and ('Not Exist' not in buildingcode) and (isinstance(buildingcode, str) or isinstance(buildingcode, tuple)):
        if isinstance(buildingcode, str):
            buildingcode_list = [buildingcode]
        else:
            buildingcode_list = list(buildingcode)

        for bcode in buildingcode_list:
            for placemark in root.iter('{http://www.opengis.net/kml/2.2}Placemark'):
                name = placemark.find('{http://www.opengis.net/kml/2.2}name').text
                if bcode in name:
                    coordinates = placemark.find('{http://www.opengis.net/kml/2.2}Point/{http://www.opengis.net/kml/2.2}coordinates').text
                    coordinates_list = [float(coord) for coord in coordinates.split(',')]
                    longitude, latitude = coordinates_list[:2]
                    folium.Marker(
                        location=[latitude, longitude],
                        popup=f'Contact: {num}, Router Type: {router}, Building: {bname}', icon=folium.Icon(color=iconcolor, icon='earphone')
                    ).add_to(marker_cluster)


app.layout = html.Div(children=[
    html.H1("A Map showing Call Distribution over the AHADI KONNECT KCIS MAP."),
    html.Iframe(id='folium-map', srcDoc=mymap._repr_html_(), width='100%', height='600px'),
])

if __name__ == '__main__':
    app.run_server(debug=True)

