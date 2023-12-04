# Projet de visualisation analytique

Bienvenue dans notre appliction, l'objectif de cette anlyse est de comprendre comment l'eau est gérée en général en France.

## Installation

La commande suivante permet d'installer toutes les bibliothèques nécessaires au projet.  
Attention à bien exécuter la commande dans le dossier qui contient **"requirements.txt"**.

-  ```pip install -r requirements.txt```

## Application

Pour lancer l'appliction, il suffit d'exécuter le fichier python **"app.py"**.

## Données 

Pour télécharger les données dans une base de données mongoDB, il faut exécuter le fichier **"pi_fetcher.py"**.

## Travail en cours pour les données :

La base de donnée n'est pas encore opérationnelle car nous avons rencontrer des problèmes avec notamment les paramètres des APIs ainsi que la diversité des APis (données météorologiques). En ce qui concerne le fichier "Indicateur" de l'API Indicateurs de services du site Hub Eau, nous n'avons pas encore eu le temps de le manipuler correctement.

## Informtions sur nos APIs :

Pour réaliser ce projet, nous allons utiliser 4 APIs :

Les trois premières viennent du site Hub'eau et la dernière du site opendatasoft.

*API n°1* : écoulement des cours d'eau  
*API n°2* : qualité des cours d'eau  
*API n°3* : indicateurs des services  
*API n°4* : observation météorologique historiques France (SYNOP)

Nous allons récupérer des fichiers json, geojson. Pour chaque APIs nous avons décider de sélectionner plusieurs fichiers et avons déjà fait la sélection des paramètres qui seront utiles à notre analyse. Cela nous évitera de télécharger des données pour rien!

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
