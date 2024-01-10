from dash import html, register_page, dcc
import plotly.express as px

register_page(__name__, name='Baptiste', title='Water B', order=2,
              category='Visualisation', icon='bi bi-water')

def layout():
    return html.Div(
        [
            dcc.Graph(figure=scatter_charts()),
            dcc.Graph(figure=bar_charts()),
        ],
    )

def scatter_charts():
    import pandas as pd
    import numpy as np
    fake_data = pd.DataFrame({'prix': range(100, 1000, 100), 
                              'quantité de boue': map(lambda x: x*x, range(20, 2, -2)),
                              'taille': np.random.random(9) * 100_000})
    fig = px.scatter(
        fake_data,
        size='taille',
        x='prix', 
        y='quantité de boue', 
        title='quantité de boue / prix'
    )
    return fig.update_layout(showlegend=False, title_x=0.5)

def bar_charts():
    import pandas as pd
    import numpy as np
    from data.geojson_processing import FRANCE
    fake_data = pd.DataFrame({'taux de conformité': np.random.random(len(FRANCE.childs))})
    fig = px.bar(
        fake_data,
        x=list(FRANCE.childs.keys()), 
        y='taux de conformité', 
        color='taux de conformité',
        title='Région / taux de conformité'
    )
    return fig.update_layout(showlegend=False, title_x=0.5)
