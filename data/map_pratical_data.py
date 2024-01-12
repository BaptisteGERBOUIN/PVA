from __future__ import annotations
from datetime import timedelta, datetime

from data.db_connexion import get_collection
from data.geojson_processing import GeographicArea, get_france

class Map_infos:
    def __init__(self, list_api: list[Api]) -> None:
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
    def __init__(self, api_name: str, label_params: dict[str, str], parameters: dict[str, dict[str, list | dict]]) -> None:
        self.__name = api_name

        self.__date_label = label_params['date']
        self.__result_label = label_params['result']

        self.__parameters = parameters

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
    
    def get_parameter_slice(self, parameter: str='default'):
        return self.__parameters.get(parameter, [])[0]

    def get_hideout(self, parameter: str='default'):
        return {
            'colorscale': list(self.__parameters[parameter][1].values()),
            'classes': list(self.__parameters[parameter][1].keys()),
            'colorProp': 'encoded_result',
            'style': {'fillOpacity': 1.0, 'color': 'lightgray', 'weight': 2}
        }
    
    def get_colorscale(self, parameter: str='default'):
        return self.__parameters[parameter][1]
    
    def get_classes(self, parameter: str='default'):
        return list(self.__parameters[parameter][1].keys())
    
    def get_old_keys_to_new(self, parameter: str='default'):
        return self.__parameters[parameter][2]

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
    def parameters_names(self):
        return list(self.__parameters.keys())

def create_API(name: str) -> Api:
    api = None
    if name == 'ecoulements':
        parameters = {
            'default': [
                [],
                {
                    'très visible': '#008000',
                    'visible': '#00cc33',
                    'visible faible': '#afcc00',
                    'non visible': '#d6e600',
                    'assec': '#e69b00',
                    'impossible': '#e64300',
                    'sans données': 'gray'
                },
                {'1': 'très visible', '1a': 'visible', '1f': 'visible faible', '2': 'non visible', '3': 'assec', '4': 'impossible', 'None': 'sans données'}
            ]
        }
        api = Api(name, {'date': 'date_observation', 'result': 'code_ecoulement'}, parameters)

    elif name == 'qualite_rivieres':
        parameters = {
            'Potentiel en Hydrogène (pH)': [
                [6, 7, 8, 9], 
                {
                    'pH (très bas)': 'red',
                    'pH (bas)': '#ff474c',
                    'normal': 'green',
                    'pH (haut)': '#ADD8E6',
                    'pH (très haut)': 'blue',
                    'sans données': 'gray'
                }
            ],
            'Conductivité à 20°C': [
                [50, 1500],
                {'anormal (bas)': 'red', 'normal': 'green', 'anormal (haut)': 'blue', 'sans données': 'gray'}
            ],
            'Nitrates': [
                [0.21, 3.0, 10.0],
                {
                    'influence (aucune)': 'green',
                    'influence (possible)': 'blue',
                    'influence (nette)': 'orange',
                    'influence (anormale)': 'red',
                    'sans données': 'gray'}
            ]
        }
        list_parameters = list(get_collection('qualite_rivieres').distinct('libelle_parametre'))
        api = Api(name, {'date': 'date_prelevement', 'result': 'resultat'}, parameters)

    return api

APIS_INFO = Map_infos(
    list_api=[
        create_API('ecoulements'),
        create_API('qualite_rivieres')
    ]
)