import geopandas as gpd
import pandas as pd

from json import loads

from data.geojson_processing import GeographicArea
from data.map_pratical_data import Api

from data.db_connexion import get_collection

def state_map_ecoulement(df: pd.DataFrame, api: Api):
    if len(df) == 0:
        return 'None'

    df['code_simplify'] = df[api.result_label].str.replace('1a', '1').replace('1f', '1')

    get_most_common = lambda df, col: df[col].agg(lambda x: pd.Series.mode(x)[0])

    encoded_result: pd.DataFrame = get_most_common(df, 'code_simplify')
    if encoded_result == '1':
        encoded_result: pd.DataFrame = get_most_common(df, api.result_label)
    return encoded_result

def geojson_map_ecoulement(df: pd.DataFrame, gdf: gpd.GeoDataFrame, api: Api, code_label: str):
    if len(df) == 0:
        gdf['encoded_result'] = 'None'
        return gdf

    gdf = gdf.set_index('code')
    df['code_simplify'] = df[api.result_label].str.replace('1a', '1').replace('1f', '1')

    get_most_common = lambda df, groupby, col: df.groupby(groupby)[col].agg(lambda x: pd.Series.mode(x)[0]).reset_index()

    df_encoded_result: pd.DataFrame = get_most_common(df, code_label, 'code_simplify')
    df_encoded_result_detail: pd.DataFrame = get_most_common(
        df[df[code_label].isin(df_encoded_result[df_encoded_result['code_simplify'] == '1'][code_label])],
        code_label,
        api.result_label
    )

    df_encoded_result = df_encoded_result.merge(df_encoded_result_detail, on=code_label).set_index(code_label)
    df_encoded_result['encoded_result'] = df_encoded_result.apply(
        lambda row: row['code_simplify'] if row['code_simplify'] != '1' else row[api.result_label], axis=1)

    gdf['encoded_result'] = df_encoded_result['encoded_result']
    gdf['encoded_result'] = gdf['encoded_result'].fillna('None')
    return gdf.reset_index()

def data_map_ecoulement(area: GeographicArea, date_range: list[str], api: Api) -> pd.DataFrame:
    collection = get_collection(collection_name=api.name)

    code_label = 'code_departement'
    if area.type == 'Pays':
        code_label = 'code_region'

    gdf = area.gdf

    query = {
        api.date_label: {"$gte": date_range[0], "$lte": date_range[1]},
        code_label: {'$in': gdf['code'].to_list()},
        api.result_label: {"$exists": True, "$ne": None}
    }

    result_query = collection.find(query, {'_id': 0, api.result_label: 1, code_label: 1})
    df_query = pd.DataFrame(list(result_query))
    
    df_geojson = geojson_map_ecoulement(df_query, gdf, api, code_label)
    df_geojson['encoded_result'] = df_geojson.apply(lambda row: api.get_old_keys_to_new()[row['encoded_result']], axis=1)
    nbr_obs = len(df_query)
    state = state_map_ecoulement(df_query, api)

    if len(df_query) == 0:
        empty_df = pd.DataFrame({'encoded_result': [api.get_classes()[-1]], 'count': [1]})
        return loads(df_geojson.to_json(drop_id=True)), nbr_obs, state, empty_df, empty_df
        
    df_pie_obs = df_query.value_counts(api.result_label).reset_index().rename(columns={api.result_label: 'encoded_result'})
    df_pie_obs['encoded_result'] = df_pie_obs.apply(lambda row: api.get_old_keys_to_new()[row['encoded_result']], axis=1)

    df_pie_area = df_geojson['encoded_result'].value_counts().reset_index()
    
    return loads(df_geojson.to_json(drop_id=True)), nbr_obs, state, df_pie_area, df_pie_obs

def state_map_qualite_rivieres(df: pd.DataFrame, gdf: gpd.GeoDataFrame, api: Api):
    df_encoded_result = df.agg(lambda x: pd.Series.mode(x)[0])
    return df_encoded_result['categories']

def geojson_map_qualite_rivieres(df: pd.DataFrame, gdf: gpd.GeoDataFrame, api: Api, parameter: str, code_label: str):
    gdf = gdf.set_index('code')
    df_encoded_result = df.groupby(code_label)['categories'].agg(lambda x: pd.Series.mode(x)[0])
    gdf['encoded_result'] = df_encoded_result
    gdf['encoded_result'] = gdf['encoded_result'].fillna(api.get_classes(parameter)[-1])

    return gdf.reset_index()

def data_map_qualite_rivieres(area: GeographicArea, date_range: list[str], api: Api, parameter: str) -> pd.DataFrame:
    collection = get_collection(collection_name=api.name)

    code_label = 'code_departement'
    if area.type == 'Pays':
        code_label = 'code_region'

    gdf = area.gdf

    query = {
        api.date_label: {"$gte": date_range[0], "$lte": date_range[1]},
        code_label: {'$in': gdf['code'].to_list()},
        api.result_label: {"$exists": True, "$ne": None},
        'libelle_parametre': {'$eq': parameter}
    }

    result_query = collection.find(query, {'_id': 0, api.result_label: 1, code_label: 1, 'symbole_unite': 1})
    df_query = pd.DataFrame(list(result_query))

    nbr_obs = len(df_query)
    if len(df_query) == 0:
        gdf['encoded_result'] = api.get_classes(parameter)[-1]
        df_geojson = gdf
        state = api.get_classes(parameter)[-1]
        empty_df = pd.DataFrame({'encoded_result': [api.get_classes(parameter)[-1]], 'count': [1]})
        return loads(df_geojson.to_json(drop_id=True)), nbr_obs, state, empty_df, empty_df
    
    df_query['categories'] = pd.cut(
        df_query[api.result_label],
        bins=[float('-inf')] + api.get_parameter_slice(parameter) + [float('inf')],
        labels=api.get_classes(parameter)[:-1],
        include_lowest=True
    )

    df_geojson = geojson_map_qualite_rivieres(df_query, gdf, api, parameter, code_label)
    state = state_map_qualite_rivieres(df_query, gdf, api)
    
    df_pie_obs = df_query.value_counts('categories').reset_index().rename(columns={'categories': 'encoded_result'})
    df_pie_area = df_geojson['encoded_result'].value_counts().reset_index()
    
    return loads(df_geojson.to_json(drop_id=True)), nbr_obs, state, df_pie_area, df_pie_obs