from dash import html, register_page, dcc, callback, Output, Input, State, no_update, ctx
import dash_mantine_components as dmc

from data.requestsbaptiste import data_box_price, data_bar_plot, dropdown_annee, dropdown_departement, data_bar_reclamation, data_box_renouvellement, data_bar_frequence, data_histo_pertes, data_box_rendement
from view.figure import getboxplotprice, getbarplotprice, getbarplotreclamation, getboxplotrenouvellement, getboxplotfrequence, gethistopertes, get_box_rendement

register_page(__name__, name='Baptiste', title='Water B', order=2,
              category='Visualisation', icon='bi bi-water')

def layout():
    return [
            dmc.Tabs(
                [
                    dmc.TabsList(
                        [
                            dmc.Tab("Abonnés", value="abonnes"),
                            dmc.Tab("Réseau", value="reseau"),
                            dmc.Tab("Qualité de l'eau potable", value="qualite"),
                        ], grow=True,
                    ), 
                    panel_abonne(),

                    panel_reseau(), 

                    panel_qualite(), 
                ], 
                value="abonnes"
            ), 
    ]


def panel_abonne():
    return dmc.TabsPanel(
        [
            dmc.Tabs(
                [
                    dmc.TabsList(
                        [
                            dmc.Tab("Prix au mètre cube", value="prix"),
                            dmc.Tab("Taux de réclamations", value="taux"),
                            dmc.Tab("Fréquence des interruptions de service non programmées", value="frequence"),
                        ], grow=True,
                    ),
                    panel_prix(),

                    panel_taux(),

                    panel_frequence(),
                ],
                value="prix"
            ),
        ],
        value="abonnes",
    )


def panel_reseau():
    return  dmc.TabsPanel(
        [
            dmc.Tabs(
                [
                    dmc.TabsList(
                        [
                            dmc.Tab("Renouvellement des réseaux d'eau potable", value="renouvellement"),
                            dmc.Tab("Pertes en réseau", value="perte"),
                            dmc.Tab("Rendement du réseau de distribution", value="rendement"),
                        ], grow=True,
                    ), 
                    panel_renouvellement(),
                    panel_perte(),
                    panel_rendement(),
                ], value="renouvellement"
            ),
        ],
        value="reseau",
    )


def panel_qualite():
    return  dmc.TabsPanel(
        [
            dmc.Tabs(
                [
                    dmc.TabsList(
                        [
                            dmc.Tab("Conformité physico-chimique de l’eau au robinet", value="physico"),
                            dmc.Tab("Conformité microbiologique de l’eau au robinet", value="microbio"),
                        ], grow=True,
                    ), 
                    panel_physico(),
                    panel_microbio(),
                ], value="physico"
            ),
        ],
        value="qualite",
    ) 


def panel_prix():
    return dmc.TabsPanel(
        [
            dmc.Tabs(
                [
                    dmc.TabsList(
                        [
                            dmc.Tab("Les graphiques", value="graphique"),
                            dmc.Tab("La fiche explicative", value="fiche"),
                        ], grow=True,
                    ),
                    panel_graphique_prix(),

                    panel_fiche_prix(),

                ],
                value="graphique"
            ),
        ],
        value="prix",
    )

def dropdown_year():
    return dcc.Dropdown(
        id='dropdown-annee',
        options=[
            {'label': annee, 'value': annee} for annee in dropdown_annee().unique()
        ],
        value=dropdown_annee().unique()[0],
        multi=False,
        clearable=False,
    )

def dropdown_department():
    return dcc.Dropdown(
        id='dropdown-departement',
        options=[
            {'label': departement, 'value': departement} for departement in dropdown_departement().unique()
        ],
        value=dropdown_departement().unique()[0],
        multi=False,
        clearable=False,
    )

def panel_graphique_prix():
    return html.Div(
        [
            html.H1("Prix du mètre cube d'eau par département"),
            dropdown_year(),
            dropdown_department(),
            dcc.Graph(id='prix-m3-graph'),
            dcc.Graph(id='prix-m3-graph2'),
        ]
    )

def panel_fiche_prix():
    return html.Div( 
        [
            html.H2("Indicateur : Prix du service au m³"),

            html.H3("Définition"),
            html.P([
                "Le prix au m3 est calculé pour une consommation annuelle de 120 m3 (référence INSEE). Fixé par les organismes publics, ",
                "le prix dépend notamment de la nature et de la qualité de la ressource en eau, des conditions géographiques, ",
                "de la densité de population, du niveau de service choisi, de la politique de renouvellement du service, ",
                "des investissements réalisés et de leur financement."
            ], style={'font-size': '1.2em', 'margin-bottom': '10px', 'marginTop': '10px'}),

            html.H3("Unité"),
            html.P("Il est exprimé en : €/m³", style={'font-size': '1.2em', 'margin-bottom': '10px', 'marginTop': '10px'}),

            html.H3("Fréquence de détermination"),
            html.P([
                "Le prix est celui en vigueur au 1er janvier de l’année de présentation du rapport (c'est-à-dire au 1er janvier de l’année N+1 ",
                "pour l’indicateur relatif à l’année N)."
            ], style={'font-size': '1.2em', 'margin-bottom': '10px', 'marginTop': '10px'}),

            html.A("Lien vers le document", href="https://www.services.eaufrance.fr/documents/indicators/D102.0.pdf", target="_blank")
        ]
    )




def panel_taux():
    return  html.Div(
        [
            html.H1("Taux de réclamations"),
            dropdown_year(),
            dcc.Graph(id='reclamation-graph'),

            html.H2("Indicateur : Taux de réclamations"),

            html.H3("Définition"),
            html.P([
                "Cet indicateur mesure le niveau de réclamations écrites enregistrées par le service de l'eau, ",
                "exprimé en proportion pour chaque tranche de 1000 abonnés. En d'autres termes, il évalue le nombre de plaintes ",
                "formelles écrites reçues par le service de l'eau, ajusté pour représenter le taux de réclamations pour chaque ",
                "tranche de 1000 abonnés au service.",
                "Cela permet d'avoir une idée du niveau de satisfaction ou d'insatisfaction des abonnés vis-à-vis du service de l'eau, ",
                "en prenant en compte la taille de la base d'abonnés. Un indicateur plus élevé pourrait indiquer un niveau de service ",
                "insatisfaisant, tandis qu'un indicateur plus bas suggère généralement un niveau de satisfaction plus élevé parmi les abonnés."
            ], style={'font-size': '1.2em', 'margin-bottom': '10px', 'marginTop': '10px'}),

            html.H3("Unité"),
            html.P("Il est exprimé en : nb/1000ab", style={'font-size': '1.2em', 'margin-bottom': '10px', 'marginTop': '10px'}),

            html.H3("Fréquence de détermination"),
            html.P([
                "Les réclamations prises en compte sont celles dont la date d’enregistrement par l’opérateur se situe entre le ",
                "01 janvier et le 31 décembre de l’année N."
            ], style={'font-size': '1.2em', 'margin-bottom': '10px', 'marginTop': '10px'}),

            html.A("Lien vers le document", href="https://www.services.eaufrance.fr/documents/indicators/P155.1.pdf", target="_blank")

        ])

def panel_frequence():
    return  html.Div(
        [
            html.H1("Représentation de la fréquence des interruptions de service non programmées"),
            dropdown_year(),
            dropdown_department(),
            dcc.Graph(id='frequence-graph'),

            html.H2("Indicateur : Continuité du service d'eau potable"),

            html.H3("Définition"),
            html.P([
                "Cet indicateur vise à évaluer la continuité du service d'eau potable en mesurant le nombre de coupures d'eau impromptues ",
                "pour lesquelles les abonnés n'ont pas été avertis au moins 24 heures à l'avance. Ce nombre est ensuite rapporté à une ",
                "base de 1000 abonnés.",
                "En d'autres termes, il quantifie le nombre d'interruptions non planifiées du service d'eau potable qui ont eu lieu sans ",
                "préavis suffisant, ajusté en fonction de la taille de la population d'abonnés. Cet indicateur est utile pour évaluer la ",
                "fiabilité du service d'eau potable, en mettant l'accent sur la fréquence des interruptions imprévues et sur la capacité du ",
                "fournisseur à informer les abonnés à l'avance. Un indicateur plus bas suggère une meilleure continuité du service et une ",
                "meilleure communication avec les abonnés en cas d'interruption."
            ], style={'font-size': '1.2em', 'margin-bottom': '10px', 'marginTop': '10px'}),

            html.H3("Unité"),
            html.P("Il est exprimé en : nb/1000ab", style={'font-size': '1.2em', 'margin-bottom': '10px', 'marginTop': '10px'}),

            html.H3("Fréquence de détermination"),
            html.P([
                "Les coupures d’eau prises en compte sont celles qui surviennent entre le 01 janvier et le 31 décembre de l’année N, ",
                "quelle que soit la date de l’information faite aux usagers."
            ], style={'font-size': '1.2em', 'margin-bottom': '10px', 'marginTop': '10px'}),

            html.A("Lien vers le document", href="https://www.services.eaufrance.fr/documents/indicators/P151.1.pdf", target="_blank")

        ])

def panel_renouvellement():
    return  html.Div(
        [
            html.H1("Représentation de pourcentage maximum par département du taux de renouvellement du réseau d'eau en France"),
            dropdown_year(),
            dcc.Graph(id='max-indicateur-graph'),

            html.H2("Indicateur : Taux de renouvellement du réseau d'eau potable"),

            html.H3("Définition"),
            html.P([
                "Ce texte signifie que l'indicateur en question mesure le taux de renouvellement moyen annuel du réseau d'eau potable ",
                "au cours des cinq dernières années. Ce taux est exprimé en pourcentage et est calculé par rapport à la longueur totale du ",
                "réseau d'eau potable, à l'exclusion des branchements.",
                "En d'autres termes, cet indicateur évalue la fréquence à laquelle les sections du réseau d'eau potable ont été remplacées ",
                "ou renouvelées au cours d'une période de cinq ans. Il exclut les branchements individuels du calcul, se concentrant plutôt ",
                "sur la longueur principale du réseau. Cette mesure peut être utile pour évaluer la maintenance et la modernisation du réseau ",
                "d'eau potable, ainsi que pour estimer la durabilité et la fiabilité du système au fil du temps."
            ], style={'font-size': '1.2em', 'margin-bottom': '10px', 'marginTop': '10px'}),

            html.H3("Unité"),
            html.P("Il est exprimé en : %", style={'font-size': '1.2em', 'margin-bottom': '10px', 'marginTop': '10px'}),

            html.H3("Fréquence de détermination"),
            html.P("Les données prises en compte sont celles qui sont connues au 31/12 de l’année N.", style={'font-size': '1.2em', 'margin-bottom': '10px', 'marginTop': '10px'}),

            html.A("Lien vers le document", href="https://www.services.eaufrance.fr/documents/indicators/P107.2.pdf", target="_blank")

        ])

def panel_perte():
    return  html.Div(
        [
            html.H1("Représentation du total des pertes par année en France"),
            dcc.Dropdown(
                id='dropdown-departement',
                options=[
                    {'label': departement, 'value': departement} for departement in dropdown_departement().unique()
                ],
                value=dropdown_departement().unique()[0],
                multi=False,
                clearable=False,
            ),
            dcc.Graph(id='perte-graph'),

            html.H2("Indicateur : Pertes en réseau"),

            html.H3("Définition"),
            html.P([
                "L'indice linéaire des pertes en réseau évalue les pertes par fuites sur le réseau de distribution en les rapportant à ",
                "la longueur totale des canalisations du réseau (hors branchements).",
                "En d'autres termes, cet indice mesure la proportion des pertes d'eau par fuites par rapport à la longueur du réseau de distribution ",
                "principal, en excluant les branchements. Cela permet d'obtenir une évaluation relative de l'efficacité du réseau en termes de gestion ",
                "des fuites d'eau. Un indice plus bas suggère une meilleure performance en matière de réduction des pertes d'eau, tandis qu'un indice ",
                "plus élevé peut indiquer des problèmes de fuites et de gestion du réseau. Cet indicateur est souvent utilisé dans le secteur de la ",
                "distribution d'eau pour évaluer et améliorer l'efficacité des réseaux de distribution."
            ], style={'font-size': '1.2em', 'margin-bottom': '10px', 'marginTop': '10px'}),

            html.H3("Unité"),
            html.P("Il est exprimé en : m³/km/j", style={'font-size': '1.2em', 'margin-bottom': '10px', 'marginTop': '10px'}),

            html.H3("Fréquence de détermination"),
            html.P("Le linéaire de réseau est celui qui est établi au 31 décembre de l’année N. Les volumes pris en compte sont ceux qui sont déterminés au titre de l’année N.",
                style={'font-size': '1.2em', 'margin-bottom': '10px', 'marginTop': '10px'}),

            html.A("Lien vers le document", href="https://www.services.eaufrance.fr/documents/indicators/P106.3.pdf", target="_blank")
        ])

def panel_rendement():
    return  html.Div(
        [
            html.H1("Représentation du rendement du réseau de distribution en France"),
            dropdown_year(),
            dcc.Graph(id='rendement-graph'),

            html.H2("Indicateur : Rendement du réseau de distribution"),

            html.H3("Définition"),
            html.P([
                "Cet indicateur mesure le rapport entre le volume d'eau consommé par les usagers (particuliers, industriels) et le volume d'eau introduit ",
                "dans le réseau de distribution d'eau potable, comprenant à la fois la consommation des usagers et le volume nécessaire pour la gestion ",
                "du dispositif d'eau potable par le service public.",
                "En d'autres termes, cet indicateur évalue l'efficacité de l'utilisation de l'eau dans une région ou un système en comparant la quantité d'eau ",
                "consommée par les usagers avec le volume total d'eau introduit dans le réseau. Cela peut aider à identifier les pertes d'eau, les fuites, ",
                "ou d'autres inefficacités dans le réseau de distribution d'eau potable. Un rapport plus élevé peut indiquer une utilisation inefficace de l'eau, ",
                "tandis qu'un rapport plus bas suggère une meilleure gestion et utilisation de la ressource en eau."
            ], style={'font-size': '1.2em', 'margin-bottom': '10px', 'marginTop': '10px'}),

            html.H3("Unité"),
            html.P("Il est exprimé en : %", style={'font-size': '1.2em', 'margin-bottom': '10px', 'marginTop': '10px'}),

            html.H3("Fréquence de détermination"),
            html.P("Les volumes pris en compte pour l’année N sont ceux déterminés au titre de l’année N.",
                style={'font-size': '1.2em', 'margin-bottom': '10px', 'marginTop': '10px'}),

            html.A("Lien vers le document", href="https://www.services.eaufrance.fr/documents/indicators/P104.3.pdf", target="_blank")

        ])

def panel_physico():
    return  html.Div(
        [
            # html.H1("Prix du mètre cube d'eau par département"),
            # dcc.Dropdown(
            #     id='dropdown-annee',
            #     options=[
            #         {'label': annee, 'value': annee} for annee in dropdown_annee().unique()
            #     ],
            #     value=dropdown_annee().unique()[0],
            #     multi=False,
            #     clearable=False,
            # ),
            # dcc.Dropdown(
            #     id='dropdown-departement',
            #     options=[
            #         {'label': departement, 'value': departement} for departement in dropdown_departement().unique()
            #     ],
            #     value=dropdown_departement().unique()[0],
            #     multi=False,
            #     clearable=False,
            # ),
            # dcc.Graph(id='prix-m3-graph'),
            # dcc.Graph(id='prix-m3-graph2'),

            html.H2("Indicateur : Conformité physico-chimique de l’eau au robinet"),

            html.H3("Définition"),
            html.P([
                "Cet indicateur évalue le respect des limites réglementaires de qualité de l'eau distribuée aux usagers, en se concentrant sur des paramètres ",
                "physico-chimiques spécifiques tels que pesticides, nitrates, chrome, bromate. Pour effectuer cette évaluation, l'indicateur se base sur les mesures ",
                "réalisées par l'Agence Régionale de Santé (ARS), et dans certaines circonstances, sur celles de l'exploitant du système de distribution d'eau.",
                "En d'autres termes, l'indicateur permet de vérifier si la qualité de l'eau distribuée répond aux normes réglementaires établies pour différents ",
                "composants chimiques et physiques. Les paramètres mentionnés, tels que pesticides, nitrates, chrome et bromate, sont souvent soumis à des normes ",
                "spécifiques en raison de leurs implications sur la santé humaine. L'ARS et l'exploitant effectuent des mesures régulières pour s'assurer que ces ",
                "normes sont respectées, et cet indicateur offre une évaluation synthétique de cette conformité."
            ], style={'font-size': '1.2em', 'margin-bottom': '10px', 'marginTop': '10px'}),

            html.H3("Unité"),
            html.P("Il est exprimé en : %", style={'font-size': '1.2em', 'margin-bottom': '10px', 'marginTop': '10px'}),

            html.H3("Fréquence de détermination"),
            html.P("Les prélèvements pris en compte sont ceux dont la date de prise des échantillons est comprise entre le 01 janvier et le 31 décembre de l’année N.",
                style={'font-size': '1.2em', 'margin-bottom': '10px', 'marginTop': '10px'}),

            html.A("Lien vers le document", href="https://www.services.eaufrance.fr/documents/indicators/P102.1.pdf", target="_blank")

        ])

def panel_microbio():
    return  html.Div(
        [
            # html.H1("Prix du mètre cube d'eau par département"),
            # dcc.Dropdown(
            #     id='dropdown-annee',
            #     options=[
            #         {'label': annee, 'value': annee} for annee in dropdown_annee().unique()
            #     ],
            #     value=dropdown_annee().unique()[0],
            #     multi=False,
            #     clearable=False,
            # ),
            # dcc.Dropdown(
            #     id='dropdown-departement',
            #     options=[
            #         {'label': departement, 'value': departement} for departement in dropdown_departement().unique()
            #     ],
            #     value=dropdown_departement().unique()[0],
            #     multi=False,
            #     clearable=False,
            # ),
            # dcc.Graph(id='prix-m3-graph'),
            # dcc.Graph(id='prix-m3-graph2'),

            html.H2("Indicateur : Conformité microbiologique de l’eau au robinet"),

            html.H3("Définition"),
            html.P([
                "Cet indicateur évalue le respect des limites réglementaires de qualité de l'eau distribuée aux usagers en ce qui concerne les paramètres ",
                "bactériologiques, notamment la présence de bactéries pathogènes dans l'eau. Pour effectuer cette évaluation, l'indicateur se base sur les mesures ",
                "réalisées par l'Agence Régionale de Santé (ARS), et dans certaines circonstances, sur celles de l'exploitant du système de distribution d'eau.",
                "En substance, cet indicateur vise à garantir que l'eau fournie aux usagers ne contient pas de niveaux dangereux de bactéries pathogènes, ",
                "conformément aux normes réglementaires. La présence de ces bactéries dans l'eau peut présenter des risques pour la santé humaine, d'où l'importance ",
                "de surveiller et de maintenir des niveaux de qualité d'eau sûrs. L'ARS et l'exploitant réalisent des mesures régulières pour s'assurer du respect de ",
                "ces normes, et l'indicateur offre une évaluation synthétique de la conformité de la qualité bactériologique de l'eau distribuée."
            ], style={'font-size': '1.2em', 'margin-bottom': '10px', 'marginTop': '10px'}),

            html.H3("Unité"),
            html.P("Il est exprimé en : %", style={'font-size': '1.2em', 'margin-bottom': '10px', 'marginTop': '10px'}),

            html.H3("Fréquence de détermination"),
            html.P("Les prélèvements pris en compte sont ceux dont la date de prise des échantillons est comprise entre le 01 janvier et le 31 décembre de l’année N.",
                style={'font-size': '1.2em', 'margin-bottom': '10px', 'marginTop': '10px'}),

            html.A("Lien vers le document", href="https://www.services.eaufrance.fr/documents/indicators/P101.1.pdf", target="_blank"),
        ]
    )

# --- CALLBACKS ---

@callback(
    [Output('prix-m3-graph', 'figure'),
     Output('prix-m3-graph2', 'figure')],
    [Input('dropdown-annee', 'value'),
     Input('dropdown-departement', 'value')],
)
def update_m3_graph(selected_annee, selected_departement):
    filtered_df = data_box_price(selected_annee, selected_departement)
    fig = getboxplotprice(filtered_df, selected_annee, selected_departement)
    filtered_moyenne = data_bar_plot(selected_departement)
    fig2 = getbarplotprice(filtered_moyenne, selected_departement)
    return fig, fig2

@callback(
    [Output('reclamation-graph', 'figure')],
    [Input('dropdown-annee', 'value')]
)
def update_reclamation_graph(selected_annee):
    return getbarplotreclamation(data_bar_reclamation(selected_annee), selected_annee)


@callback(
    [Output('max-indicateur-graph', 'figure')],
    [Input('dropdown-annee', 'value')]
)
def update_max_indicateur_graph(selected_annee):
    return getboxplotrenouvellement(data_box_renouvellement(selected_annee))

@callback(
    [Output('frequence-graph', 'figure')],
    [Input('dropdown-annee', 'value'),
     Input('dropdown-departement', 'value')
    ]
)
def update_frequence_graph(selected_annee, selected_departement):
    return getboxplotfrequence(data_bar_frequence(selected_annee, selected_departement))

@callback(
    [Output('perte-graph', 'figure')],
    [Input('dropdown-departement', 'value')]
)
def update_perte_graph(selected_departement):
    return gethistopertes(data_histo_pertes(selected_departement))

@callback(
    [Output('rendement-graph', 'figure')],
    [Input('dropdown-annee', 'value')]
)
def update_rendement_graph(selected_annee):
    return get_box_rendement(data_box_rendement(selected_annee))