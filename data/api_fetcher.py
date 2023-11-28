import requests as req
import pandas as pd
from pymongo import MongoClient


database_name = "BDD"
collection_name = "CollectionCoursdeau"

client = MongoClient("mongodb://localhost:27017")

db = client[database_name]

collection = db[collection_name]

print(f"La base de données '{database_name}' et la collection '{collection_name}' ont été créées avec succès.")



def get_data(url: str, params: dict) -> dict:
    
    r = req.get(url=url, params=params)
    r.raise_for_status()
    return r.json().get('data', [])


def get_water_flow_data_obs() -> dict:
    url = 'https://hubeau.eaufrance.fr/api/v1/ecoulement/observations'
    params = {
        'size': '2000',
        'fields': 'libelle_ecoulement,code_station,libelle_station,code_departement,libelle_departement,code_commune,libelle_commune,code_region,libelle_region,coordonnee_x_station,coordonnee_y_station,code_bassin,libelle_bassin,code_cours_eau,libelle_cours_eau,date_observation,code_ecoulement,libelle_ecoulement,latitude,longitude',
    }
    
    all_data = [] #Liste pour stocker toutes les données
    
    
    ceiling = 10000 # Nombre d'éléments à récupérer à chaque itération
    
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

def insert_data_to_mongodb(data: list, database_name: str, collection_name: str):
    
    client = MongoClient("mongodb://localhost:27017") # Connexion à MongoDB
    db = client[database_name]
    collection = db[collection_name]

    
    collection.insert_many(data) # On insere les données dans la collection MongoDB


if __name__ == "__main__":
    
    data = get_water_flow_data_obs() # On recupere les données

    database_name = "BDD"
    collection_name = "CollectionCoursdeau"

    
    insert_data_to_mongodb(data, database_name, collection_name) # On insere les données dans MongoDB
















#Récupération des données de l'API cours d'eau

# def get_water_flow_data_obs() -> dict: #Cours d'eau / observations 
#     url = 'https://hubeau.eaufrance.fr/api/v1/ecoulement/observations'
#     params = {
#         'size': '20000',
#         'date_observation_min': '2023-06-01',
#         'date_observation_max': '2023-06-30',
#         'fields': 'libelle_ecoulement,code_station,libelle_station,code_departement,libelle_departement,code_commune,libelle_commune,code_region,libelle_region,coordonnee_x_station,coordonnee_y_station,code_bassin,libelle_bassin,code_cours_eau,libelle_cours_eau,date_observation,code_ecoulement,libelle_ecoulement,latitude,longitude',
#     }
#     return get_data(url, params).fillna('Données manquantes').value_counts().reset_index(name='Quantité')

def get_water_flow_data_station() -> dict: #Cours d'eau / station 
    url = 'https://hubeau.eaufrance.fr/api/v1/ecoulement/stations'
    params = {
        'size': '20000',
        'date_observation_min': '2023-06-01',
        'date_observation_max': '2023-06-30',
        'fields': 'code_station,libelle_station,code_departement,libelle_departement,code_commune,libelle_commune,code_region,libelle_region,coordonnee_x_station,coordonnee_y_station,code_cours_eau,libelle_cours_eau,date_maj_station,latitude,longitude',
    }
    return get_data(url, params).fillna('Données manquantes').value_counts().reset_index(name='Quantité')


# datacoursdeau = get_water_flow_data_station()
# datacoursdeau.to_csv('.datacoursdeau.csv')


#Récupération des données de l'API Qualité de l'eau

def get_water_quality_data_analyse() -> dict: #Qualité des cours d'eau / analyse_pc 
    url = 'https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/analyse_pc'
    params = {
        'size': '20000',
        'date_observation_min': '2023-06-01',
        'date_observation_max': '2023-06-30',
        'fields': 'code_station, libelle_station,code_parametre,libelle_parametre,resultat,code_unite,symbole_unite,code_remarque,date_maj_analyse,longitude,latitude',
    }
    return get_data(url, params).fillna('Données manquantes').value_counts().reset_index(name='Quantité')


def get_water_quality_data_station() -> dict: #Qualité des cours d'eau / station_pc 
    url = 'https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/station_pc'
    params = {
        'size': '20000',
        'date_observation_min': '2023-06-01',
        'date_observation_max': '2023-06-30',
        'fields': 'code_station,libelle_station,coordonnee_x,coordonnee_y,longitude,latitude,code_commune,libelle_commune,code_departement,libelle_departement,code_region,libelle_region,code_cours_eau,date_maj_information',
    }
    return get_data(url, params).fillna('Données manquantes').value_counts().reset_index(name='Quantité')



#Récupération des données de l'API Indicateurs des services


def get_water_quality_data_analyse() -> dict: #Qualité des cours d'eau / analyse_pc 
    url = 'https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/analyse_pc'
    params = {
        'size': '20000',
        'date_observation_min': '2023-06-01',
        'date_observation_max': '2023-06-30',
        'fields': 'libelle_ecoulement,code_station,libelle_station,code_departement,libelle_departement,code_commune,libelle_commune,code_region,libelle_region,coordonnee_x_station,coordonnee_y_station,code_bassin,libelle_bassin,code_cours_eau,libelle_cours_eau,date_observation,code_ecoulement,libelle_ecoulement,latitude,longitude',
    }
    return get_data(url, params).fillna('Données manquantes').value_counts().reset_index(name='Quantité')


def get_water_quality_data_station() -> dict: #Qualité des cours d'eau / station_pc 
    url = 'https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/station_pc'
    params = {
        'size': '20000',
        'date_observation_min': '2023-06-01',
        'date_observation_max': '2023-06-30',
        'fields': 'libelle_ecoulement,code_station,libelle_station,code_departement,libelle_departement,code_commune,libelle_commune,code_region,libelle_region,coordonnee_x_station,coordonnee_y_station,code_bassin,libelle_bassin,code_cours_eau,libelle_cours_eau,date_observation,code_ecoulement,libelle_ecoulement,latitude,longitude',
    }
    return get_data(url, params).fillna('Données manquantes').value_counts().reset_index(name='Quantité')

# data2 = get_data('https://hubeau.eaufrance.fr/api/v0/indicateurs_services/indicateurs')
# data2.to_csv('.toto.csv')
