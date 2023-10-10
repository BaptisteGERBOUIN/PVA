from dash import html, register_page, dcc
import plotly.express as px

from data.api import get_nitrate_data

register_page(__name__, title='Water A')

def layout():
    return html.Div(
        [
            dcc.Graph(figure=scatter_charts()),
        ],
    )

def scatter_charts():
    fig = px.line(
        get_nitrate_data(), 
        x='date_prelevement', 
        y='resultat', 
        markers=True,
        title='Teneur en Nitrates à La Jalle de Blanquefort à Bordeaux '
    )
    return fig.update_layout(showlegend=False, title_x=0.5)
