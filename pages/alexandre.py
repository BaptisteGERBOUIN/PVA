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
        get_water_flow_data().value_counts().reset_index(name='count'),
        x='libelle_ecoulement',
        y='count',
        color='libelle_ecoulement',
        title='Quantité des différentes catégories d\'écoulement d\'eau en France sur le mois de Juin.',
        log_y=True
    )
    return fig.update_layout(showlegend=False)