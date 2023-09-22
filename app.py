from dash import Dash, dcc, html

app = Dash(__name__)
app.layout = html.Div([
    html.H1(children='Hi Barbie')
])

if __name__ == '__main__':
    app.run(debug=True)