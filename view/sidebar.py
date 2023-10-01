from dash import html

def getSidebar():
    return html.Div([
        html.Div(html.Img(src='./assets/images/water_drop_lighter.png'), className='sidebar_main_icon'),
        html.H2('Accueil', className='sidebar_category_title'),
        getLink('Menu', '/', 'house'),
        html.H2('Affichage', className='sidebar_category_title'),
        getLink('Baptiste', '/baptiste', 'water'),
        getLink('Alexandre', '/alexandre', 'moisture'),
        html.H2('Données', className='sidebar_category_title'),
        getLink('Origine', '/origin', 'database-check'),
        getLink('Table', '/table', 'table'),
    ], id='sidebar')

def getLink(name: str, path: str, icon_text: str):
    return html.A([
        html.I(className=f'bi bi-{icon_text} sidebar_icon'),
        html.Div(
            html.Div(
                html.P(name, className='sidebar_text_link'),
            className='sidebar_text_link_box'),
        className='sidebar_text_link_background')
    ], href=path, className='sidebar_link')