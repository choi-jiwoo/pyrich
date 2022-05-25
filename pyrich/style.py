import pandas as pd


GREEN = '#137333'
RED = '#a50e0e'

def style_table(table: pd.DataFrame, style: str, subset: list) -> pd.DataFrame:
    styled_table = table.style.applymap(style, subset=subset)
    return styled_table

def style_change(value: float) -> str:
    color = {
        'neg': RED,
        'pos': GREEN,
    }
    style = None
    if value > 0:
        style = f"color:{color['pos']};"
    elif value < 0:
        style = f"color:{color['neg']};"
    return style

def style_trade_type(_type: str) -> str:
    color = {
        'buy': GREEN,
        'sell': RED,
    } 
    if _type == 'buy':
        style = f"color:{color['buy']};"
    elif _type == 'sell':
        style = f"color:{color['sell']};"
    return style