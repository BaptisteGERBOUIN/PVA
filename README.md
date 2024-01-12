# Projet de visualisation analytique

Bienvenue dans notre application, l'objectif de cette analyse est de comprendre comment l'eau est gérée en France métropolitaine. C'est avec plaisir que nous vous invitons à explorer toutes les facettes de notre site ainsi qu'à faire vos analyses grâce aux nombreux graphiques et cartes que l'on vous propose.

## Installation

La commande suivante permet d'installer toutes les bibliothèques nécessaires au projet.

Attention à bien exécuter la commande dans le dossier qui contient **"requirements.txt"**.

- ```pip install -r requirements.txt```

## Données

Pour télécharger les données dans une base de données MongoDB, il faut exécuter le fichier **"download_data.py. Le temps de téléchargement est d'environ 30 min.

## Informations sur nos APIs :

Pour réaliser ce projet, nous allons utiliser 3 APIs via le site Hub'eau :

*API n°1* : écoulement des cours d'eau  : https://hubeau.eaufrance.fr/page/api-ecoulement
*API n°2* : qualité des cours d'eau  : https://hubeau.eaufrance.fr/page/api-qualite-cours-deau
*API n°3* : indicateurs des services  : https://hubeau.eaufrance.fr/page/api-indicateurs-services

Nous allons récupérer des fichiers json, geojson. Pour chaque APIs nous avons décidé de sélectionner plusieurs fichiers et avons déjà fait la sélection des paramètres qui seront utiles à notre analyse. Cela nous évitera de télécharger des données pour rien ! Pour voir quels paramètres nous avons utilisé, nous vous invitons à vous rendre au fichier "config.ini" qui est dans le dossier "download" du dossier "data".

## Application

Pour lancer l'application, il suffit d'exécuter le fichier python **"app.py"**.