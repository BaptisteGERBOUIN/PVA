import requests
from pymongo import MongoClient

# Remplacez ces valeurs par les informations spécifiques à votre configuration
mongodb_url = "mongodb://localhost:27017/"
database_name = "votre_base_de_donnees"
collection_name = "ma_collection"
api_url = "https://hubeau.eaufrance.fr/api/v1/qualite_cours_eau"



# Paramètres de la requête (vous pouvez ajuster ces paramètres selon vos besoins)
params = {
    'format': 'json',   # Format de réponse (json, xml, csv, etc.)
    'size': 100,        # Nombre maximal d'éléments à récupérer par requête
    # Ajoutez d'autres paramètres selon la documentation de l'API pour filtrer les données
}

# Effectuer la requête HTTP
response = requests.get(api_url, params=params)

# Vérifier si la requête a réussi (code 200)
if response.status_code == 200:
    data = response.json()
    # Traitez les données comme vous le souhaitez
    print(data)
else:
    print(f"Erreur lors de la requête HTTP: {response.status_code}")