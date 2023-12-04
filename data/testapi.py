import requests as req
import pandas as pd
from pymongo import MongoClient


database_name = "BDDTEST"
collection_name = "COLLECTIONTEST"

client = MongoClient("mongodb://localhost:27017")

db = client[database_name]

collection = db[collection_name]

print(f"La base de données '{database_name}' et la collection '{collection_name}' ont été créées avec succès.")


def get_data(url: str, params: dict) -> dict:
    
    r = req.get(url=url, params=params)
    r.raise_for_status()
    return r.json().get('data', [])


# Fonction pour récupérer les données
def get_water_flow_data_obs(limit: int = 10) -> list:
    url = 'https://hubeau.eaufrance.fr/api/v1/ecoulement/observations'
    params = {
        'size': str(limit),
        'fields': 'libelle_ecoulement,code_station,libelle_station,code_departement,libelle_departement,code_commune,libelle_commune,code_region,libelle_region,coordonnee_x_station,coordonnee_y_station,code_bassin,libelle_bassin,code_cours_eau,libelle_cours_eau,date_observation,code_ecoulement,libelle_ecoulement,latitude,longitude',
    }
    
    # Appeler la fonction get_data pour récupérer les données depuis l'API
    data = get_data(url, params)
    
    return data




def insert_data_to_mongodb(data: list, database_name: str, collection_name: str):
    # Connexion à MongoDB
    client = MongoClient("mongodb://localhost:27017")
    db = client[database_name]
    collection = db[collection_name]

    # Insérer les données dans la collection MongoDB
    collection.insert_many(data)


if __name__ == "__main__":
    # Récupérer les données
    data = get_water_flow_data_obs(limit=10)

    # Spécifier le nom de la base de données et de la collection MongoDB
    database_name = "BDDTEST"
    collection_name = "COLLECTIONTEST"

    # Insérer les données dans MongoDB
    insert_data_to_mongodb(data, database_name, collection_name)