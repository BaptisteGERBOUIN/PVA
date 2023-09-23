from dash import Dash, dcc, html, page_container
from dash_bootstrap_components import themes, icons

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[themes.PULSE, icons.FONT_AWESOME, './css/bookshelf.css'],
    suppress_callback_exceptions=True
)

app.title = 'PVA'

app.layout = html.Div([
    page_container
])

if __name__ == '__main__':
    app.run(debug=True)