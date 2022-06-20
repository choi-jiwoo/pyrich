import pandas as pd
from pyrich.portfolio import Portfolio
from pyrich.cash import Cash


def portfolio_data(portfolio: Portfolio) -> tuple[pd.DataFrame, pd.Series]:
    portfolio_table = portfolio.current_portfolio()
    portfolio_value = portfolio.get_current_portfolio_value(portfolio_table)
    return portfolio_table, portfolio_value

def cash_data(current_cash: Cash) -> pd.Series:
    total_cash = current_cash.get_total_cash_in_krw()
    return total_cash

def current_asset_data(current_stock_value: float, current_cash: float) -> float:
    cur_asset_value = current_stock_value + current_cash
    return cur_asset_value