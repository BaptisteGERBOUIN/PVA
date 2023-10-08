from dash import html
import dash_bootstrap_components as dbc

def getSidebar():
    return html.Div(
        [
            html.Div(
                [
                    html.Img(src='./assets/images/water-drop.png'),
                    html.Span('Dash River'),
                ],
                className='water-menu-icon',
            ),
            dbc.Nav(
                [
                    html.H2('Accueil', className='water-menu-heading'),
                    getMenuLink('Menu', '/', 'house'),
                    html.H2('Visualisation', className='water-menu-heading'),
                    getMenuLink('Baptiste', '/baptiste', 'water'),
                    getMenuLink('Alexandre', '/alexandre', 'moisture'),
                    html.H2('Données', className='water-menu-heading'),
                    getMenuLink('Origine', '/origin', 'database-check'),
                    getMenuLink('Table', '/table', 'table'),
                ],
                className='water-menu-body',
            ),
        ],
        id='app_sidebar',
    )

def getMenuLink(name: str, path: str, icon_text: str):
    return dbc.NavLink(
        [
            html.I(className=f'bi bi-{icon_text} sidebar_icon'),
            html.Span(name),
            html.Div(className='water-menu-fill-hover'),
        ],
        href=path,
        className='water-menu-link',
        active='exact',
    )