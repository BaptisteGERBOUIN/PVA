from datetime import datetime, date, timedelta

from pymongo import MongoClient
import geopandas as gpd
import pandas as pd

from datetime import date

from data.geojson_processing import GeographicArea

from json import loads

MONGODB_URI = 'mongodb://localhost'
DATABSE_NAME = 'pva_water_project'

MIN_DATE = date(2018, 1, 1)
MAX_DATE = date(2023, 12, 31)

def get_collection(collection_name: str):
    client = MongoClient(MONGODB_URI)
    db_water = client[DATABSE_NAME]
    return db_water[collection_name]

# query = {
#     'date_observation': {"$gte": '2023-12-26', "$lte": '2023-12-26'}
# }

# result_query = get_collection('ecoulements').find(query, {'_id': 0, 'date_observation': 1, 'code_ecoulement': 1})

# print(list(result_query))

query = {'date_observation': {'$gte': '2023-12-26', '$lte': '2023-12-26'}, 'code_region': {'$in': ['24']}, 'code_ecoulement': {'$exists': True, '$ne': None}}

query2 = {'date_observation': {'$gte': '2023-12-02', '$lte': '2023-12-26'}, 'code_region': {'$in': ['11', '24', '27', '28', '32', '44', '52', '53', '75', '76', '84', '93']}, 'code_ecoulement': {'$exists': True, '$ne': None}}

print(pd.DataFrame(list(get_collection('ecoulements').find(query2))))