# %%
import dash_bootstrap_components as dbc
import dash
import dash_html_components as html
import plotly.graph_objects as go
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output
import dash_leaflet as dl
import pandas as pd


# %%
"""Data"""
missions_with_coordinates = pd.read_csv(
    "/home/kai/dash_spaceflight_app/missions_with_coordinates.csv", index_col=0
)
missions_with_coordinates["Date"] = pd.to_datetime(missions_with_coordinates["Date"], format='mixed')

# extract the year and insert as a column. 
missions_with_coordinates['year'] = (missions_with_coordinates['Date'].astype(str).str[:4]).astype(int)
missions_with_coordinates

# %%
# text
header_text = "Visualization of rocket launch data 🚀"

# %%
app = dash.Dash(external_stylesheets=[dbc.themes.LUX])

url = "https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png"
attribution = '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a> '
icon_file_path = "/home/kai/dash_spaceflight_app/assets/rocket-solid.svg"

# Setup icon options, example from Leaflet doc (https://leafletjs.com/examples/custom-icons/).
icon = {
    "iconUrl": "https://www.clipartmax.com/png/small/157-1574618_space-shuttle-icon-space-shuttle-icon.png",
    "iconSize": [38, 95],  # size of the icon
    "shadowSize": [50, 64],  # size of the shadow
    "iconAnchor": [
        22,
        94,
    ],  # point of the icon which will correspond to marker's location
    "shadowAnchor": [4, 62],  # the same for the shadow
    "popupAnchor": [
        -3,
        -76,
    ],  # point from which the popup should open relative to the iconAnchor
}


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
        html.H3(
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
      dl.Map(
            [
                dl.TileLayer(url=url, attribution=attribution),
                dl.MarkerClusterGroup(
                    id="markers",
                    children=[
                        dl.Marker(
                            position=[row["Latitude"], row["Longitude"]],
                            children=[
                                dl.Tooltip(
                                    row["Location"],
                                ),
                            ],
                        )
                        for _, row in missions_with_coordinates.iterrows()
                    ],
                ),
            ],
            style={"width": "100%", "height": "1000px"},
            zoom=3,  # Set the initial zoom level to show the whole world map
            center=[0, 0],  # Set the center of the map to the coordinates [0, 0]
        ),
        html.Div(html.Br()),
        html.Div(html.Br()),
        dcc.RangeSlider(
            min =  missions_with_coordinates["year"].min(),
            max =  missions_with_coordinates["year"].max(),
            step = 2,
            value=[missions_with_coordinates["year"].min(), missions_with_coordinates["year"].max()],
            tooltip={"placement": "bottom", "always_visible": True},
             marks={str(year): str(year) for year in missions_with_coordinates["year"].unique() if year % 2 == 0 },
            id = 'year_slider',
            className='custom-range-slider'
        ),
    ],
    style={
        "background-image": 'url("/assets/launch.jpg")',
        "background-size": "cover",
        "background-position": "center center",
        "height": "100vh",
    },
)


@app.callback(
    Output(component_id='markers', component_property='children'),
    Input(component_id='year_slider', component_property='value')
)
def update_map_markers(year_range): # have to use the input component property in the function in this case? 
    start_year, end_year = year_range
    filtered_missions = missions_with_coordinates.query('year >= @start_year and year <= @end_year')

    filtered_markers = [
        dl.Marker(
            position=[row["Latitude"], row["Longitude"]],
            children=[
                dl.Tooltip(row["Location"]),
            ],
        )
        for _, row in filtered_missions.iterrows()
    ]

    return filtered_markers




if __name__ == "__main__":
    app.run_server()

#%%