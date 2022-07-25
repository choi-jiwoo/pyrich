from copy import deepcopy
import pandas as pd
from pyrich.portfolio import Portfolio
from pyrich.cash import Cash
from pyrich.record import Record
from pyrich.forex import get_usd_to_krw


def portfolio_data(portfolio: Portfolio) -> tuple[pd.DataFrame, pd.Series]:
    portfolio_table = portfolio.current_portfolio()
    portfolio_value = portfolio.get_current_portfolio_value(portfolio_table)
    return portfolio_table, portfolio_value

def current_portfolio(portfolio_table: pd.DataFrame, display_krw: bool) -> pd.DataFrame:
    drop_col = ['current_value', 'invested_amount', 'total_gain']
    current_portfolio = portfolio_table.drop(drop_col, axis=1)
    if display_krw:
        current_portfolio['currency'] = Record.map_currency(current_portfolio['country'])
    return current_portfolio

def total_realized_gain_in_krw(realized_gain_table: pd.DataFrame) -> pd.DataFrame:
    usd_to_krw = get_usd_to_krw()
    realized_gain_table = deepcopy(realized_gain_table)
    currency_grp = realized_gain_table.groupby('currency')
    usd_idx = currency_grp.indices['USD']
    stocks_in_usd = currency_grp.get_group('USD')
    realized_gain_table.iloc[usd_idx, 1:-1] = stocks_in_usd.iloc[:, 1:-1] * usd_to_krw
    realized_gain_table.drop(['country', 'currency'], axis=1, inplace=True)
    total_realized_gain = realized_gain_table.sum().to_frame(name='KRW').T
    return total_realized_gain

def cash_data(current_cash: Cash) -> pd.Series:
    total_cash = current_cash.get_total_cash_in_krw()
    return total_cash

def current_asset_data(current_stock_value: float, current_cash: float) -> float:
    cur_asset_value = current_stock_value + current_cash
    return cur_asset_value

def current_yield(gain: float, invested: float):
    return (gain / invested) * 100