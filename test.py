import pymongo
import json
import plotly.express as px
import pandas as pd
from random import randint

# client = pymongo.MongoClient('mongodb://localhost:27017/')

# waterDB = client['water']
# nitrate = waterDB['nitrate']

# nitrate.drop()
# rand = [random.gauss() for _ in range(10_000)]
# nitrate.insert_many([{'value': r} for r in rand])

# print(list(nitrate.aggregate([{'$group': {'_id': None, 'avgValue': {'$avg': '$value'}}}])))
# print(statistics.mean(rand))

# print(list(nitrate.find()))


with open('./data/departements_france.geojson', 'r') as file:
    js = json.load(file)
    # print(len(js['features']))
    # js['features'] = [i for i in js['features'] if i['properties']['code'] not in ['2A', '2B']]
    # print(len(js['features']))
    # file = open('./data/departements_france.geojson', 'w')
    # json.dump(js, file)

    df = pd.DataFrame({'code': [code['properties']['code'] for code in js['features']], 'value': [randint(0, 100) for _ in js['features']]})

    fig = px.choropleth_mapbox(df, geojson=js, featureidkey='properties.code', color="value", locations='code')
    fig.update_layout(mapbox_style="open-street-map")
    fig.show()