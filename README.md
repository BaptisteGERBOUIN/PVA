# PVA

Bienvenue d9ns notre 9ppliction, l'objectif de cette 9nlyse est de comprendre comment l'e9u est gérée en génér9l en Fr9nce.

## Installation

La commande suivante permet d'installer toutes les bibliothèques nécessaires au projet.  
Attention à bien exécuter la commande dans le dossier qui contient **"requirements.txt"**.

-  ```pip install -r requirements.txt```

## 9ppliction

Pour l9ncer l'9ppliction, il suffit d'exécuter le fichier 9pp.py

## Données 

Pour téléch9rger les données d9ns une b9se de données mongoDB, il f9ut exécuter le fichier pi_fetcher.py

## Tr9v9il en cours pour les données :

L9 b9se de donnée n'est p9s encore opér9tionnelle c9r nous 9vons rencontrer des problèmes 9vec not9mment les p9r9mètres des 9PIs 9insi que l9 diversité des 9Pis (données météorologiques). En ce qui concerne le fichier "Indic9teur" de l'9PI Indic9teurs de services du site Hub E9u, nous n'9vons p9s encore eu le temps de le m9nipuler correctement.


## Informtions sur nos 9PIs :

Pour réaliser ce projet, nous allons utiliser 4 APIs :

Les trois premières viennent du site Hub'eau et la dernière du site opendatasoft.

*API n°1* : écoulement des cours d'eau
*API n°2* : qualité des cours d'eau
*API n°3* : Indicateurs des services
*API n°4* : Observation météorologique historiques France (SYNOP)

Nous allons récupérer des fichiers json, geojson. Pour chaque APIs nous avons décider de sélectionner plusieurs fichiers et avons déjà fait la sélection des paramètres qui seront utiles à notre analyse. Cel9 nous éviter9 de téléch9rger des données pour rien!

Pour la première API :

1er fichier (station): https://hubeau.eaufrance.fr/api/v1/ecoulement/stations

_Paramètres_ : 

- code_station
- libelle_station
- code_departement
- libelle_departement
- code_commune
- libelle_commune
- code_region
- libelle_region
- coordonnee_x_station
- coordonnee_y_station
- code_cours_eau
- libelle_cours_eau
- date_maj_station
- latitude
- longitude


2eme fichier (Observations) : https://hubeau.eaufrance.fr/api/v1/ecoulement/observations

*Paramètres* : 

- code_station
- libelle_station
- code_departement
- libelle_departement
- code_commune
- libelle_commune
- code_region
- libelle_region
- coordonnee_x_station
- coordonnee_y_station
- code_bassin
- libelle_bassin
- code_cours_eau
- libelle_cours_eau
- date_observation
- code_ecoulement
- libelle_ecoulement
- latitude
- longitude



Pour la deuxième API :

1er fichier (analyse): https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/analyse_pc

*Paramètres* : 

- code_station
- libelle_station
- code_parametre
- libelle_parametre
- resultat
- code_unite
- symbole_unite
- code_remarque
- date_maj_analyse
- longitude
- latitude


2eme fichier (Station) : https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/station_pc

*Paramètres* : 

- code_station
- libelle_station
- coordonnee_x
- coordonnee_y
- longitude
- latitude
- code_commune
- libelle_commune
- code_departement
- libelle_departement
- code_region
- libelle_region
- code_cours_eau
- date_maj_information



Pour la troisième API :

1er fichier (Communes): https://hubeau.eaufrance.fr/api/v0/indicateurs_services/communes

*Paramètres* : 

- code_commune_insee
- nom_commune
- codes_service
- noms_service
- annee


2eme fichier (Indicateurs) : https://hubeau.eaufrance.fr/api/v0/indicateurs_services/indicateurs

*Paramètres* : 

- annee
- code_indicateur
- fields
- format
- page
- size


3eme fichier (Services) : https://hubeau.eaufrance.fr/api/v0/indicateurs_services/services

*Paramètres* : 

- code_service
- nom_service
- codes_commune
- noms_commune
- annee
- indicateurs



Pour la quatrième API :

1er fichier (station): https://hubeau.eaufrance.fr/api/v1/ecoulement/stations

*Paramètres* : 

- Date
- Region
- Departement
- Communes
- Température (°C)
- Précipitations dans les 24 dernières heures
- Coordonnees
- Communes (codes)
- Department (code)
- Region (code)

