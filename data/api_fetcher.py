import requests as req
import pandas as pd

def get_data(url: str, params: dict[str, str]) -> pd.DataFrame:
    r = req.get(url=url, params=params)
    r.raise_for_status()

    return pd.DataFrame.from_dict(r.json()['data'])

def get_water_flow_data() -> pd.DataFrame:
    url = 'https://hubeau.eaufrance.fr/api/v1/ecoulement/observations'
    params = {
        'size': '20000',
        'date_observation_min': '2023-06-01',
        'date_observation_max': '2023-06-30',
        'fields': 'libelle_ecoulement'
    }
    return get_data(url, params).fillna('Données manquantes').value_counts().reset_index(name='Quantité')

def get_nitrate_data() -> pd.DataFrame:
    url = 'https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/analyse_pc'
    params = {
        'code_station': '05073800',
        'libelle_parametre': 'Nitrates',
        'date_debut_prelevement': '2013-01-01',
        'code_qualification': '1',
        'size': '1000',
        'fields': 'code_station,libelle_station,code_parametre,libelle_parametre,date_prelevement,resultat,symbole_unite,code_remarque,mnemo_remarque,code_statut,mnemo_statut,code_qualification,libelle_qualification'
    }
    return get_data(url, params)