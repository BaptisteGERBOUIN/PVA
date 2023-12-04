from datetime import date

from dash import register_page, Input, Output, State, no_update, callback, ctx
from dash import html, dcc

from data.geojson_processing import FRANCE

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import dash_leaflet as dl

register_page(__name__, title='Water A')

# --- HTML ---

def layout():
    return [
        dcc.Store(id='path_to_area', data=['France']),
        html.Div(
            [
                menu_map(),
                html.Div(
                    [
                        breadcrumbs_map(),
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
            dbc.DropdownMenu(
                label='Type de la carte',
                children=[
                    dbc.DropdownMenuItem('Qualité'),
                    dbc.DropdownMenuItem('Quantité'),
                ],
                size='lg'
            ),
            dcc.DatePickerRange(
                id='my-date-picker-range',
                min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date(2017, 9, 19),
                initial_visible_month=date(2017, 7, 5),
                end_date=date(2017, 8, 25)
            ),
        ],
        id='map_menu_container'
    )

def breadcrumbs_map():
    return dmc.Breadcrumbs(
        id='path_display',
        separator='→',
        children=[
            html.Div('France', id='path_root', className='path_display'),
            html.Div(' - ', id='path_region', className='path_display'),
            html.Div(' - ', id='path_departement', className='path_display')
        ]
    )

def viewport_map():
    return dl.Map(
        [
            # dl.TileLayer(), #add basemap (open-street-map)
            dl.GeoJSON(
                data=FRANCE.gdf_to_json(),
                zoomToBounds=True,
                hoverStyle={'color': '#666'},
                id='geojson_mapbox'
            ),
            dl.EasyButton(n_clicks=0, icon='bi bi-house-door', title='Voir France entière', id='btn_home_france')
        ],
        zoomSnap=0.2,
        zoomControl=False,
        scrollWheelZoom=False,
        dragging=False,
        doubleClickZoom=False,
        id='zoomable_map'
    )

# --- CALLBACKS ---

@callback(
    [
        Output('geojson_mapbox', 'data'),
        Output('geojson_mapbox', 'clickData'),
        Output('path_to_area', 'data'),

        Output('path_root', 'children'),
        Output('path_region', 'children'),
        Output('path_departement', 'children'),
    ],
    [
        Input('geojson_mapbox', 'clickData'),
        Input('btn_home_france', 'n_clicks'),

        Input('path_root', 'n_clicks'),
        Input('path_region', 'n_clicks'),
        Input('path_departement', 'n_clicks'),
    ],
    [
        State('path_to_area', 'data'),
    ],
    prevent_initial_call=True)
def update_map_and_path_on_click(inClickData, inBtn, inPathRoot, inPathRegion, inPathDepart, statePathToArea):
    triggeredId = ctx.triggered_id

    geosjonClickData = None
    geosjonData, pathData = [no_update] * 2
    pathRoot, pathRegion, pathDepartement = [no_update] * 3

    if triggeredId == 'btn_home_france':
        geosjonData, pathData = btn_home_map(inBtn)

    if triggeredId == 'geojson_mapbox':
        geosjonData, pathData = go_in_area(inClickData, statePathToArea)

    if triggeredId in ['path_root', 'path_region', 'path_departement']:
        geosjonData, pathData = click_on_path_display(triggeredId, statePathToArea)

    pathRoot, pathRegion, pathDepartement = update_path_display(pathData)

    return geosjonData, geosjonClickData, pathData, pathRoot, pathRegion, pathDepartement

def btn_home_map(btn: int):
    """
    Manages the button that takes you back to the most zoomed-out area (France).
    """
    if not btn:
        return no_update, no_update
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

def click_on_path_display(triggeredId: str, pathToArea: list):
    '''
    Display the path by updating the map of the selected zone based on the trigger 
    identifier supplied and the current path to the zone.
    '''
    for indexPath, pathName in enumerate(['path_root', 'path_region', 'path_departement']):
        if triggeredId != pathName:
            continue
        if len(pathToArea) == indexPath + 1:
            return [no_update] * 2
        pathToArea = pathToArea[:indexPath + 1]
        break
    return FRANCE.get_from_path(pathToArea).gdf_to_json(), pathToArea

def update_path_display(pathData: list):
    """
    Update the path display information with a given path data.
    """
    if pathData == no_update:
        return [no_update] * 3
    return *pathData, *[' - ' for _ in range(3 - len(pathData))]