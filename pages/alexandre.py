from dash import register_page, Input, Output, State, no_update, callback, ctx
from dash_extensions.javascript import assign
from dash_iconify import DashIconify
from dash import html, dcc

import dash_mantine_components as dmc
import dash_leaflet as dl
import dash_leaflet.express as dlx

from data.map_pratical_data import APIS_INFO
from data.geojson_processing import FRANCE

import data.db_requests as db_requests
import view.figure as figure

register_page(__name__, name='Alexandre', title='Water A', order=3,
              category='Visualisation', icon='bi bi-moisture')
# --- HTML ---

def layout():
    return [
        dcc.Store(id='path_to_area', data=[FRANCE.name]),
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
        ),
        html.Div(
            [
                infos()
            ],
            id='infos_container'
        )
    ]

def menu_map():
    return html.Div(
        html.Div(
            [
                html.Div(
                    dmc.DateRangePicker(
                        id="date_range_picker",
                        minDate=APIS_INFO.get_api('ecoulements').min_date,
                        maxDate=APIS_INFO.get_api('ecoulements').max_date,
                        value=[APIS_INFO.get_api('ecoulements').max_date, APIS_INFO.get_api('ecoulements').max_date],
                        disabledDates=APIS_INFO.get_api('ecoulements').disabled_dates,
                        allowSingleDateInRange=True,
                        clearable=False,
                    ),
                    id='map_date_picker_container'
                ),
            ],
            id='map_menu_container',
        ),
        id='map_menu_decor'
    )

def viewport_map():
    style_handle = assign("""
        function(feature, context) {
            const {classes, colorscale, style, colorProp} = context.hideout;  // get props from hideout
            const value = feature.properties[colorProp];  // get value the determines the color
            for (let i = 0; i < classes.length; ++i) {
                if (value == classes[i]) {
                    style.fillColor = colorscale[i];  // set the fill color according to the class
                }
            }
            return style;
        }
    """)
    return dl.Map(
        [
            # dl.TileLayer(), #add basemap (open-street-map)
            dl.GeoJSON(
                data=db_requests.data_map(
                    area=FRANCE,
                    date_range=[APIS_INFO.get_api('ecoulements').max_date, APIS_INFO.get_api('ecoulements').max_date],
                    api=APIS_INFO.get_api('ecoulements')
                )[0],
                style=style_handle,
                zoomToBounds=True,
                hoverStyle={'color': '#666'},
                id='geojson_mapbox',
                hideout=APIS_INFO.get_api('ecoulements').hideout
            ),
            dlx.categorical_colorbar(
                categories=APIS_INFO.get_api('ecoulements').hideout['classes'],
                colorscale=APIS_INFO.get_api('ecoulements').hideout['colorscale'],
                width=300,
                height=30,
                position="bottomleft"
            ),
            dl.EasyButton(n_clicks=0, icon='bi bi-house-door', title=f'Voir {FRANCE.name} entière', id='btn_home_france'),
            dl.EasyButton(n_clicks=0, icon='bi bi-arrow-90deg-left', title='Revenir en arrière', id='btn_backward'),
            dmc.SegmentedControl(
                data=['Qualité', 'Quantité'],
                color='blue',
                radius='md', 
                id='seg_control'
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

def infos():
    _, nbr_obs, state, dfPieArea, figPieObs = db_requests.data_map(
        area=FRANCE,
        date_range=[APIS_INFO.get_api('ecoulements').max_date, APIS_INFO.get_api('ecoulements').max_date],
        api=APIS_INFO.get_api('ecoulements')
    )
    return html.Div(
        [
            html.Div(
                [
                    html.Span(FRANCE.name, id='name_area')
                ],
                className='box_title_name'
            ),
            html.Div(
                [
                    DashIconify(icon="bi:clipboard-data", width=20),
                    html.Span('Nombre d\'observation :', id='text_nbr_observation'),
                    html.Span(nbr_obs, id='value_nbr_observation')
                ],
                id='box_nbr_observation'
            ),
            html.Div(
                [
                    DashIconify(icon="bi:flag", width=20),
                    html.Span('État de la zone :', id='text_state_area'),
                    html.Span(state, id='value_state_area')
                ],
                id='box_state_area'
            ),
            dmc.Divider(variant='solid', className='divider_infos'),
            html.Div(
                [
                    html.Span('État de la zone', id='name_graph')
                ],
                className='box_title_name'
            ),
            tabs(dfPieArea, figPieObs)
        ],
        id='infos_sub_container'
    )

def tabs(dfPieArea, dfPieObs):
    return html.Div(
        dmc.Tabs(
            [
                dmc.TabsList(
                    [
                        dmc.Tab("Par sous zone", value="area"),
                        dmc.Tab("Par observation", value="observation")
                    ]
                ),
                dmc.TabsPanel(
                    dcc.Graph(
                        figure=figure.build_pie_chart_map(dfPieArea, APIS_INFO.get_api('ecoulements')),
                        id='area_result_tab'
                    ),
                    value="area"),
                dmc.TabsPanel(
                    dcc.Graph(
                        figure=figure.build_pie_chart_map(dfPieObs, APIS_INFO.get_api('ecoulements')),
                        id='observation_result_tab'
                    ),
                    value="observation")
            ],
            value='area',
            id='tabs_result_by_observation_or_area'
        ),
        id='box_result_graph'
    )

# --- CALLBACKS ---

@callback(
    [
        Output('geojson_mapbox', 'data'),
        Output('path_to_area', 'data'),

        Output('geojson_mapbox', 'clickData'),

        Output('name_area', 'children'),
        Output('value_nbr_observation', 'children'),
        Output('value_state_area', 'children'),

        Output('area_result_tab', 'figure'),
        Output('observation_result_tab', 'figure'),
    ],
    [
        Input('geojson_mapbox', 'clickData'),
        Input('btn_home_france', 'n_clicks'),
        Input('btn_backward', 'n_clicks'),
        Input('date_range_picker', 'value'),
    ],
    [
        State('path_to_area', 'data'),
    ],
    prevent_initial_callbacks=True)
def update_map_and_path_on_click(inClickData, inBtnHome, inBtnBack, inDatePick, statePathToArea):
    triggeredId = ctx.triggered_id

    mapData, pathData = [no_update] * 2
    geosjonClickData = None
    nameArea, nbrObs, stateArea = [no_update] * 3
    figPieArea, figPieObs = [no_update] * 2

    if triggeredId is None:
        return mapData, pathData, geosjonClickData, nameArea, nbrObs, stateArea, figPieArea, figPieObs

    if triggeredId == 'btn_home_france':
        mapData, pathData = btn_home_map(inBtnHome)
    
    if triggeredId == 'btn_backward':
        mapData, pathData = btn_backward(inBtnBack, statePathToArea)

    if triggeredId == 'geojson_mapbox':
        mapData, pathData = go_in_area(inClickData, statePathToArea)
    
    if triggeredId == 'date_range_picker':
        mapData = FRANCE.get_from_path(statePathToArea)

    mapData, nbrObs, stateArea, dfPieArea, dfPieObs = db_requests.data_map(mapData, inDatePick, APIS_INFO.get_api('ecoulements'))

    if dfPieArea is not None:
        figPieArea = figure.build_pie_chart_map(dfPieArea, APIS_INFO.get_api('ecoulements'))

    if dfPieObs is not None:
        figPieObs = figure.build_pie_chart_map(dfPieObs, APIS_INFO.get_api('ecoulements'))

    if pathData != no_update:
        nameArea = pathData[-1]

    return mapData, pathData, geosjonClickData, nameArea, nbrObs, stateArea, figPieArea, figPieObs

def btn_home_map(btn: int):
    """
    Manages the button that takes you back to the most zoomed-out area (France).
    """
    if not btn:
        return no_update, no_update
    return FRANCE, [FRANCE.name]

def btn_backward(btn: int, pathToArea: list):
    if not btn:
        return no_update, no_update
    if len(pathToArea[:-1]) > 1:
        return FRANCE.get_from_path(pathToArea[:-1]), pathToArea[:-1]
    return FRANCE, [FRANCE.name]

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
        return FRANCE.get_from_path(pathToArea), pathToArea
    return FRANCE.get_from_path(pathToArea), no_update

# @callback(
#     [
#         Output('name_area', 'children'),
#         Output('value_nbr_observation', 'children'),
#         Output('value_state_area', 'children'),
#     ],
#     [
#         Input('path_to_area', 'data')
#     ])
# def update_name_of_area_on_click(inPathToArea):
#     return inPathToArea[-1], 0, 'Inconnu'

