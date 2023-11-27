import pymongo
import json
import plotly.express as px
import pandas as pd
from random import randint
import numpy as np
import geopandas as gpd

# client = pymongo.MongoClient('mongodb: //localhost: 27017/')

# waterDB = client['water']
# nitrate = waterDB['nitrate']

# nitrate.drop()
# rand = [random.gauss() for _ in range(10_000)]
# nitrate.insert_many([{'value': r} for r in rand])

# print(list(nitrate.aggregate([{'$group': {'_id': None, 'avgValue': {'$avg': '$value'}}}])))
# print(statistics.mean(rand))

# print(list(nitrate.find()))

france = gpd.read_file('./data/territoire_france/departements_france.geojson')
from shapely.ops import unary_union

# https: //epsg.io/2154
a = gpd.GeoSeries(unary_union(france['geometry']), crs=2154)

# https: //wiki.openstreetmap.org/wiki/Zoom_levels
bounds = a.bounds.iloc[0].to_dict()
zoom = np.interp(
    x=min(bounds['maxx'] - bounds['minx'], bounds['maxy'] - bounds['miny']), 
    xp=[0.00025, 0.0007, 0.0014, 0.003, 0.006, 0.012, 0.024, 0.048, 0.096, 0.192, 0.3712, 0.768, 1.536, 3.072, 6.144, 11.8784, 23.7568, 47.5136, 98.304, 190.0544, 360.0], 
    fp=[20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0])

print(zoom)

fig = px.choropleth_mapbox(
    data_frame=france, 
    geojson=france.geometry, 
    # featureidkey='properties.code', 
    locations=france.index, 
    center={'lon': 2.45163, 'lat': 46.62401 + 0.25}, 
    mapbox_style='open-street-map', 
    zoom=zoom, 
    opacity=0.94
)

fig.update_layout(
    showlegend=False, 
    margin={'r': 0, 't': 0, 'l': 0, 'b': 0}, 
    # mapbox_bounds={'west': bounds['minx'], 'east': bounds['maxx'], 'south': bounds['miny'], 'north': bounds['maxy']}
)
fig.show()