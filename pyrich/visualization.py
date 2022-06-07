import pandas as pd
import plotly.express as px


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

def draw_stock_chart(close: pd.Series, average_price: float, **kwargs):
    fig = px.line(close, **kwargs)
    fig.update_layout(
        margin=dict(t=0, l=0, r=0, b=0),
        xaxis=dict(title=None),
        yaxis=dict(title=None),
        showlegend=False,
        shapes=[
            dict(
                line=dict(color='gray'),
                x0=0,
                x1=1,
                y0=average_price,
                y1=average_price,
                xref='paper',
                yref='y',
                line_width=1,
            )
        ],
    )
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label='1m', step='month', stepmode='backward'),
                dict(count=6, label='6m', step='month', stepmode='backward'),
                dict(count=1, label='YTD', step='year', stepmode='todate'),
                dict(count=1, label='1y', step='year', stepmode='backward'),
                dict(step='all')
            ])
        )
    )
    return fig

def draw_pie(data: pd.DataFrame, **kwargs):
    fig = px.pie(data, **kwargs)
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
        margin=dict(t=0, l=40, r=40, b=0),
        coloraxis=dict(showscale=False),
    )
    return fig