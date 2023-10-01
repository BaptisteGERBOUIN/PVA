from dash import Dash, dcc, html, page_container
from dash_bootstrap_components import themes, icons

from view.sidebar import getSidebar

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[themes.PULSE, icons.BOOTSTRAP],
    suppress_callback_exceptions=True
)

app.title = 'PVA'
app.layout = html.Div([
    getSidebar(),
    page_container
])

if __name__ == '__main__':
    app.run(debug=True)