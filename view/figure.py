import plotly.express as px
import pandas as pd

from data.map_pratical_data import Api

def build_pie_chart_map(df: pd.DataFrame, api: Api, parameter: str='default'):
    return px.pie(
        df,
        values='count',
        color='encoded_result',
        color_discrete_map=api.get_colorscale(parameter)
    )


def getboxplotprice(df, selected_departement, selected_annee):
    return px.box(df, x='code_departement', y='indicateur', points="all", labels={'indicateur': 'Prix du mètre cube d\'eau'},
        title=f"Prix du mètre cube d'eau pour le département {selected_departement} en {selected_annee}")
    
def getbarplotprice(df, selected_departement):
    return px.bar(df, x='annee', y='indicateur',labels={'indicateur': 'Evolution du prix du mètre cube moyen d\'eau'},
        title=f"Prix du mètre cube d'eau pour le département {selected_departement} sur 11 ans")

def getbarplotreclamation(df, selected_annee):
    return [px.bar(df, x="code_departement", y="indicateur", title=f"Taux de réclamation pour l'année {selected_annee}")]

def getboxplotrenouvellement(df):
    return [px.box(df, x="indicateur", notched=True)]

def getboxplotfrequence(df):
    return [px.violin(df, y="indicateur",box=True, points="all")]

def gethistopertes(df):
    return [px.histogram(df, x="annee", y="indicateur", marginal="box")]

def get_box_rendement(df):
    return [px.box(df, y="indicateur")]