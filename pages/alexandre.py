from datetime import datetime, date, timedelta

from dash import register_page, Input, Output, State, no_update, callback, ctx
from dash import html, dcc

from data.geojson_processing import FRANCE

import dash_mantine_components as dmc
from dash_iconify import DashIconify
import dash_leaflet as dl

register_page(__name__, name='Alexandre', title='Water A', order=3,
              category='Visualisation', icon='bi bi-moisture')

# --- HTML ---

def layout():
    return [
        dcc.Store(id='path_to_area', data=['France']),
        html.Div(
            [
                menu_map(),
                html.Div(
                    [
                        viewport_map()
                    ],
                    id='map_box'
                )
            ],
            id='map_container'
        )
    ]

def menu_map():
    return html.Div(
        [
            html.Span('Sélecteur de date', id='date_range_label'),
            html.Div(
                dmc.DateRangePicker(
                    id="date_range_picker",
                    minDate=date(2020, 8, 5),
                    value=[datetime.now().date(), datetime.now().date() + timedelta(days=5)],
                    clearable=False,
                ),
                id='map_date_picker_container'
            ),
            dmc.Switch(
                id='date_map_switch',
                offLabel=DashIconify(icon="bi:calendar-event", width=20),
                onLabel=DashIconify(icon="bi:calendar4-range", width=20),
                checked=True,
                size="lg",
            ),
        ],
        id='map_menu_container'
    )

def viewport_map():
    return dl.Map(
        [
            dl.TileLayer(), #add basemap (open-street-map)
            dl.GeoJSON(
                data=FRANCE.gdf_to_json(),
                zoomToBounds=True,
                hoverStyle={'color': '#666'},
                id='geojson_mapbox'
            ),
            dl.EasyButton(n_clicks=0, icon='bi bi-house-door', title='Voir France entière', id='btn_home_france'),
            dl.EasyButton(n_clicks=0, icon='bi bi-arrow-90deg-left', title='Revenir en arrière', id='btn_backward'),
            html.Div(
                [
                    html.Span('Indicateur :', id='seg_control_label'),
                    dmc.SegmentedControl(
                        data=['Qualité', 'Quantité'],
                        color='blue',
                        radius='md', 
                        id='seg_control'
                    )
                ]
            ),
        ],
        zoomSnap=0.2,
        zoomControl=False,
        scrollWheelZoom=False,
        dragging=False,
        attributionControl=False,
        doubleClickZoom=False,
        id='zoomable_map'
    )

# --- CALLBACKS ---

@callback(
    [
        Output('geojson_mapbox', 'data'),
        Output('path_to_area', 'data'),

        Output('geojson_mapbox', 'clickData'),
    ],
    [
        Input('geojson_mapbox', 'clickData'),
        Input('btn_home_france', 'n_clicks'),
        Input('btn_backward', 'n_clicks'),
    ],
    [
        State('path_to_area', 'data'),
    ])
def update_map_and_path_on_click(inClickData, inBtnHome, inBtnBack, statePathToArea):
    triggeredId = ctx.triggered_id

    geosjonData, pathData = [no_update] * 2
    geosjonClickData = None

    if triggeredId == 'btn_home_france':
        geosjonData, pathData = btn_home_map(inBtnHome)
    
    if triggeredId == 'btn_backward':
        geosjonData, pathData = btn_backward(inBtnBack, statePathToArea)

    if triggeredId == 'geojson_mapbox':
        geosjonData, pathData = go_in_area(inClickData, statePathToArea)

    return geosjonData, pathData, geosjonClickData

def btn_home_map(btn: int):
    """
    Manages the button that takes you back to the most zoomed-out area (France).
    """
    if not btn:
        return no_update, no_update
    return FRANCE.gdf_to_json(), ['France']

def btn_backward(btn: int, pathToArea: list):
    if not btn:
        return no_update, no_update
    if len(pathToArea[:-1]) > 1:
        return FRANCE.get_from_path(pathToArea[:-1]).gdf_to_json(), pathToArea[:-1]
    return FRANCE.gdf_to_json(), ['France']

def go_in_area(clickData: dict, pathToArea: list):
    """
    Manages a click event to navigate to a specific zone based on the click data 
    supplied and the current path to the zone.
    """
    if clickData is None:
        return no_update, no_update
    areaName = clickData['properties']['name']

    if pathToArea[-1] != areaName:
        pathToArea = pathToArea + [areaName]
        return FRANCE.get_from_path(pathToArea).gdf_to_json(), pathToArea
    return FRANCE.get_from_path(pathToArea).gdf_to_json(), no_update

@callback(
    [
        Output('map_date_picker_container', 'children'),
    ],
    [
        Input('date_map_switch', 'checked'),
    ])
def update_map_and_path_on_click(inChecked):
    if inChecked:
        return [
            dmc.DateRangePicker(
                id="date_range_picker",
                minDate=date(2020, 8, 5),
                value=[datetime.now().date(), datetime.now().date() + timedelta(days=5)],
                clearable=False,
            )
        ]
    return [
        dmc.DatePicker(
            id="date_range_picker",
            minDate=date(2020, 8, 5),
            value=[datetime.now().date()],
            clearable=False,
        )
    ]