from __future__ import annotations
from shapely.ops import unary_union
from copy import deepcopy
from json import loads

import pandas as pd
import geopandas as gpd

PATH_TO_DATA = './data/territoire_france/'
# https: //epsg.io/2154
CRS = 2154 # France

class GeographicArea:

    def __init__(self, name: str, geometry: gpd.GeoSeries, gdf: gpd.GeoDataFrame, type_area: str, parent: str=None) -> None:
        self.__name = name
        self.__geometry = gpd.GeoSeries(geometry)
        self.__gdf = gdf.copy()
        self.__type = type_area

        self.__gdf['tooltip'] = '<b>' + self.__gdf['name'] + ' (' + self.__gdf['code'] + ')'

        self.__parent = parent
        self.__childs: dict[str, GeographicArea] = {}

    def add_child(self, child: GeographicArea) -> None:
        self.__childs[child.__name] = child

    @property
    def geometry(self) -> gpd.GeoSeries:
        return self.__geometry

    @property
    def bounds(self) -> dict[str, float]:
        return self.__geometry.bounds.iloc[0].to_dict()
    
    def getMaxBounds(self) -> list[tuple(float, float)]:
        bounds = self.bounds
        width = bounds['maxx'] - bounds['minx']
        height = bounds['maxy'] - bounds['miny']
        return [
            (bounds['miny'] - height * 0.05, bounds['minx'] - width * 0.05),
            (bounds['maxy'] + height * 0.05, bounds['maxx'] + width * 0.05)]
    
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def gdf(self) -> gpd.GeoDataFrame:
        return self.__gdf.copy()
    
    @property
    def type(self) -> str:
        return self.__type
    
    def gdf_to_json(self) -> dict:
        return loads(self.__gdf.to_json(drop_id=True))

    @property
    def parent(self) -> str:
        return self.__parent
    
    @property
    def childs(self) -> dict[str, GeographicArea]:
        return deepcopy(self.__childs)
    
    def get_from_path(self, path: list) -> GeographicArea:
        if not path or (len(path) == 1 and path[0] == self.__name):
            return self

        for path_index in range(1, len(path)):
            geoArea = self.__childs.get(path[path_index])
            if geoArea is not None:
                return geoArea.get_from_path(path[path_index:])
        return None
    
    def __get_string(self, space='  ') -> str:
        string = f'> {self.__name}\n{space}+ PARENT = {self.__parent}'
        if self.__childs:
            string += f'\n{space}- CHILDS :\n  {space}'
            string += f'\n  {space}'.join(child.__get_string(' ' * 4 + space) for child in self.__childs.values())
        return string

    def __str__(self) -> str:
        return self.__get_string()
    
def get_departement_name() -> gpd.GeoDataFrame :
    return gpd.read_file(PATH_TO_DATA + 'departements_france.geojson').rename(columns={'nom': 'name'})

def get_france() -> GeographicArea:
    gdfRegion: gpd.GeoDataFrame = gpd.read_file(
        PATH_TO_DATA + 'regions_france.geojson').rename(columns={'nom': 'name'})
    gdfDepartement: gpd.GeoDataFrame = gpd.read_file(
        PATH_TO_DATA + 'departements_france.geojson').rename(columns={'nom': 'name'})
    dfTerritoire: pd.DataFrame = pd.read_csv(
        PATH_TO_DATA + 'territoire-francais.csv', 
        usecols=['Code', 'Département', 'Région'], 
        sep=';')
    
    France = GeographicArea(
        name='France Métropolitaine (hors Corse)',
        gdf=gdfRegion,
        geometry=gpd.GeoSeries(unary_union(gdfRegion['geometry']), crs=CRS),
        type_area='Pays')
    
    for _, rowR in gdfRegion.iterrows():
        filtered_gdf = gdfDepartement[gdfDepartement['name'].isin(
                dfTerritoire[dfTerritoire['Région'] == rowR['name']]['Département'])]
        Region = GeographicArea(
            name=rowR['name'], 
            geometry=rowR['geometry'], 
            gdf=filtered_gdf.reset_index(drop=True),
            type_area='Région', 
            parent='France')

        for _, rowD in filtered_gdf.iterrows():
            Departement = GeographicArea(
                name=rowD['name'], 
                geometry=rowD['geometry'],
                gdf=gpd.GeoDataFrame(rowD.to_frame().T).reset_index(drop=True),
                type_area='Département',
                parent=rowR['name'])
            Region.add_child(Departement)

        France.add_child(Region)
    return France

FRANCE = get_france()