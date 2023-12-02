import requests as req
from tqdm import tqdm
import pandas as pd
from pymongo import MongoClient
from api_parameters import flowWaterObservation, flowWaterStation, qualityStation, qualityAnalyse, serviceIndicatorCommunes, serviceIndicatorIndicateurs, serviceIndicatorServices

#----
#Creation/Connexion à la DataBase

database_name = "BDD"
collection_name = "CollectionCoursdeau"
client = MongoClient("mongodb://localhost:27017")
db = client[database_name]
collection = db[collection_name]
print(f"La base de données '{database_name}' et la collection '{collection_name}' ont été créées avec succès.")
#----


#----
#Fonction de recuperation des données

def get_data(url: str, params: dict) -> dict:
    
    r = req.get(url=url, params=params)
    r.raise_for_status()
    return r.json().get('data', [])
#----

#----
#Insertion des données dans la base de données

def get_all_data_with_specified_parameters(api_params: dict) -> dict:

    url = api_params['url']
    params = api_params['parameters']

    # Ajouter le champ 'fields' si présent dans les paramètres
    fields = params.get('fields')
    if fields:
        params['fields'] = fields  

    all_data = [] #Liste pour stocker toutes les données
    ceiling = 10_000 # Nombre d'éléments à récupérer à chaque itération
    start_index = 0
    total_iterations_limit = 1
    total_iterations = 0
    
    while total_iterations < total_iterations_limit:
        params['start'] = start_index # on ajoute le paramètre 'start' pour définir l'index de départ
        data = get_data(url, params) # on appelle la fonction get_data pour récupérer les données depuis l'API

        if not data:
            break

        all_data.extend(data) # On ajoute les données du lot actuel à la liste globale

        if len(data) < ceiling:  # on verifie s'il reste des données à récupérer
            break
        
        start_index += ceiling # on met à jour l'index de départ pour la prochaine itération

        total_iterations += 1
    
    return all_data
#----

#----
def insert_data_to_mongodb(data: list, database_name: str, collection_name: str):
    with MongoClient("mongodb://localhost:27017") as client: # Connexion à MongoDB
        db = client[database_name]
        collection = db[collection_name]
        # collection.insert_many(data) # On insere les données dans la collection MongoDB
        with tqdm(total=len(data), desc=f"Inserting data into {collection_name}", dynamic_ncols=True) as pbar:
            for chunk in data:
                collection.insert_one(chunk)
                pbar.update(1)
#----

#----
if __name__ == "__main__":
    database_name = "BDD"

    # Définir les paramètres pour chaque collection
    collections = [
        {'params': flowWaterObservation, 'name': 'flowWaterObservation'},
        {'params': flowWaterStation, 'name': 'flowWaterStation'},
        {'params': qualityStation, 'name': 'qualityStation'},
        {'params': qualityAnalyse, 'name': 'qualityAnalyse'},
        {'params': serviceIndicatorCommunes, 'name': 'serviceIndicatorCommunes'},
        # {'params': serviceIndicatorIndicateurs, 'name': 'serviceIndicatorIndicateurs'},
        # {'params': serviceIndicatorServices, 'name': 'serviceIndicatorServices'}
    ]

    for collection_info in collections:
        data = get_all_data_with_specified_parameters(collection_info['params'])

        insert_data_to_mongodb(data, database_name, collection_info['name'])
