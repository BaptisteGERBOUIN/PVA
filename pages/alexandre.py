from dash import html, register_page, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from datetime import date

from data.api_fetcher import get_water_flow_data

register_page(__name__, title='Water A')

# --- HTML ---

def layout():
    return html.Div(
        [
            menu_map(),
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

# --- CALLBACKS ---

fig = px.scatter_mapbox(geo_df,
                        lat=geo_df.geometry.y,
                        lon=geo_df.geometry.x,
                        hover_name="name",
                        zoom=1)