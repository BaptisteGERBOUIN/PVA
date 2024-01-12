import dash
from dash import html, register_page
import dash_mantine_components as dmc

register_page(__name__, name='Origine', title='Origine', order=4,
              category='Données', icon='bi bi-database-check')

def layout():
    return [
            dmc.Tabs(
                [
                    dmc.TabsList(
                        [
                            dmc.Tab("Pourquoi avons-choisi ce thème?", value="theme"),
                            dmc.Tab("Sources et données", value="sources"),
                            dmc.Tab("Qui sommes-nous", value="equipe"),
                        ], grow=True,
                    ),
                    panel_theme(),

                    panel_sources(),

                    panel_equipe(),
                ],
                color="blue", 
                value="theme"
                )   
            ]


def panel_theme():
    return dmc.TabsPanel(
        [
            html.Div([
                html.P("Pourquoi avons-nous choisi ce thème?", 
                    style={'font-size': '1.5em', 'font-weight': 'bold', 'margin-bottom': '10px', 'marginTop': '40px', 'textAlign': 'center'}
                    ),
                html.Ol(
                    [
                        html.Li(
                            "Influence sur la santé humaine et sur l'environnement : "
                            "La santé humaine et l'écosystème sont directement liés à la qualité de l'eau. "
                            "La pollution des cours d'eau peut nuire à la santé publique, "
                            "tandis que la pollution des cours d'eau peut nuire à la biodiversité et aux écosystèmes aquatiques. "
                            "Nous sommes mieux équipés pour prendre des mesures préventives et correctives pour protéger l'environnement "
                            "et la santé humaine en comprenant ces aspects.",
                            style={'margin-bottom': '10px', 'align' : 'justify', 'margin-left': '150px', 'margin-right': '200px'},
                        ),
                        html.Li(
                            "Gestion durable des ressources hydriques : "
                            "L'eau est une ressource vitale, et son utilisation durable est cruciale pour répondre aux besoins actuels et futurs. "
                            "En analysant la quantité d'eau des cours d'eau, nous pouvons mieux comprendre la disponibilité de cette ressource "
                            "et prendre des décisions éclairées sur sa gestion. Cela comprend la mise en place de politiques et de pratiques pour "
                            "assurer un approvisionnement adéquat en eau tout en garantissant la durabilité des écosystèmes aquatiques.",
                            style={'margin-bottom': '10px', 'align' : 'justify', 'margin-left': '150px', 'margin-right': '200px'}
                        ),
                        html.Li(
                            "Adaptation aux changements climatiques et aux pressions anthropiques : "
                            "Les ressources en eau sont sous une pression accrue en raison des changements climatiques et de l'activité humaine. "
                            "L'analyse approfondie de la qualité des réseaux d'eau et des cours d'eau permet de suivre les changements, "
                            "d'identifier les sources de pollution et de mettre en œuvre des stratégies d'adaptation. "
                            "Nous pouvons développer des solutions durables pour atténuer les effets des changements climatiques "
                            "et de l'activité humaine sur nos ressources en eau en comprenant les impacts actuels et potentiels.",
                            style={'margin-bottom': '10px', 'margin-left': '150px', 'margin-right': '200px'}
                        ),
                    ],
                    style={'margin-left': '20px', 'align' : 'justify', 'margin-left': '150px', 'margin-right': '200px'}
                ),
                html.P(
                    "En somme, s'intéresser à la qualité des réseaux et cours d'eau ainsi qu'à la quantité d'eau disponible "
                    "revêt une importance cruciale pour garantir la santé, la durabilité et la résilience de nos ressources en eau, "
                    "tout en contribuant à la préservation de l'environnement et à la sécurité des communautés.",
                    style={'margin-top': '20px', 'margin-bottom': '10px', 'align' : 'justify', 'margin-left': '150px', 'margin-right': '200px'}
                ),
            ])],
            value="theme"
        )

def panel_sources():
    return dmc.TabsPanel(
        [
            html.Div([
                    html.P(
                        "Nous avons élaboré notre analyse en nous appuyant sur des sources de données fiables et reconnues, "
                        "principalement issues des sites Hub_eau, Naïades, et Eau France. Ces plateformes, "
                        "spécialisées dans la surveillance et la gestion des ressources en eau en France, "
                        "ont fourni des informations essentielles pour notre évaluation.",
                        style={'font-size': '1.2em', 'margin-bottom': '10px', 'marginTop': '40px'}
                    ),
                    html.P(
                        "Nous avons particulièrement exploité l'API du site Hub_eau pour accéder à des données relatives "
                        "à l'écoulement des cours d'eau, la qualité de ces cours d'eau, ainsi que les indicateurs des services liés à l'eau. "
                        "En ce qui concerne le stockage et la gestion de ces données, nous avons opté pour une base de données MongoDB. "
                        "Cette base de données NoSQL offre une flexibilité pour gérer les divers types de données provenant de différentes sources. "
                        "La structure de MongoDB nous permet d'organiser et de interroger les informations relatives à l'écoulement des cours d'eau, "
                        "à la qualité de l'eau, ainsi qu'aux indicateurs des services, garantissant ainsi une accessibilité optimale des données "
                        "pour nos utilisateurs.",
                        style={'margin-bottom': '20px'}
                    ),
                    ]),
                ],
                value="sources"
            )

def panel_equipe():
    return  dmc.TabsPanel(
        [
            html.Div([
                    html.P(
                            "Étudiants en première année de Master, nous avons réalisé ce projet dans le cadre de notre cursus (CMI ISI). "
                            "Le but étant de produire une visualisation analytique via un site web avec le sujet de notre choix. "
                            "Alexandre Leys et Baptiste Gerbouin, actuellement à l’Université de Bordeaux Sciences et Technologies, "
                            "nous sommes ravis de vous présenter le fruit de notre travail.",
                            style={'font-size': '1.2em', 'margin-bottom': '10px', 'marginTop': '40px'}
                        ),
                        html.P(
                            "C’est avec plaisir que nous recevons vos avis, quelle que soit leur nature, "
                            "pour pouvoir développer avec justesse et précision notre site.",
                            style={'margin-bottom': '10px'}
                        ),
                        html.P(
                            "Nous contacter :",
                            style={'font-weight': 'bold', 'margin-bottom': '5px'}
                        ),
                        html.P(
                            "Baptiste Gerbouin : bgerbouin@gmail.com",
                            style={'margin-bottom': '5px'}
                        ),
                        html.P(
                            "Alexandre Leys : alexandre.leys11@gmail.com",
                            style={'margin-bottom': '20px'}
                        ),                                
            ])], value="equipe"
        )