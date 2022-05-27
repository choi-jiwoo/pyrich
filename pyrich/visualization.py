import pandas as pd
import plotly.express as px
from typing import Iterable


def draw_pie(data: pd.DataFrame, **kwargs):
    fig = px.pie(data, **kwargs)
    return fig
