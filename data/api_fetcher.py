import requests as req
import pandas as pd

def get_data(url: str, params: dict[str, str]) -> pd.DataFrame:
    r = req.get(url=url, params=params)
    r.raise_for_status()

    # print(r.json()['count'])
    return pd.DataFrame.from_dict(r.json()['data'])

def get_water_flow_data() -> pd.DataFrame:
    url = 'https://hubeau.eaufrance.fr/api/v1/ecoulement/observations'
    params = {
        'size': '20000',
        'date_observation_min': '2023-06-01',
        'date_observation_max': '2023-06-30',
        'fields': 'libelle_ecoulement'
    }
    return get_data(url, params).fillna('Données manquantes')

# print(get_water_flow_data().value_counts().reset_index(name='count'))