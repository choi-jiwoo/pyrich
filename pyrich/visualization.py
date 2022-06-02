import pandas as pd
import plotly.express as px
from typing import Iterable


def draw_line(data: pd.DataFrame, **kwargs):
    fig = px.line(data, **kwargs)
    fig.update_layout(
        margin=dict(t=10, l=0, r=0, b=0),
        xaxis=dict(showgrid=False, title=None),
        yaxis=dict(showgrid=False, title=None),
        plot_bgcolor='white',
        showlegend=False,
    )
    fig.update_traces(
        line=dict(color='blue'),
    )
    return fig

def draw_pie(data: pd.DataFrame, **kwargs):
    fig = px.pie(data, **kwargs)
    fig.update_layout(margin=dict(t=10, l=0, r=0, b=10))
    return fig

def draw_treemap(data: pd.DataFrame, treemap_name: str, section: tuple, **kwargs):
    fig = px.treemap(data, path=[px.Constant(treemap_name), *section], **kwargs)
    fig.update_traces(dict(
        texttemplate='%{label}<br>%{customdata}%',
        hovertemplate=None,
        textposition='middle center',
        insidetextfont=dict(family=('Trebuchet MS', 'Arial'), size=20),
    ))
    fig.update_layout(
        margin=dict(t=0, l=40, r=40, b=100),
        coloraxis=dict(showscale=False),
    )
    return fig