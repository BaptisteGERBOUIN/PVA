from dash import html, register_page

register_page(__name__, path='/', title='PVA')

def layout():
    return html.Div([
        getBookshelf()
    ], id='window')

def getBookshelf():
    return html.Div([
        getBook('home', '/', 'I'),
        getBook('data context', '/data', 'II'),
        getBook('baptiste', '/baptiste', 'III'),
        getBook('alexandre', '/alexandre', 'IV'),
        getBook('table', '/table', 'V')
    ], id='bookshelf')

def getBook(id: str, url: str, roman: str):
    return html.A([
        html.Div(className='bookTop'),
        html.Div([
            html.Div(className='bookLeft'),
            html.P(id, className='bookText bookTitle'),
            html.Div(className='bookRight'),
            html.Div(className='bookBarFront BookBar1'),
            html.Div(className='bookBarSide BookBar1'),
            html.Div(className='bookBarFront BookBar2'),
            html.Div(className='bookBarSide BookBar2'),
            html.Div(className='bookBarFront BookBar3'),
            html.Div(className='bookBarSide BookBar3'),
            html.Div(className='bookBarFront BookBar4'),
            html.Div(className='bookBarSide BookBar4'),
            html.P(roman, className='bookText bookIndex'),
        ], className='bookFront'),
    ], href=url, id=id.replace(' ', '_'), className='book')