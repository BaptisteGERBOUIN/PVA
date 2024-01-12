from dash import html, register_page

register_page(__name__, path='/', title='PVA')

def layout():
    return html.Div(
        [
            html.H1(
                "Projet Visualisation Analytique",
                style={'font-weight': 'bold', 'textAlign': 'center'}
            ),
            div_home(),
        ],
    )

def div_home():
    return  html.Div(
        [
            html.P(
                "Chers visiteurs,",
                style={'font-size': 18, 'font-weight': 'bold', 'textAlign': 'center'}
            ),
            html.P(
                "C'est avec un immense plaisir que nous vous accueillons sur notre site dédié à l'analyse approfondie de la qualité des réseaux français, des cours d'eau, et de la quantité d'eau qui les traverse. "
                "Au cœur de notre mission, nous nous efforçons de vous offrir une vision exhaustive et détaillée de l'état actuel des ressources hydriques en France.",
            ),
            html.P(
                "Notre plateforme aspire à être une source fiable et incontournable pour tous ceux qui partagent un intérêt pour l'eau, sa qualité, et son impact sur notre environnement. "
                "Nous avons rassemblé des analyses minutieuses, des données précises et des évaluations complètes pour vous permettre de naviguer à travers la complexité des réseaux et cours d'eau français.",
            ),
            html.P(
                "Sur ce site, vous découvrirez non seulement des informations sur la qualité des réseaux, avec un accent particulier sur les paramètres physico-chimiques et bactériologiques, "
                "mais également des analyses approfondies sur la qualité des cours d'eau, mettant en lumière les enjeux et les avancées dans la préservation de ces précieuses ressources.",
            ),
            html.P(
                "La quantité d'eau dans nos cours d'eau est un sujet d'une importance capitale, et nous vous offrons une exploration détaillée de cette dimension importante à nos yeux. "
                "Nos analyses incluent des données actuelles et des tendances, avec l'objectif de vous informer de manière complète sur les défis et les opportunités liés à la disponibilité de l'eau en France.",
            ),
            html.P(
                "Nous sommes convaincus que la compréhension de ces aspects contribuera à sensibiliser davantage sur la nécessité de préserver et de gérer nos ressources hydriques. "
                "Nous vous encourageons à explorer toutes les sections de notre site, à vous plonger dans les données, et à partager vos réflexions avec nous.",
            ),
            html.P(
                "Vos retours et suggestions sont les bienvenus, car ils enrichissent notre démarche collective vers une meilleure compréhension et préservation de l'eau en France.",
            ),
            html.P(
                "Bienvenue sur notre site, et bonne navigation !",
            ),
            html.P(
                "Cordialement,",
                style={'font-size': 18, 'font-weight': 'bold', 'margin-top': '20px'}
            ),
            html.P(
                "L'équipe",
                style={'font-size': 18, 'font-weight': 'bold'}
            ),
        ],
    )