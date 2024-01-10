import pandas as pd
import geopandas as gpd
import threading
from pymongo import MongoClient
from configparser import ConfigParser

from copy import deepcopy
from json import loads
from tqdm.auto import tqdm
from datetime import date
from dateutil.relativedelta import relativedelta

from api_downloader import get_data_from_api

# MongoDB connection details
MONGODB_URI = 'mongodb://localhost'
DATABSE_NAME = 'pva_water_project'

# List of all French department codes
CODE_DEPARTEMENTS = gpd.read_file('./data/territoire_france/departements_france.geojson')['code'].to_list()

# Shared data among threads
DATA_LOCK = threading.Lock()

def get_data_thread(url: str, params: dict[str, str], data: list):
    thread_data = get_data_from_api(url, params, 20_000, 1, disablePbar=True)
    for row in thread_data:
        row.update({'code_departement': params['code_departement']})
    
    with DATA_LOCK:
        data.extend(thread_data)

def create_new_download_thread(url: str, params: dict[str, str], data: list) -> threading.Thread:
    download_thread = threading.Thread(target=get_data_thread, args=(url, params, data))
    download_thread.start()
    return download_thread

def download_by_months_departements_to_database(url: str, params: dict[str, str], collection_name: str, name_field_date: list[str]):
    from_year = int(params[name_field_date[0]][:4])
    to_year = int(params[name_field_date[1]][:4])

    for year in tqdm(range(from_year, to_year), unit='year', desc='Downloading by year'):
        for month in tqdm(range(1, 13), unit='month', leave=False, desc='Downloading by month'):
            thread_list: list[threading.Thread] = []

            start_date = date(year, month, 1)
            end_date = date(year, month, 1) + relativedelta(months=1) - relativedelta(days=1)

            data = []
            for i, code in enumerate(CODE_DEPARTEMENTS):
                thread_params = deepcopy(params)
                thread_params.update({name_field_date[0]: str(start_date), name_field_date[1]: str(end_date)})
                thread_params.update({'code_departement': code})

                thread_list.append(create_new_download_thread(url, thread_params, data))

            for thread in tqdm(thread_list, leave=False, desc='Synchronization of all departmental downloads'):
                thread.join()

            client = MongoClient(MONGODB_URI)
            db_water = client[DATABSE_NAME]
            db_water[collection_name].insert_many(data)
            client.close()

def download_api_indicateur_by_years_to_database(url: str, params: dict[str, str], collection_name: str):
    selected_columns = params.pop('fields').split(',')

    data = []
    for year in tqdm(range(2000, 2023), unit='year', desc='Downloading by year'):
        params.update({'annee': year})
        data.extend(get_data_from_api(url, params, 20_000, 1, disablePbar=True))

    data = pd.DataFrame(data)[selected_columns]
    data['code_departement'] = data['codes_commune'].map(lambda row: int(row[0][:2]) if row and row[0][:2].isnumeric() else pd.NA)
    data['code_departement'] = data['code_departement'].dropna()

    data = data.drop(columns=['codes_commune'])
    data['code_indicateur'] = params['code_indicateur']

    client = MongoClient(MONGODB_URI)
    db_water = client[DATABSE_NAME]
    collection = db_water[collection_name]

    collection.insert_many(data.to_dict('records'))
    client.close()

def download_upload_to_database(name: str, url: str, params: dict[str, str], name_date_param: dict[str, str]):
    print(f'> API - {name.capitalize()}')
    if name == 'ecoulements':
        client = MongoClient(MONGODB_URI)
        db_water = client[DATABSE_NAME]
        collection = db_water[name]

        data = get_data_from_api(url=url, params=params, page_size=20_000, nbr_page=None)

        collection.insert_many(data)
        client.close()
    
    elif name == 'qualite_rivieres':
        download_by_months_departements_to_database(
            url=url,
            params=params,
            collection_name=name,
            name_field_date=list(name_date_param.values()))
        
    elif name == 'indicateurs':
        download_api_indicateur_by_years_to_database(
            url=url,
            params=params,
            collection_name=name
        )

# -- Run --

config = ConfigParser()
config.read('./data/download/config.ini')

base_url = config.get('BASE_URL', 'BASE_URL')

download_upload_to_database(
    name='qualite_rivieres',
    url=base_url + config.get('API_QUALITE_RIVIERES', 'API_URL'),
    params=loads(config.get('API_QUALITE_RIVIERES', 'PARAMETERS')),
    name_date_param=loads(config.get('API_QUALITE_RIVIERES', 'NAME_DATE_PARAMETER'))
)

# download_upload_to_database(
#     name='ecoulements',
#     url=base_url + config.get('API_ECOULEMENTS', 'API_URL'),
#     params=loads(config.get('API_ECOULEMENTS', 'PARAMETERS')),
#     name_date_param=loads(config.get('API_ECOULEMENTS', 'NAME_DATE_PARAMETER'))
# )

# download_upload_to_database(
#     name='indicateurs',
#     url=base_url + config.get('API_INDICATEUR_P104.3', 'API_URL'),
#     params=loads(config.get('API_INDICATEUR_P104.3', 'PARAMETERS')),
#     name_date_param=None
# )