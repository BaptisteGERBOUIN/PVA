from pymongo import MongoClient
import pandas as pd

from data.geojson_processing import get_departement_name

client = MongoClient("mongodb://localhost:27017")
db = client["pva_water_project"]
collection = db["indicateurs_services"]

#PREMIER INDICATEUR

def dataframe():
    resultats = collection.find({"code_indicateur": "D102.0"})
    df = pd.DataFrame(resultats)
    df = df.dropna(subset=['indicateur'])
    df = df.dropna(subset=['code_departement'])
    df['code_departement'] = df['code_departement'].astype(float)
    return df

def data_box_price(selected_annee, selected_departement):
    return dataframe()[(dataframe()['annee'] == selected_annee) & (dataframe()['code_departement'] == selected_departement)]

def data_bar_plot(selected_departement):
    moyenne_prix = dataframe().groupby(['code_departement', 'annee'])['indicateur'].mean().reset_index()
    moyenne_prix = moyenne_prix.dropna(subset=['indicateur'])
    filtered_moyenne = moyenne_prix[moyenne_prix['code_departement'] == selected_departement]
    return filtered_moyenne

def dropdown_annee():
    return dataframe()['annee']

def dropdown_departement():
    departement = get_departement_name()[['code', 'name']]
    departement['code'] = departement['code'].astype(int)
    departement = departement.sort_values('name')
    return departement

#DEUXIEME INDICATEUR

def data_bar_reclamation(selected_annee):
    resultats = collection.find({"code_indicateur": "P155.1"})
    df = pd.DataFrame(resultats)
    df = df.dropna(subset=['indicateur'])
    filtered_df = df[(df['annee'] == selected_annee)]
    sum_by_departement = filtered_df.groupby('code_departement')['indicateur'].sum().reset_index()  
    return sum_by_departement 

#TROISIEME INDICATEUR

def data_box_renouvellement(selected_annee):

    resultats = collection.find({"code_indicateur": "P107.2"})
    df = pd.DataFrame(resultats)
    df = df.dropna(subset=['indicateur'])
    max_by_departement = df.groupby(['code_departement', 'annee'])['indicateur'].max().reset_index()
    filtered_df = max_by_departement[max_by_departement['annee'] == selected_annee]

    return filtered_df

#QUATRIEME INDICATEUR

def data_bar_frequence(selected_annee, selected_departement):
    resultats = collection.find({"code_indicateur": "P151.1"})
    df = pd.DataFrame(resultats)
    df = df.dropna(subset=['indicateur'])
    df = df.dropna(subset=['code_departement'])
    df['code_departement'] = df['code_departement'].astype(float)
    filtered_df = df[(df['annee'] == selected_annee) & (df['code_departement'] == selected_departement)]
    return filtered_df

#CINQUIEME INDICATEUR

def data_histo_pertes(selected_departement):
    resultats = collection.find({"code_indicateur": "P106.3"})
    df = pd.DataFrame(resultats)
    df = df.dropna(subset=['indicateur'])
    df = df.dropna(subset=['code_departement'])
    df['code_departement'] = df['code_departement'].astype(float)
    filtered_df = df[(df['code_departement'] == selected_departement)]
    return filtered_df

#SIXIEME INDICATEUR

def data_box_rendement(selected_annee):
    resultats = collection.find({"code_indicateur": "P104.3"})
    df = pd.DataFrame(resultats)
    df = df.dropna(subset=['indicateur'])
    df = df.dropna(subset=['code_departement'])
    df['code_departement'] = df['code_departement'].astype(float)
    filtered_df = df[(df['annee'] == selected_annee)]
    return filtered_df

#SEPTIEME INDICATEUR

#HUITIEME INDICATEUR