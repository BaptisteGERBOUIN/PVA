from pymongo import MongoClient
import geopandas as gpd
import pandas as pd

from data.geojson_processing import GeographicArea

from json import loads

MONGODB_URI = 'mongodb://localhost'
DATABSE_NAME = 'pva_water_project'

def data_map(area: GeographicArea, date_range: list[str], collection_name: str) -> pd.DataFrame:
    client = MongoClient(MONGODB_URI)
    db_water = client[DATABSE_NAME]
    collection = db_water[collection_name]

    params_names = {'date': 'date_observation', 'resultat': 'code_ecoulement'}
    if collection_name != 'ecoulements':
        params_names = {'date': 'date_prelevement', 'resultat': 'resultat'}

    code_name = 'code_departement'
    if area.type == 'Pays':
        code_name = 'code_region'

    query = {
        params_names['date']: {"$gte": date_range[0], "$lte": date_range[1]},
        code_name: {'$in': area.gdf['code'].to_list()}
    }

    if collection_name == 'ecoulements':
        result_query = collection.find(query, {'_id': 0, params_names['resultat']: 1, code_name: 1})
        df_query = pd.DataFrame(list(result_query))

        df_code_visible = df_query[params_names['resultat']].isin(['1', '1a', '1f'])
        df_is_visible = (df_query[df_code_visible].groupby(code_name).count() / df_query.groupby(code_name).count() > 0.5)[params_names['resultat']]

        list_areas = []
        for code_visible, is_visible in [(df_code_visible, df_is_visible), (~df_code_visible, ~df_is_visible)]:
            df_area = df_query[code_visible].groupby(code_name).value_counts().reset_index(name='count')
            df_area = df_area.loc[df_area.groupby(code_name)['count'].idxmax()]
            list_areas.append(df_area.set_index(code_name)[is_visible][params_names['resultat']])
        
        gdf = area.gdf
        gdf['state'] = pd.concat(list_areas).reset_index(drop=True)
        return loads(gdf.to_json(drop_id=True))

    client.close()
    return