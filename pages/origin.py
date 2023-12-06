from dash import html, register_page

register_page(__name__, name='Origine', title='Origine', order=4,
              category='Données', icon='bi bi-database-check')

def layout():
    return html.Div(
        [
            
        ],
    )


# Objectif, donner accès aux utilisateurs les bases de données que nous avons utilisées.