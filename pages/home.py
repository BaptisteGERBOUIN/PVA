from dash import html, register_page

register_page(__name__, path='/', name='Menu', title='PVA', order=1,
              category='Accueil', icon='bi bi-house')

def layout():
    return html.Div(
        [
            'Bonjour, ceci est notre page de bienvenue :)'
        ],
    )