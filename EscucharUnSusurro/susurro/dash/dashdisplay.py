import dash
from dash import dcc, html
import folium
from dash.dependencies import Input, Output
from buildinfo import *
import xml.etree.ElementTree as ET
import json
import geopandas as gpd

app = dash.Dash(__name__, external_stylesheets=[
    'https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/slate/bootstrap.min.css', 
    'https://codepen.io/chriddyp/pen/bWLwgP.css'
])

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

for index, row in buildings_gdf.iterrows():
    name = row['name']
    lat, lon = row['geometry'].y, row['geometry'].x
    if name != "Untitled Path":
        folium.CircleMarker(location=[lat, lon], radius=5, color='green', fill=True, fill_color='blue', popup=name).add_to(mymap)

tree = ET.parse('../geobank/doc.kml')
root = tree.getroot()

for num, user_info in results_dict.items():
    router = user_info['router']
    buildingcode = user_info['buildingcode']
    bname = user_info['bname']
    iconcolor = determineIconcolor(buildingcode)

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
                    ).add_to(mymap)

# Sidebar layout
sidebar = html.Div(
    [
        html.H2("Sidebar Menu"),
        dcc.Checklist(
            id="toggle-options",
            options=[
                {"label": "Show Buildings", "value": "show_buildings"},
                {"label": "Show User Markers", "value": "show_user_markers"},
                # Add more options as needed
            ],
            value=["show_buildings", "show_user_markers"],  # Default selected options
        ),
        dcc.RadioItems(
            id="dark-mode-toggle",
            options=[
                {"label": "Light Mode", "value": "light"},
                {"label": "Dark Mode", "value": "dark"},
            ],
            value="light",  # Default mode
            labelStyle={"display": "block", "margin-bottom": "10px"},
        ),
    ],
    style={"position": "fixed", "top": 0, "left": 0, "width": "20%", "height": "100vh", "padding": "20px"},
)
# Main content layout
content = html.Div(
    [
        html.H1("A Map showing Call Distribution over the AHADI KONNECT KCIS MAP."),
        html.Iframe(id="folium-map", srcDoc=mymap._repr_html_(), width="80%", height="600px", style={"border": "none"}),
    ],
    style={"margin-left": "20%"},
)

app.layout = html.Div([sidebar, content])
# app.layout = html.Div(children=[
#     html.H1("A Map showing Call Distribution over the AHADI KONNECT KCIS MAP."),
#     html.Iframe(id='folium-map', srcDoc=mymap._repr_html_(), width='100%', height='600px'),
# ])
app.css.append_css({
    "external_url": [
        "https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/slate/bootstrap.min.css",  # Dark-themed Bootstrap
        "https://codepen.io/chriddyp/pen/bWLwgP.css",  # Dash CSS
    ]
})
@app.callback(
    Output("folium-map", "srcDoc"),
    [Input("toggle-options", "value"), Input("dark-mode-toggle", "value")]
)
def update_map(selected_options, dark_mode):

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

    for index, row in buildings_gdf.iterrows():
        name = row['name']
        lat, lon = row['geometry'].y, row['geometry'].x
        if name != "Untitled Path":
            folium.CircleMarker(location=[lat, lon], radius=5, color='green', fill=True, fill_color='blue', popup=name).add_to(mymap)

    tree = ET.parse('../geobank/doc.kml')
    root = tree.getroot()

    for num, user_info in results_dict.items():
        router = user_info['router']
        buildingcode = user_info['buildingcode']
        bname = user_info['bname']
        iconcolor = determineIconcolor(buildingcode)

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
                        ).add_to(mymap)

    # Example: Show/hide buildings based on user selection
    if "show_buildings" in selected_options:
        for index, row in buildings_gdf.iterrows():
            name = row['name']
            lat, lon = row['geometry'].y, row['geometry'].x
            if name != "Untitled Path":
                folium.CircleMarker(location=[lat, lon], radius=5, color='green', fill=True, fill_color='blue', popup=name).add_to(mymap)

    if dark_mode == "dark":
        app.css.clear()
        app.external_stylesheets = [
            "https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/darkly/bootstrap.min.css",  # Dark-themed Bootstrap
        ]
    else:
        app.css.clear()
        app.external_stylesheets = [
            "https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/slate/bootstrap.min.css",  # Light themed Bootstrap
            "https://codepen.io/chriddyp/pen/bWLwgP.css",  # Dash CSS

        ]

    return mymap._repr_html_()

if __name__ == '__main__':
    app.run_server(debug=True)

