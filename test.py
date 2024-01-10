import requests
import pandas as pd
import geopandas as gpd
from tqdm.auto import tqdm
from json import loads
from math import ceil

def scale_unit(value: int | str, unit: str, precision: int=2, divisor: int=1000) -> str:
    value = int(value)
    for threshold, modifier in zip(range(1, 5), ['', 'k', 'M', 'G']):
        if value < divisor**threshold:
            return str(round(value / divisor**(threshold - 1), precision)) + modifier + unit
    return str(round(value / divisor**5, precision)) + 'T' + unit

def get_data(url: str, params: dict[str, str], page_size: int=5_000, nbr_page: int=3, leavePbar: bool=True, disablePbar: bool=False) -> list[dict[str, ]]:
    if nbr_page is None or nbr_page <= 0:
        head_params = {**params, 'size': 1, 'fields': params['fields'].split(',')[0]}

        response = requests.get(url, params=head_params)
        response.raise_for_status()
        nbr_rows_to_download = response.json().get('count', 0)
        nbr_page = ceil(nbr_rows_to_download / page_size)
    else:
        nbr_rows_to_download = page_size * nbr_page

    final_json_data = list()
    total_downloaded = 0
    api_pbar = tqdm(total=nbr_rows_to_download, desc=f'API: {url}', unit='row', unit_scale=True, leave=leavePbar, disable=disablePbar)
    for current_page in range(1, nbr_page + 1):
        params.update({'page': current_page, 'size': page_size})
        response = requests.get(url, params=params, stream=True)
        response.raise_for_status()

        with tqdm(desc=f'Downloading page {current_page}', unit='B', unit_scale=True, miniters=1, leave=False, disable=disablePbar) as sub_pbar:
            json_data = ''
            for data in response.iter_content(1000, decode_unicode=True):
                sub_pbar.update(len(data))
                api_pbar.update(data.count('{'))
                json_data += data
            api_pbar.update(-1)

            total_downloaded += sub_pbar.format_dict['n']
            api_pbar.set_description(f'API: {url} [Total downloaded: {scale_unit(total_downloaded, unit='B')}]')

        final_json_data.extend(loads(json_data).get('data', []))
    return final_json_data

params = {
    'fields': 'code_station,libelle_station,code_parametre,libelle_parametre,resultat,code_unite,symbole_unite,code_remarque,date_maj_analyse,longitude, latitude',
    'code_parametre': '1098,1099,1301,1302,1303,1304,1305,1309,1330,1340,1418,1419,1421,1422,1552',
    'date_debut_prelevement': '2018-01-01',
    'date_fin_prelevement': '2018-12-31',
    'code_departement': '33'
}

# data = get_data(
#     url='https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/analyse_pc',
#     params=params,
#     page_size=20_000,
#     nbr_page=None
# )

import datetime
from dateutil.relativedelta import relativedelta

# counter = []
# for year in tqdm(range(2018, 2024)):
#     for month in tqdm(range(1, 13), leave=False):

#         start_date = datetime.date(year, month, 1)
#         end_date = datetime.date(year, month, 1) + relativedelta(months=1) - relativedelta(days=1)

#         for code in tqdm(gpd.read_file('./data/territoire_france/departements_france.geojson')['code'].to_list(), leave=False):
#             params = {
#                 'fields': 'code_station,libelle_station,code_parametre,libelle_parametre,resultat,code_unite,symbole_unite,date_prelevement,heure_prelevement,longitude,latitude',
#                 'code_parametre': '1098,1099,1301,1302,1303,1304,1305,1309,1330,1340,1418,1419,1421,1422,1552',
#                 'date_debut_prelevement': str(start_date),
#                 'date_fin_prelevement': str(end_date),
#                 'code_departement': code,
#                 'size': 10_000
#             }
#             if requests.get('https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/analyse_pc', params=params).json()['count'] > 20_000:
#                 counter.append([f'{year}-{month:>02}', code])
# print(len(counter))
# print(counter)


import threading
import requests

def download_month(code, start_date, end_date):
    params = {
        'fields': 'code_station,libelle_station,code_parametre,libelle_parametre,resultat,code_unite,symbole_unite,date_prelevement,heure_prelevement,longitude,latitude',
        'code_parametre': '1098,1099,1301,1302,1303,1304,1305,1309,1330,1340,1418,1419,1421,1422,1552',
        'date_debut_prelevement': str(start_date),
        'date_fin_prelevement': str(end_date),
        'code_departement': code
    }

    get_data(
        url='https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/analyse_pc',
        params=params,
        page_size=20_000,
        nbr_page=1,
        disablePbar=True
    )

def create_new_download_thread(code, start_date, end_date) -> threading.Thread:
    download_thread = threading.Thread(target=download_month, args=(code, start_date, end_date))
    download_thread.start()
    return download_thread

codes_departements = gpd.read_file('./data/territoire_france/departements_france.geojson')['code'].to_list()
for year in tqdm(range(2018, 2024), unit='year'):
    for month in tqdm(range(1, 13), unit='month', leave=False):
        thread_list: list[threading.Thread] = []

        start_date = datetime.date(year, month, 1)
        end_date = datetime.date(year, month, 1) + relativedelta(months=1) - relativedelta(days=1)

        for code in codes_departements:
            thread_list.append(create_new_download_thread(code, start_date, end_date))

        for thread in tqdm(thread_list, leave=False):
            thread.join()