import requests as req
from tqdm import tqdm
from pymongo import MongoClient
from api_parameters import flowWaterObservation, flowWaterStation, qualityStation, qualityAnalyse, serviceIndicatorCommunes, serviceIndicatorIndicateurs, serviceIndicatorServices, donneesMeteorologique

#----
#Creation/Connexion à la DataBase

database_name = "BDD"
collection_name = "CollectionCoursdeau"
client = MongoClient("mongodb://localhost:27017")
db = client[database_name]
collection = db[collection_name]
#----


#----
#Fonction de recuperation des données pour les APIs de Hub eau

def get_data(url: str, params: dict) -> dict:
    
    r = req.get(url=url, params=params)
    r.raise_for_status()
    return r.json().get('data', [])
#----


#----
# Fonction permettant de rappeler la fonction get_data pour récupérer toutes les données que l'on veut
# C'est à dire sans la limite exigée par l'API (grâce à une boucle)

def get_all_data_with_specified_parameters(api_params: dict) -> dict:

    url = api_params['url']
    params = api_params['parameters']


    all_data = [] #Liste pour stocker toutes les données
    ceiling = 20_000_000# Nombre d'éléments à récupérer à chaque itération
    start_index = 0
    total_iterations_limit = 100
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
        # {'params': serviceIndicatorIndicateurs, 'name': 'serviceIndicatorIndicateurs'}, Travail encore en cours
        {'params': serviceIndicatorServices, 'name': 'serviceIndicatorServices'},
        # {'params': donneesMeteorologique, 'name': 'donneesMeteorologique'} Travail encore en cours
    ]

    for collection_info in collections:
        data = get_all_data_with_specified_parameters(collection_info['params'])

        insert_data_to_mongodb(data, database_name, collection_info['name'])
