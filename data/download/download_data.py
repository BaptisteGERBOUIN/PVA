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
import pandas as pd
import geopandas as gpd

PATH_TO_DATA = './data/territoire_france/'

gdfRegion: gpd.GeoDataFrame = gpd.read_file(PATH_TO_DATA + 'regions_france.geojson'). \
    rename(columns={'nom': 'Région', 'code': 'code_region'})

dfTerritoire: pd.DataFrame = pd.read_csv(
        PATH_TO_DATA + 'territoire-francais.csv', 
        usecols=['Code', 'Département', 'Région'], 
        sep=';'). \
    rename(columns={'Code': 'code_departement'})

CODE = dfTerritoire.merge(gdfRegion, on='Région')[['code_region', 'code_departement']]

# Shared data among threads
DATA_LOCK = threading.Lock()

def api_ecoulements_to_database(url: str, params: dict[str, str], collection_name: str):
    client = MongoClient(MONGODB_URI)
    db_water = client[DATABSE_NAME]
    collection = db_water[collection_name]

    data = get_data_from_api(url=url, params=params, page_size=20_000, nbr_page=None)

    collection.insert_many(data)
    client.close()

def get_data_thread(url: str, params: dict[str, str], data: list):
    thread_data = get_data_from_api(url=url, params=params, page_size=20_000, nbr_page=1, disablePbar=True)

    code_region = CODE[CODE['code_departement'] == params['code_departement']]['code_region'].to_list()[0]
    for row in thread_data:
        row.update({'code_departement': params['code_departement'], 'code_region': code_region})
    
    with DATA_LOCK:
        data.extend(thread_data)

def create_new_download_thread(url: str, params: dict[str, str], data: list) -> threading.Thread:
    download_thread = threading.Thread(target=get_data_thread, args=(url, params, data))
    download_thread.start()
    return download_thread

def api_qualite_rivieres_to_database(url: str, params: dict[str, str], collection_name: str):
    from_year = int(params.get('date_debut_prelevement', '2000')[:4])
    to_year = int(params.get('date_fin_prelevement', str(date.today().year))[:4])

    for year in tqdm(range(from_year, to_year), unit='year', desc='Downloading by year'):
        for month in tqdm(range(1, 13), unit='month', leave=False, desc='Downloading by month'):
            thread_list: list[threading.Thread] = []

            start_date = date(year, month, 1)
            end_date = date(year, month, 1) + relativedelta(months=1) - relativedelta(days=1)

            data = []
            for code in CODE['code_departement'].to_list():
                thread_params = deepcopy(params)
                thread_params.update({'date_debut_prelevement': str(start_date), 'date_fin_prelevement': str(end_date)})
                thread_params.update({'code_departement': code})

                thread_list.append(create_new_download_thread(url, thread_params, data))

            for thread in tqdm(thread_list, leave=False, desc='Synchronization of all departmental downloads'):
                thread.join()

            client = MongoClient(MONGODB_URI)
            db_water = client[DATABSE_NAME]
            db_water[collection_name].insert_many(data)
            client.close()

def api_indicateurs_to_database(url: str, params: dict[str, str], collection_name: str):
    selected_columns = params.pop('fields').split(',')

    for code_indicateur in tqdm(params.get('code_indicateur', '').split(','), desc='Downloading by indicator', unit='indicator'):
        data = []
        for year in tqdm(range(2008, 2020), unit='year', desc='Downloading by year', leave=False):
            params.update({'annee': year, 'code_indicateur': code_indicateur})
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

def download_upload_to_database(collection_name: str, url: str, params: dict[str, str]):
    print(f'> API - {collection_name.capitalize()}')
    if collection_name == 'ecoulements':
        api_ecoulements_to_database(url=url, params=params, collection_name=collection_name)
    
    elif collection_name == 'qualite_rivieres':
        api_qualite_rivieres_to_database(url=url, params=params, collection_name=collection_name)
        
    elif collection_name == 'indicateurs_services':
        api_indicateurs_to_database(url=url, params=params, collection_name=collection_name)

# -- Run --

config = ConfigParser()
config.read('./data/download/config.ini')

base_url = config.get('BASE_URL', 'BASE_URL')

for api in [section for section in config.sections() if 'API' == section[:3]]:
    download_upload_to_database(
        url=base_url + config.get(api, 'API_URL'),
        params=loads(config.get(api, 'PARAMETERS')),
        collection_name=config.get(api, 'API_NAME'))