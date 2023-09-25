from dash import html, register_page

register_page(__name__, title='Table')

def layout():
    return html.Div([
        bookPage(__name__.split(".")[-1])
    ], className='selectedBook')

def bookPage(name: str):
    return html.Div([
        html.Div(className='front'),
        html.Div(className='bar1'),
        html.Div([
            html.P(name, className='title')
        ], className='titleBox'),
        html.Div(className='bar2'),
        html.Div([
            html.I(className='bi bi-table')
        ], className='circle'),
        html.Div(className='bar3'),
        html.Div(className='bar4'),
    ], className='bookPage')