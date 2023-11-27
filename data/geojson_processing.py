from __future__ import annotations
from shapely.ops import unary_union
from numpy import interp
from copy import deepcopy

import pandas as pd
import geopandas as gpd

PATH_TO_DATA = './data/territoire_france/'
# https: //epsg.io/2154
CRS = 2154 # France

class GeographicArea:

    def get_zoom(bounds: dict[str, float]) -> float:
        return interp(
            x=min(bounds['maxx'] - bounds['minx'], bounds['maxy'] - bounds['miny']), 
            xp=[0.00025, 0.0007, 0.0014, 0.003, 0.006, 0.012, 0.024, 0.048, 0.096, 
                0.192, 0.3712, 0.768, 1.536, 3.072, 6.144, 11.8784, 23.7568, 47.5136, 
                98.304, 190.0544, 360.0], 
            fp=[20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0])

    def __init__(self, name: str, geometry: gpd.GeoSeries, gdf: gpd.GeoDataFrame=None, parent: str=None) -> None:
        self.__name = name
        self.__geometry = gpd.GeoSeries(geometry)
        self.__gdf = gdf

        self.__parent = parent
        self.__childs: dict[str, GeographicArea] = {}

        self.__zoom: float = GeographicArea.get_zoom(self.bounds)

    @property
    def zoom(self) -> float:
        return self.__zoom

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
        PATH_TO_DATA + 'regions_france.geojson')
    gdfDepartement: gpd.GeoDataFrame = gpd.read_file(
        PATH_TO_DATA + 'departements_france.geojson')
    dfTerritoire: pd.DataFrame = pd.read_csv(
        PATH_TO_DATA + 'territoire-francais.csv', 
        usecols=['Code', 'Département', 'Région'], 
        sep=';')
    
    France = GeographicArea(
        name='France',
        gdf=gdfRegion,
        geometry=gpd.GeoSeries(unary_union(gdfRegion['geometry']), crs=CRS))
    
    for _, rowR in gdfRegion.iterrows():
        filtered_gdf = gdfDepartement[gdfDepartement['nom'].isin(dfTerritoire[dfTerritoire['Région'] == rowR['nom']]['Département'])]
        Region = GeographicArea(
            name=rowR['nom'], 
            geometry=rowR['geometry'], 
            gdf=filtered_gdf, 
            parent='France')

        for _, rowD in filtered_gdf.iterrows():
            Departement = GeographicArea(
                name=rowD['nom'], 
                geometry=rowD['geometry'], 
                parent=rowR['nom'])
            Region.add_child(Departement)

        France.add_child(Region)
    return France

FRANCE = get_france()