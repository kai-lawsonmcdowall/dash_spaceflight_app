import dash
import dash_html_components as html
import dash_leaflet as dl
from dash.dependencies import Output, Input

# Assuming you have the data in the specified format
data = [
    {'Organisation': 'SpaceX',
     'Location': 'LC-39A, Kennedy Space Center, Florida, USA',
     'Date': 'Fri Aug 07, 2020 05:12 UTC',
     'Detail': 'Falcon 9 Block 5 | Starlink V1 L9 & BlackSky',
     'Rocket_Status': 'StatusActive',
     'Price': '50.0',
     'Mission_Status': 'Success',
     'Position': [-80.6042, 28.6083]},
    {'Organisation': 'CASC',
     'Location': 'Site 9401 (SLS-2), Jiuquan Satellite Launch Center, China',
     'Date': 'Thu Aug 06, 2020 04:01 UTC',
     'Detail': 'Long March 2D | Gaofen-9 04 & Q-SAT',
     'Rocket_Status': 'StatusActive',
     'Price': '29.75',
     'Mission_Status': 'Success',
     'Position': [40.966, 100.296]}
]

# Create the Dash app
app = dash.Dash(__name__)

# Create the layout
app.layout = html.Div([
    dl.Map(
        [dl.TileLayer(), dl.LayerGroup(id="marker-layer")],
        style={'width': '100%', 'height': '400px'},
        center=[0, 0],
        zoom=2
    )
])

# Add markers to the map
@app.callback(
    Output("marker-layer", "children"),
    [Input("marker-layer", "children")]
)
def update_markers(children):
    markers = []
    for d in data:
        location = d['Location']
        position = d['Position']
        marker = dl.Marker(location=position, children=dl.Tooltip(location))
        markers.append(marker)
    return markers

if __name__ == '__main__':
    app.run_server()
#%%
#%%