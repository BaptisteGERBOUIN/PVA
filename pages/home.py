from dash import html, register_page

register_page(__name__, path='/', title='PVA')

def layout():
    return html.Div([
        getBookshelf()
    ], id='window')

def getBookshelf():
    return html.Div([
        getBook('home', '/'),
        getBook('data context', '/data'),
        getBook('baptiste', '/baptiste'),
        getBook('alexandre', '/alexandre'),
        getBook('table', '/table')
    ], id='bookshelf')

def getBook(id: str, url: str):
    return html.A([
        html.Div(className='bookTop'),
        html.Div([
            html.Div(className='bookLeft'),
            html.Div(id.upper(), className='bookTitle'),
            html.Div(className='bookRight')
        ], className='bookFront'),
    ], href=url, id=id.replace(' ', '_'), className='book')