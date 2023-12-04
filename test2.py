import dash_leaflet as dl
from dash import Dash, html, Output, Input
import json
from data.geojson_processing import FRANCE
import dash_bootstrap_components as dbc
from datetime import date

from dash import register_page, Input, Output, State, no_update, callback
from dash import html, dcc

a = json.load(open('./data/territoire_france/departements_france.geojson', 'r'))
v = json.loads(FRANCE.gdf.to_json())

geojson = dl.GeoJSON(
    data=json.loads(FRANCE.gdf.to_json(drop_id=True)),
    zoomToBounds=True,
    zoomToBoundsOnClick=True,
    hoverStyle={'color': '#666'}
)

map = dl.Map(
    [
        # dl.TileLayer(), 
        geojson
    ],
    zoomSnap=0.2,
    dragging=True,
    maxBounds=[(42, -5.5), (51.5, 10)],
    id="my_map", 
    # style={'width': '100vw', 'height': '100vh'}
)

app = Dash(prevent_initial_callbacks=True)
app.layout = html.Div(
    [
        html.Div(
        [
            dbc.DropdownMenu(
                label='Type de la carte',
                children=[
                    dbc.DropdownMenuItem('Qualité'),
                    dbc.DropdownMenuItem('Quantité'),
                ],
                size='lg'
            ),
            dcc.DatePickerRange(
                id='my-date-picker-range',
                min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date(2017, 9, 19),
                initial_visible_month=date(2017, 7, 5),
                end_date=date(2017, 8, 25)
            ),
        ],
        style={'display': 'flex', 'justifyContent': 'space-evenly'}
    ),
        html.Div(
            map,
            id="map_container",
        )
    ],
    style={
        'position': 'fixed', 
        # 'width':'100%',
        'height':'100%',
        'top':'0px',
        'left':'0px',
        'margin': '0px',
        'width': '50%',
    }
)

if __name__ == '__main__':
    app.run_server(debug=True)