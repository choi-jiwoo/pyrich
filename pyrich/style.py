import pandas as pd


def style_change(value: float) -> str:
    color = {
        'neg': '#a50e0e',
        'pos': '#137333',
    }
    style = None
    if value > 0:
        style = f"color:{color['pos']};"
    elif value < 0:
        style = f"color:{color['neg']};"
    return style