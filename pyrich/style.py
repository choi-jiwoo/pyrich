import pandas as pd


BLACK = '#000000'
GREEN = '#137333'
RED = '#a50e0e'

def style_table(table: pd.DataFrame, style: str, subset: list) -> pd.DataFrame:
    styled_table = table.style.applymap(style, subset=subset)
    return styled_table

def style_neg_value(value: float) -> str:
    return f'color:{RED};' if value < 0 else None

def style_change(value: float) -> str:
    color = {
        'zero': BLACK,
        'neg': RED,
        'pos': GREEN,
    }
    style = None
    if value > 0:
        style = f"color:{color['pos']};"
    elif value < 0:
        style = f"color:{color['neg']};"
    else:
        style = f"color:{color['zero']};"
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