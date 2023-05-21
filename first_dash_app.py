# %%
import dash
import dash_html_components as html
import plotly.graph_objects as go
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd


# %%
"""Data Analysis"""
import os
app_dir = os.path.realpath(__file__)

# importing mission launches and coordinates
mission_launches = pd.read_csv("mission_launches_cleaned.csv")
long_and_lat = pd.read_csv("launch_long_and_lat.csv")
# %%
# merging the data
missions_with_coordinates = pd.merge(
    mission_launches, long_and_lat, on="Location", how="left"
)
missions_with_coordinates.dropna(inplace=True)

#%%
# mapping this to a world mpa
import folium
from folium.plugins import MarkerCluster
import pandas as pd

# Create the map
map = folium.Map(zoom_start=2, tiles='cartodbpositron')
marker_cluster = MarkerCluster().add_to(map)

# Iterate over the DataFrame rows
for index, row in missions_with_coordinates.iterrows():
    location = [row['Latitude'], row['Longitude']]
    popup = row['Location']

    # Create a marker for each location
    folium.Marker(
        location=location,
        popup=popup,
        icon=folium.Icon(color="black", icon="fa-thin fa-shuttle-space fa-rotate-270", prefix="fa"),
        rotation=-90
    ).add_to(marker_cluster)

#rotating the folium icon 90 degrees to the left.
map
# Convert the Folium map to HTML
folium_map_html = map._repr_html_()
#%%



# %%
# text
header_text = "Visualization of rocket launch data 🚀"

# dropdown options:
org_options = [
    {"label": "please select an organization", "value": "org_default"},
    {"label": "SpaceX"},
    {"label": "Roscosmos"},
    {"label": "NASA"},
]

# %%
app = dash.Dash()
app.layout = html.Div(
    id="parent",
    children=[
        html.H1(
            id="H1",
            children=header_text,
            style={
                "display": "flex",
                "justify-content": "center",
                "color": "#fff",
                "font-family": "Roboto, sans-serif",
                "marginTop": 10,  # decrease the margin top
                "marginBottom": 10,  # decrease the margin bottom
                "padding-left": "20px",
                "padding-top": "10px",  # decrease the padding top
                "padding-bottom": "5px",  # decrease the padding bottom
            },
        ),
        html.H2(
            id="subheading",
            children=[
                "It includes all the space missions that has been launched since the beginning of Space Race between the USA and the Soviet Union in 1957. This dataset can be found ",
                html.A(
                    "here",
                    href="https://www.kaggle.com/datasets/salmane/space-missions-launches",
                    style={"color": "white"},
                ),
            ],
            style={
                "text-align": "center",
                "padding": "20px",
                "color": "#fff",
                "font-family": "Roboto, sans-serif",
                "height": "20vh",
            },
        ),
        dcc.Dropdown(
            id="dropdown",
            options=org_options,
            value="org_default",
            style={
                "font-family": "Roboto, sans-serif",
            },
        ),
        html.Iframe(srcDoc=folium_map_html, style={'height': '500px', 'width': '100%'})
    ],
    style={
        "background-image": 'url("/assets/nightsky.jpg")',
        "background-size": "cover",
        "background-position": "center center",
    },
)

if __name__ == "__main__":
    app.run_server()
#%%