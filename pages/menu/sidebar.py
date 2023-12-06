from dash import html, page_registry
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
                getMenu(),
                className='water-menu-body',
            ),
        ],
        id='app_sidebar',
    )

def getMenu():
    menu = []
    category_name = ''
    for page in page_registry.values():
        if category_name != page.get('category'):
            category_name = page.get('category')
            menu.append(html.H2(category_name, className='water-menu-heading'))
        menu.append(getMenuLink(page.get('name'), page.get('path'), page.get('icon')))
    return menu

def getMenuLink(name: str, path: str, icon_text: str):
    return dbc.NavLink(
        [
            html.I(className=f'{icon_text} sidebar_icon'),
            html.Span(name),
            html.Div(className='water-menu-fill-hover'),
        ],
        href=path,
        className='water-menu-link',
        active='exact',
    )