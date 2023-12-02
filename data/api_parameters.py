
BASE_URL = 'https://hubeau.eaufrance.fr/api/'
SIZE = 20_000

#Parametres pour l'API ecoulement d'eau

flowWaterObservation = {
    'url' : BASE_URL + 'v1/ecoulement/observations',      
    'parameters' : {
        'size' : SIZE, 
        'fields' : 'code_station,libelle_station,code_departement,libelle_departement,code_commune,libelle_commune,code_region,libelle_region,coordonnee_x_station,coordonnee_y_station,code_bassin,libelle_bassin,code_cours_eau,libelle_cours_eau,date_observation,code_ecoulement,libelle_ecoulement,latitude,longitude'
        } 
}


flowWaterStation = {
    'url' : BASE_URL + 'v1/ecoulement/stations',
    'parameters' : {
        'size' : SIZE,
        'fields' : 'code_station,libelle_station,code_departement,libelle_departement,code_commune,libelle_commune,code_region,libelle_region,coordonnee_x_station,coordonnee_y_station,code_cours_eau,libelle_cours_eau,date_maj_station,latitude,longitude'
        } 
}



#Parametres pour l'API qualité des eaux

qualityStation = {
    'url' : BASE_URL + 'v2/qualite_rivieres/station_pc',
    'parameters' : {
        'size' : SIZE,
        'fields': 'code_station,libelle_station,coordonnee_x,coordonnee_y,longitude,latitude,code_commune,libelle_commune,code_departement,libelle_departement,code_region,libelle_region,code_cours_eau,date_maj_information'
        }
}

qualityAnalyse = {
    'url' : BASE_URL + 'v2/qualite_rivieres/analyse_pc',
    'parameters' : {
        'size' : SIZE,
        'fields' : 'code_station,libelle_station,code_parametre,libelle_parametre,resultat,code_unite,symbole_unite,code_remarque,date_maj_analyse,longitude,latitude'
        }
}


#Parametres pour l'API Indicateurs de services


serviceIndicatorCommunes = {
    'url' : BASE_URL + 'v0/indicateurs_services/communes',
    'parameters' : {
        'size' : 5_000,
        'fields' : 'code_commune_insee,nom_commune,codes_service,noms_service,annee'
        }
}


serviceIndicatorIndicateurs = {
    'url' : BASE_URL + 'v0/indicateurs_services/indicateurs?code_indicateur=D102.0',
    'parameters' : {
        'size' : SIZE,
        'fields' : 'code_service,nom_service,codes_commune,noms_commune,annee,indicateur'
        }
}


serviceIndicatorServices = {
    'url' : BASE_URL + 'v0/indicateurs_services/services',
    'parameters' : {
        'size' : SIZE,
        'fields' : 'code_service,nom_service,codes_commune,noms_commune,annee,indicateurs'
        }
}


#Parametres pour l'API Météorologique

# serviceIndicatorServices = {
#     'url' : ,
#     'parameters' : {
#         'size' : SIZE,
#         'fields' : 'Date,region,departement,communes,Température(°C),Précipitations dans les 24 dernières heures,Coordonnees,communes(codes),department (code),region (code)'
#         }
# }