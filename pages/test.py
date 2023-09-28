from dash import html, register_page

register_page(__name__, title='TEST')

def layout():
    return html.Div([
        'Coucou'
    ], className='text-red text-xl font-medium')