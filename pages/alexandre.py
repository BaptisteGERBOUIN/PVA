from dash import register_page, Input, Output, State, no_update, callback, ctx
from dash_extensions.javascript import assign
from dash_iconify import DashIconify
from dash import html, dcc

import dash_mantine_components as dmc
import dash_leaflet as dl
import dash_leaflet.express as dlx

from data.map_pratical_data import APIS_INFO
from data.geojson_processing import FRANCE

from data.map_pratical_data import Api

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
                        id='date_range_picker',
                        minDate=APIS_INFO.get_api('ecoulements').min_date,
                        maxDate=APIS_INFO.get_api('ecoulements').max_date,
                        value=[APIS_INFO.get_api('ecoulements').max_date, APIS_INFO.get_api('ecoulements').max_date],
                        disabledDates=APIS_INFO.get_api('ecoulements').disabled_dates,
                        allowSingleDateInRange=True,
                        clearable=False,
                    ),
                    id='map_date_picker_container'
                ),
                dmc.Switch(
                    checked=False,
                    onLabel='QUALITÉ',
                    offLabel='QUANTITÉ',
                    size='lg',
                    id='switch_qualite_quantite'
                ),
                dmc.Select(
                    data=APIS_INFO.get_api('qualite_rivieres').parameters_names,
                    value=APIS_INFO.get_api('qualite_rivieres').parameters_names[0],
                    nothingFound="No options found",
                    id='dropdown_parameters',
                    style={'display': 'none'}
                )
            ],
            id='map_menu_container',
        ),
        id='map_menu_decor'
    )

def viewport_map():
    style_handle = assign('''
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
    ''')
    return dl.Map(
        [
            # dl.TileLayer(), #add basemap (open-street-map)
            dl.GeoJSON(
                data=db_requests.data_map_ecoulement(
                    area=FRANCE,
                    date_range=[APIS_INFO.get_api('ecoulements').max_date, APIS_INFO.get_api('ecoulements').max_date],
                    api=APIS_INFO.get_api('ecoulements')
                )[0],
                style=style_handle,
                zoomToBounds=True,
                hoverStyle={'color': '#666'},
                id='geojson_mapbox',
                hideout=APIS_INFO.get_api('ecoulements').get_hideout()
            ),
            dlx.categorical_colorbar(
                categories=APIS_INFO.get_api('ecoulements').get_hideout()['classes'],
                colorscale=APIS_INFO.get_api('ecoulements').get_hideout()['colorscale'],
                width=500,
                height=30,
                position='bottomleft',
                id='colorbar_map'
            ),
            dl.EasyButton(n_clicks=0, icon='bi bi-house-door', title=f'Voir {FRANCE.name} entière', id='btn_home_france'),
            dl.EasyButton(n_clicks=0, icon='bi bi-arrow-90deg-left', title='Revenir en arrière', id='btn_backward')
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
    _, nbr_obs, state, dfPieArea, figPieObs = db_requests.data_map_ecoulement(
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
                    DashIconify(icon='bi:clipboard-data', width=20),
                    html.Span('Nombre d\'observation :', id='text_nbr_observation'),
                    html.Span(nbr_obs, id='value_nbr_observation')
                ],
                id='box_nbr_observation'
            ),
            html.Div(
                [
                    DashIconify(icon='bi:flag', width=20),
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
                        dmc.Tab('Par sous zone', value='area'),
                        dmc.Tab('Par observation', value='observation')
                    ]
                ),
                dmc.TabsPanel(
                    dcc.Graph(
                        figure=figure.build_pie_chart_map(dfPieArea, APIS_INFO.get_api('ecoulements')),
                        id='area_result_tab'
                    ),
                    value='area'),
                dmc.TabsPanel(
                    dcc.Graph(
                        figure=figure.build_pie_chart_map(dfPieObs, APIS_INFO.get_api('ecoulements')),
                        id='observation_result_tab'
                    ),
                    value='observation')
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

        Output('date_range_picker', 'value'),
        Output('date_range_picker', 'minDate'),
        Output('date_range_picker', 'maxDate'),
        Output('date_range_picker', 'disabledDates'),

        Output('colorbar_map', 'max'),
        Output('colorbar_map', 'classes'),
        Output('colorbar_map', 'colorscale'),
        Output('colorbar_map', 'tickValues'),
        Output('colorbar_map', 'tickText'),

        Output('geojson_mapbox', 'hideout'),
    ],
    [
        Input('geojson_mapbox', 'clickData'),
        Input('btn_home_france', 'n_clicks'),
        Input('btn_backward', 'n_clicks'),
        Input('date_range_picker', 'value'),
        Input('switch_qualite_quantite', 'checked'),
        Input('dropdown_parameters', 'value'),
    ],
    [
        State('path_to_area', 'data'),
    ],
    prevent_initial_callbacks=True)
def update_map_and_path_on_click(inClickData, inBtnHome, inBtnBack, inDatePick, inChecked, inParemeter, statePathToArea):
    triggeredId = ctx.triggered_id

    mapData, pathData = [no_update] * 2
    geosjonClickData = None
    nameArea, nbrObs, stateArea = [no_update] * 3
    figPieArea, figPieObs = [no_update] * 2
    date = {'value': no_update, 'minDate': no_update, 'maxDate': no_update, 'disabledDates': no_update}
    legend = {'max': no_update, 'classes': no_update, 'colorscale': no_update, 'tickValues': no_update, 'tickText': no_update}
    hideout = no_update

    if triggeredId is None:
        return mapData, pathData, geosjonClickData, nameArea, nbrObs, stateArea, figPieArea, figPieObs, *list(date.values()), *list(legend.values()), hideout

    api = APIS_INFO.get_api('ecoulements')
    if inChecked:
        api = APIS_INFO.get_api('qualite_rivieres')

    if triggeredId == 'btn_home_france':
        mapData, pathData = btn_home_map(inBtnHome)
    
    if triggeredId == 'btn_backward':
        mapData, pathData = btn_backward(inBtnBack, statePathToArea)

    if triggeredId == 'geojson_mapbox':
        mapData, pathData = go_in_area(inClickData, statePathToArea)

    if triggeredId == 'switch_qualite_quantite':
        date['value'] = [api.max_date, api.max_date]
        date['minDate'] = api.min_date
        date['maxDate'] = api.max_date
        date['disabledDates'] = api.disabled_dates
        inDatePick = [api.max_date, api.max_date]

    if triggeredId in ['switch_qualite_quantite', 'dropdown_parameters']:
        if inChecked:
            legend = update_legend(legend, api, inParemeter)
            hideout = api.get_hideout(inParemeter)
        else:
            legend = update_legend(legend, api, 'default')
            hideout = api.get_hideout()

    
    if triggeredId in ['switch_qualite_quantite', 'date_range_picker', 'dropdown_parameters']:
        mapData = FRANCE.get_from_path(statePathToArea)

    mapData, nbrObs, stateArea, figPieArea, figPieObs = update_with_data(
        mapData, inDatePick, inChecked, inParemeter, nbrObs, stateArea, figPieArea, figPieObs)

    if pathData != no_update:
        nameArea = pathData[-1]

    return mapData, pathData, geosjonClickData, nameArea, nbrObs, stateArea, figPieArea, figPieObs, *list(date.values()), *list(legend.values()), hideout

def btn_home_map(btn: int):
    '''
    Manages the button that takes you back to the most zoomed-out area (France).
    '''
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
    '''
    Manages a click event to navigate to a specific zone based on the click data 
    supplied and the current path to the zone.
    '''
    if clickData is None:
        return no_update, no_update
    areaName = clickData['properties']['name']

    if pathToArea[-1] != areaName:
        pathToArea = pathToArea + [areaName]
        return FRANCE.get_from_path(pathToArea), pathToArea
    return FRANCE.get_from_path(pathToArea), no_update

def update_with_data(mapData, inDatePick, inChecked, inParemeter, nbrObs, stateArea, figPieArea, figPieObs):
    if inChecked:
        api_name = 'qualite_rivieres'
        mapData, nbrObs, stateArea, dfPieArea, dfPieObs = db_requests.data_map_qualite_rivieres(
            mapData, inDatePick, APIS_INFO.get_api(api_name), inParemeter)
        figPieArea = figure.build_pie_chart_map(dfPieArea, APIS_INFO.get_api(api_name), inParemeter)
        figPieObs = figure.build_pie_chart_map(dfPieObs, APIS_INFO.get_api(api_name), inParemeter)
    else:
        api_name = 'ecoulements'
        mapData, nbrObs, stateArea, dfPieArea, dfPieObs = db_requests.data_map_ecoulement(
            mapData, inDatePick, APIS_INFO.get_api(api_name))
        figPieArea = figure.build_pie_chart_map(dfPieArea, APIS_INFO.get_api(api_name))
        figPieObs = figure.build_pie_chart_map(dfPieObs, APIS_INFO.get_api(api_name))

    return mapData, nbrObs, stateArea, figPieArea, figPieObs

def update_legend(legend, api: Api, parameter: str):
    legend = {'max': no_update, 'classes': no_update, 'colorscale': no_update, 'tickValues': no_update, 'tickText': no_update}
    indices = list(range(len(api.get_hideout(parameter)['classes']) + 1))
    legend['max'] = len(api.get_hideout(parameter)['classes'])
    legend['classes'] = indices
    legend['colorscale'] = api.get_hideout(parameter)['colorscale']
    legend['tickValues'] = [item + 0.5 for item in indices[:-1]]
    legend['tickText'] = api.get_hideout(parameter)['classes']
    return legend

@callback(
    [
        Output('dropdown_parameters', 'style'),
    ],
    [
        Input('switch_qualite_quantite', 'checked'),
    ]
)
def toggle_dropdown(inChecked):
    if inChecked:
        return {'display': 'block'}, 
    return {'display': 'none'}, 