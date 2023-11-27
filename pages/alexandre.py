from dash import html, register_page, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from datetime import date

from data.api_fetcher import get_water_flow_data
from data.geojson_processing import FRANCE

register_page(__name__, title='Water A')

# --- HTML ---

def layout():
    return html.Div(
        [
            menu_map(),
            dcc.Graph(figure=get_choropleth(), id='choropleth_mapbox')
        ],
    )

def menu_map():
    return html.Div(
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
    )

# --- FIGURE ---

def get_choropleth():
    fig = px.choropleth(
        data_frame=FRANCE.gdf, 
        geojson=FRANCE.gdf['geometry'], 
        locations=FRANCE.gdf.index, 
        center={'lon': FRANCE.geometry.centroid[0].x, 'lat': FRANCE.geometry.centroid[0].y + 0.25},
        fitbounds='locations')

    fig.update_layout(
        showlegend=False, 
        margin={'r': 0, 't': 0, 'l': 0, 'b': 0})

    return fig

# --- CALLBACKS ---

# fig = px.scatter_mapbox(geo_df,
#                         lat=geo_df.geometry.y,
#                         lon=geo_df.geometry.x,
#                         hover_name="name",
#                         zoom=1)