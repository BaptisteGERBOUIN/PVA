from datetime import date

from dash import register_page, Input, Output, State, no_update, callback
from dash import html, dcc

from data.api_fetcher import get_water_flow_data
from data.geojson_processing import FRANCE, GeographicArea

import dash_bootstrap_components as dbc
import dash_leaflet as dl
import plotly.express as px

register_page(__name__, title='Water A')

# --- HTML ---

def layout():
    return [
        dcc.Store(id='path-to-area', data=['France']),
        html.Div(
            [
                menu_map(),
                dl.Map(
                    [
                        dl.TileLayer(),
                        dl.GeoJSON(
                            data=FRANCE.gdf_to_json(),
                            zoomToBounds=True,
                            zoomToBoundsOnClick=True,
                            hoverStyle={'color': '#666'},
                            id='geojson_mapbox'
                        ),
                        dl.EasyButton(icon="bi bi-house-door", title="Home France", id="btn_home_france")
                    ],
                    zoomSnap=0.2,
                    dragging=True,
                    maxBounds=FRANCE.getMaxBounds(),
                    id='zoomable_map'
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

# --- FIGURE ---

def get_choropleth(geoArea: GeographicArea):
    fig = px.choropleth(
        data_frame=geoArea.gdf, 
        geojson=geoArea.gdf, 
        locations=geoArea.gdf.index, 
        scope='europe',
        fitbounds='locations',
        hover_name='name',
        basemap_visible=False
    )

    fig.update_layout(
        showlegend=False, 
        paper_bgcolor='rgba(0,0,0,0)',
        margin={'r': 0, 't': 0, 'l': 0, 'b': 0}
    )

    return fig

# --- CALLBACKS ---

@callback(
    [Output('map', 'figure'),
     Output('path-to-area', 'data')],
    [Input('geojson_mapbox', 'clickData'),
     Input('box-map', 'n_clicks')],
    [State('path-to-area', 'data'),
     State('map', 'hoverData')],
    prevent_initial_call=True)
def update_map_on_click(clickData, nClicks, pathToArea, hoverMap):
    if hoverMap is None:
        return click_outside_area(pathToArea)
    
    if clickData is None:
        return no_update, no_update

    return click_inside_area(clickData, pathToArea)
    
def click_inside_area(clickData, pathToArea):
    area_name = clickData['points'][0].get('hovertext')
    if area_name is None:
        return no_update, no_update

    if pathToArea[-1] != area_name:
        pathToArea = pathToArea + [area_name]
        return get_choropleth(FRANCE.get_from_path(pathToArea)), pathToArea
    return get_choropleth(FRANCE.get_from_path(pathToArea)), no_update

def click_outside_area(pathToArea):
    if len(pathToArea) > 1:
        pathToArea = pathToArea[:-1]
        return get_choropleth(FRANCE.get_from_path(pathToArea)), pathToArea
    return get_choropleth(FRANCE), no_update