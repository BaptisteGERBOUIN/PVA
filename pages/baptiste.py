from dash import html, register_page, dcc, callback, Output, Input, State, no_update, ctx
import dash_mantine_components as dmc

import data.requestsbaptiste as req_baptiste
import view.figure as figure

register_page(__name__, name='Baptiste', title='Water B', order=2,
              category='Visualisation', icon='bi bi-water')

# --- HTML ---

def layout():
    return [
            dmc.Tabs(
                [
                    dmc.TabsList(
                        [
                            dmc.Tab("Abonnés", value="abonnes"),
                            dmc.Tab("Réseau", value="reseau"),
                        ], grow=True,
                    ), 
                    panel_abonne(),

                    panel_reseau()
                ], 
                value="abonnes",
                style={'width': '100%'}
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

def panel_prix():
    return dmc.TabsPanel(
        [
            html.H1("Prix du mètre cube d'eau par département"),
            dropdown_year("dropdown-annee-prix"),
            dropdown_department("dropdown-departement-prix"),
            dcc.Graph(id='prix-m3-graph'),
            dcc.Graph(id='prix-m3-graph2'),
            
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
        ],
        value="prix",
    )

def panel_taux():
    return dmc.TabsPanel(
        [
            html.H1("Taux de réclamations"),
            dropdown_year("dropdown-annee-reclamation"),
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

        ],
        value="taux"
    )

def panel_frequence():
    return dmc.TabsPanel(
        [
            html.H1("Représentation de la fréquence des interruptions de service non programmées"),
            dropdown_year("dropdown-annee-frequence"),
            dropdown_department("dropdown-departement-frequence"),
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

        ],
        value="frequence"
    )

def panel_renouvellement():
    return dmc.TabsPanel(
        [
            html.H1("Représentation de pourcentage maximum par département du taux de renouvellement du réseau d'eau en France"),
            dropdown_year("dropdown-annee-indicateur"),
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

        ],
        value="renouvellement"
    )

def panel_perte():
    return dmc.TabsPanel(
        [
            html.H1("Représentation du total des pertes par année en France"),
            dropdown_department("dropdown-departement-perte"),

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
        ],
        value="perte"
    )

def panel_rendement():
    return dmc.TabsPanel(
        [
            html.H1("Représentation du rendement du réseau de distribution en France"),
            dropdown_year("dropdown-annee-rendement"),
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

        ],
        value="rendement"
    )

def dropdown_year(id: str):
    years = req_baptiste.dropdown_annee().unique()
    return dcc.Slider(
        id=id,
        min=years.min(),
        max=years.max(),
        step=1,
        marks={str(year): str(year) for year in years},
        value=years.max(),
        included=False
    )

def dropdown_department(id: str):
    departement = req_baptiste.dropdown_departement()
    return dcc.Dropdown(
        id=id,
        options=[
            {'label': row.iloc[1], 'value': row.iloc[0]} for _, row in departement.iterrows()
        ],
        value=departement['code'].iloc[0],
        multi=False,
        clearable=False,
    )

# --- CALLBACKS ---

@callback(
    [Output('prix-m3-graph', 'figure'),
     Output('prix-m3-graph2', 'figure')],
    [Input('dropdown-annee-prix', 'value'),
     Input('dropdown-departement-prix', 'value')],
)
def update_m3_graph(selected_annee, selected_departement):
    filtered_df = req_baptiste.data_box_price(selected_annee, selected_departement)
    fig = figure.getboxplotprice(filtered_df, selected_annee, selected_departement)
    filtered_moyenne = req_baptiste.data_bar_plot(selected_departement)
    fig2 = figure.getbarplotprice(filtered_moyenne, selected_departement)
    return fig, fig2

@callback(
    [Output('reclamation-graph', 'figure')],
    [Input('dropdown-annee-reclamation', 'value')]
)
def update_reclamation_graph(selected_annee):
    return figure.getbarplotreclamation(req_baptiste.data_bar_reclamation(selected_annee), selected_annee)

@callback(
    [Output('max-indicateur-graph', 'figure')],
    [Input('dropdown-annee-indicateur', 'value')]
)
def update_max_indicateur_graph(selected_annee):
    return figure.getboxplotrenouvellement(req_baptiste.data_box_renouvellement(selected_annee))

@callback(
    [Output('frequence-graph', 'figure')],
    [Input('dropdown-annee-frequence', 'value'),
     Input('dropdown-departement-frequence', 'value')
    ]
)
def update_frequence_graph(selected_annee, selected_departement):
    return figure.getboxplotfrequence(req_baptiste.data_bar_frequence(selected_annee, selected_departement))

@callback(
    [Output('perte-graph', 'figure')],
    [Input('dropdown-departement-perte', 'value')]
)
def update_perte_graph(selected_departement):
    return figure.gethistopertes(req_baptiste.data_histo_pertes(selected_departement))

@callback(
    [Output('rendement-graph', 'figure')],
    [Input('dropdown-annee-rendement', 'value')]
)
def update_rendement_graph(selected_annee):
    return figure.get_box_rendement(req_baptiste.data_box_rendement(selected_annee))