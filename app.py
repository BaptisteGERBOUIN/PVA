from dash import Dash, html, page_container
from dash_bootstrap_components import themes, icons

from pages.menu.sidebar import getSidebar

app = Dash(
    __name__,
    use_pages=True,
    prevent_initial_callbacks=True,
    external_stylesheets=[themes.PULSE, icons.BOOTSTRAP],
    suppress_callback_exceptions=True,
)

app.title = 'PVA'
app._favicon = './images/water-drop.png'

app.layout = html.Div(
    [
        getSidebar(),
        html.Div(page_container.children, id='page_content'),
    ],
    id='layout',
    className='d-flex',
)

if __name__ == '__main__':
    app.run(debug=False)