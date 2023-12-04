


# def get_data(url: str) -> dict:
    
#     r = req.get(url=url)
#     r.raise_for_status()
#     return r.json().get('data', [])


# def get_water_quality_data_station() -> dict: #Qualité des cours d'eau / station_pc 
#     url = 'https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/donnees-synop-essentielles-omm/records'
#     params = {
#         'size': '20000',
#         'fields': 'libelle_ecoulement,code_station,libelle_station,code_departement,libelle_departement,code_commune,libelle_commune,code_region,libelle_region,coordonnee_x_station,coordonnee_y_station,code_bassin,libelle_bassin,code_cours_eau,libelle_cours_eau,date_observation,code_ecoulement,libelle_ecoulement,latitude,longitude',
#     }
#     return get_data(url, params).fillna('Données manquantes').value_counts().reset_index(name='Quantité')

# data2 = get_data('https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/donnees-synop-essentielles-omm/records')
# data2.to_csv('.toto.csv')



import requests as req
import pandas as pd

def get_data(url: str) -> pd.DataFrame:
    r = req.get(url=url)
    r.raise_for_status()
    
    # Convertir directement le JSON en DataFrame pandas
    data_df = pd.DataFrame(r.json().get('data', []))
    
    return data_df

# Appeler la fonction get_data pour obtenir le DataFrame
data_df = get_data('https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/donnees-synop-essentielles-omm/records')

# Enregistrer le DataFrame dans un fichier CSV
data_df.to_csv('.toto.csv', index=False)  # index=False pour ne pas inclure les indices dans le fichier CSV
