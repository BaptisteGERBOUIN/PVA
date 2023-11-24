from dash import html, register_page, dcc
import dash_bootstrap_components as dbc
import plotly.express as px

from data.api_fetcher import get_water_flow_data

register_page(__name__, title='Water A')

# --- HTML ---

def layout():
    return html.Div(
        [   
            dcc.RangeSlider(0, 2,
                allowCross=False,
                step=None,
                marks={0: '11/03/2002', 1:'24/11/2023', 2:'31/12/2098'},
                tooltip={'placement': 'bottom'}),
            dbc.Tabs(
                [
                    dbc.Tab('cc', label='Qualité'),
                    dbc.Tab('dd', label='Quantité')
                ]
            , style={'justifyContent': 'center'})
        ],
    )

# --- FIGURE ---

# --- CALLBACKS ---