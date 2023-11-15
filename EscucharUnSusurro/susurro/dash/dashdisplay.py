import dash
from dash import dcc, html
import folium
from dash.dependencies import Input, Output
import json
import geopandas as gpd
from buildinfo import *
import xml.etree.ElementTree as ET

app = dash.Dash(__name__)

def add_markers_cluster(mymap, results_dict, kml_path):
    # Parse KML data
    tree = ET.parse(kml_path)
    root = tree.getroot()

    # Add markers for each user
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
                            popup=f'Contact: {num}, Router Type: {router}, Building: {bname}',
                            icon=folium.Icon(color=iconcolor, icon='earphone')
                        ).add_to(mymap)

def create_folium_map(geojson_path, buildings_geojson_path):
    # Load GeoJSON data
    with open(geojson_path, 'r') as f:
        geojson_data = json.load(f)

    # Load buildings GeoJSON
    buildings_gdf = gpd.read_file(buildings_geojson_path)

    # Calculate the average latitude and longitude
    avg_latitude = buildings_gdf['geometry'].centroid.y.mean()
    avg_longitude = buildings_gdf['geometry'].centroid.x.mean()

    # Create a Folium map
    mymap = folium.Map(location=[avg_latitude, avg_longitude], zoom_start=14)

    # Add GeoJSON layer
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

    # Add buildings as CircleMarkers
    for index, row in buildings_gdf.iterrows():
        name = row['name']
        lat, lon = row['geometry'].y, row['geometry'].x
        if name != "Untitled Path":
            folium.CircleMarker(location=[lat, lon], radius=5, color='green', fill=True, fill_color='blue', popup=name).add_to(mymap)

    return mymap

#results_dict = getresultsdict()
geojson_path = '../geobank/network_plans.geojson'
buildings_geojson_path = '../geobank/buildings.geojson'
kml_path = '../geobank/doc.kml'
#plots_div = generate_plots()
# Initial map creation without markers
mymap = create_folium_map(geojson_path, buildings_geojson_path)

# Navbar layout
navbar = html.Nav(
    children=[
        html.Ul(
            children=[
                html.Li(html.A("Home", href="#")),
                html.Li(html.A("About", href="#about")),
            ],
            style={"list-style-type": "none", "margin": 0, "padding": 0},
        )
    ],
    style={"background-color": "#333", "padding": "10px"},
)

# Sidebar layout
sidebar = html.Div(
    [
        html.H2("Filtering Options"),
        dcc.RadioItems(
            id="dark-mode-toggle",
            options=[
                {"label": "Light Mode", "value": "light"},
                {"label": "Dark Mode", "value": "dark"},
            ],
            value="light",  # Default mode
            labelStyle={"display": "block", "margin-bottom": "10px"},
        ),
        dcc.Dropdown(
            id="date-dropdown",
            options=[
                {'label': 'Today', 'value': 'today'},
                {'label': 'Last One Week', 'value': 'last_week'},
                {'label': 'All', 'value': 'all'}
            ],
            value='today',  # Default value
            style={"margin-top": "10px"},
        ),
    ],
    style={"position": "fixed", "top": 0, "left": 0, "width": "15%", "height": "100vh", "padding": "20px"},
)
# Main content layout
content = html.Div(
    [   
        navbar,
        html.H1("A map showing Call Distribution over the Ahadi Konnect KCIS map."),
        html.Iframe(id="folium-map", srcDoc=mymap.get_root().render(), width="100%", height="600px", style={"border": "none"}),
        html.H1("Dashboard for Transcription Data"),
        html.Div(id='plots-div'),

    ],
    style={"margin-left": "20%"},
)

app.layout = html.Div([sidebar, content])
@app.callback(
    [Output("folium-map", "srcDoc"),
     Output('plots-div', 'children')],
    [Input("dark-mode-toggle", "value"),
     Input("date-dropdown", "value")]
)
def update_map(dark_mode, selected_date):
    print("Callback triggered with dark_mode:", dark_mode)
    print("Callback triggered with selected_date:", selected_date)

    # Ensure generate_plots is correctly imported
    plots_div = generate_plots()
    #plots_div = json.loads(plots_div) 
    print("Generated plots_div:", plots_div)

    # Update results_dict based on the selected date
    updated_results_dict = getresultsdict(selected_date)
    print("Updated results_dict:", updated_results_dict)

    add_markers_cluster(mymap, updated_results_dict, kml_path)

    return mymap.get_root().render(), plots_div

if __name__ == '__main__':
    app.run_server(debug=True)

