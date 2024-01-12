import plotly.express as px
import pandas as pd

from data.map_pratical_data import Api

def build_pie_chart_map(df: pd.DataFrame, api: Api, parameter: str='default'):
    return px.pie(
        df,
        values='count',
        color='encoded_result',
        color_discrete_map=api.get_colorscale(parameter)
    )