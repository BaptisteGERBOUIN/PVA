from dash import html, register_page, dcc
import plotly.express as px

from data.api_fetcher import get_water_flow_data

register_page(__name__, title='Water A')

def layout():
    return html.Div(
        [
            dcc.Graph(figure=bar_charts()),
        ],
    )

def bar_charts():
    fig = px.bar(
        get_water_flow_data(),
        x='libelle_ecoulement',
        y='Quantité',
        color='libelle_ecoulement',
        title='Quantité des différentes catégories d\'écoulement d\'eau en France sur le mois de Juin.'
    )
    return fig.update_layout(showlegend=True, title_x=0.5) 