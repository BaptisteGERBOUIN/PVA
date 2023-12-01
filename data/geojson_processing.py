from __future__ import annotations
from shapely.ops import unary_union
from copy import deepcopy

import pandas as pd
import geopandas as gpd

PATH_TO_DATA = './data/territoire_france/'
# https: //epsg.io/2154
CRS = 2154 # France

class GeographicArea:

    def __init__(self, name: str, geometry: gpd.GeoSeries, gdf: gpd.GeoDataFrame, parent: str=None) -> None:
        self.__name = name
        self.__geometry = gpd.GeoSeries(geometry)
        self.__gdf = gdf

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
    
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def gdf(self) -> gpd.GeoDataFrame:
        return self.__gdf

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
        name='France',
        gdf=gdfRegion.set_index('code'),
        geometry=gpd.GeoSeries(unary_union(gdfRegion['geometry']), crs=CRS))
    
    for _, rowR in gdfRegion.iterrows():
        filtered_gdf = gdfDepartement[gdfDepartement['name'].isin(
                dfTerritoire[dfTerritoire['Région'] == rowR['name']]['Département'])]
        Region = GeographicArea(
            name=rowR['name'], 
            geometry=rowR['geometry'], 
            gdf=filtered_gdf.set_index('code'), 
            parent='France')

        for _, rowD in filtered_gdf.iterrows():
            Departement = GeographicArea(
                name=rowD['name'], 
                geometry=rowD['geometry'],
                gdf=gpd.GeoDataFrame(rowD.to_frame().T.set_index('code')), 
                parent=rowR['name'])
            Region.add_child(Departement)

        France.add_child(Region)
    return France

FRANCE = get_france()