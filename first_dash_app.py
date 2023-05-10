# %%
import dash
import dash_html_components as html
import plotly.graph_objects as go
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd


# %%
# ran sed -E 's/^[0-9]+,[0-9]+,//' /home/kai/dash/mission_launches.csv > /home/kai/dash/mission_launches_cleaned.csv to clean data.
mission_launches = pd.read_csv("mission_launches_cleaned.csv")

# %%
mission_launches

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
        dcc.Graph(
            id="bar_plot",
            figure=go.Figure(
                layout=dict(template="plotly_dark"),
            ),
        ),
    ],
    style={
        "background-image": 'url("/assets/nightsky.jpg")',
        "background-size": "cover",
        "background-position": "center center",
    },
)

if __name__ == "__main__":
    app.run_server()

# %%
mission_launches
# %%
unique_organisations = set(list(mission_launches["Organisation"]))
