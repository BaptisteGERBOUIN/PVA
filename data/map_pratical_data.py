from __future__ import annotations
from datetime import timedelta, datetime

from data.db_connexion import get_collection
from data.geojson_processing import GeographicArea, get_france

from plotly.express.colors import qualitative

class Map_infos:
    def __init__(self, area: GeographicArea, list_api: list[Api]) -> None:
        self.__dict_api = {}

        for api in list_api:
            self.add_api(api)
    
    def add_api(self, api: Api):
        self.__dict_api[api.name] = api
    
    def get_api(self, api_name: str) -> Api:
        return self.__dict_api.get(api_name, None)
    
    @property
    def area(self):
        return self.__area

class Api:
    def __init__(self, api_name: str, label_params: dict[str, str], colorscale: dict[str, str]) -> None:
        self.__name = api_name

        self.__date_label = label_params['date']
        self.__result_label = label_params['result']

        self.__colorscale = colorscale

        self.__hideout = {
            'colorscale': list(colorscale.values()),
            'classes': list(colorscale.keys()),
            'colorProp': 'encoded_result',
            'style': {'fillOpacity': 1.0, 'color': 'white', 'weight': 2}
        }

        self.get_date_info()

    def get_date_info(self):
        collection = get_collection(self.__name)

        str_to_date = lambda date: datetime.strptime(date, '%Y-%m-%d')
        min_date = str_to_date(list(collection.find().sort({self.__date_label: 1}).limit(1))[0][self.__date_label])
        max_date = str_to_date(list(collection.find().sort({self.__date_label: -1}).limit(1))[0][self.__date_label])

        available_date = list(collection.find({}, {'_id': 0, self.__date_label: 1}).distinct(self.__date_label))
        
        disabled_dates = []
        current_date = min_date
        while current_date != max_date:
            if current_date.date().isoformat() not in available_date:
                disabled_dates.append(current_date.date().isoformat())
            current_date = current_date + timedelta(days=1)

        self.__min_date = min_date.date().isoformat()
        self.__max_date = max_date.date().isoformat()
        self.__disabled_dates = disabled_dates

    def get_color(self, key: str):
        return self.__colorscale.get(key, None)

    @property
    def get_colors(self):
        return self.__colorscale

    @property
    def min_date(self):
        return self.__min_date
    
    @property
    def max_date(self):
        return self.__max_date
    
    @property
    def disabled_dates(self):
        return self.__disabled_dates

    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def date_label(self) -> str:
        return self.__date_label
    
    @property
    def result_label(self) -> str:
        return self.__result_label
    
    @property
    def hideout(self):
        return self.__hideout

def create_API(name: str) -> Api:
    api = None
    if name == 'ecoulements':
        colorscale = {'1': '#008000', '1a': '#00cc33', '1f': '#afcc00', '2': '#d6e600', '3': '#e69b00', '4': '#e64300', 'None': 'gray'}
        api = Api(name, {'date': 'date_observation', 'result': 'code_ecoulement'}, colorscale)

    elif name == 'qualite_rivieres':
        api = Api(name, {'date': 'date_prelevement', 'result': 'resultat'}, {})

    return api

APIS_INFO = Map_infos(
    area=get_france(),
    list_api=[
        create_API('ecoulements'),
        create_API('qualite_rivieres')
    ]
)