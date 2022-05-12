from collections import deque
import pandas as pd
import numpy as np
from pyrich.record import Record


class Portfolio(Record):

    def __init__(self, name: str, table: str) -> None:
        super().__init__(table)
        self.name = name

    def _get_pivot_table(self, column: str, remove_na: bool=False) -> pd.DataFrame:
        record_pivot_table = pd.pivot_table(
            self.record,
            values=column,
            index=['country', 'symbol'],
            columns='type',
            aggfunc=np.sum
        )
        if remove_na:
            record_pivot_table.fillna(0, inplace=True)
        return record_pivot_table

    def _get_current_stock(self) -> pd.DataFrame:
        stock = self._get_pivot_table('quantity', remove_na=True)
        stock['amount'] = stock['buy'] - stock['sell']
        return stock

    def _get_earnings(self) -> pd.DataFrame:
        earnings = self._get_pivot_table('total_price_paid')
        earnings['amount'] = earnings['sell'] - earnings['buy']
        return earnings
    
    def _get_average_price_paid(self, symbol: str) -> float:
        symbol_transaction = self.record[self.record['symbol']==symbol]
        symbol_transaction = symbol_transaction[['type', 'quantity', 'price']]
        transactions = deque()
        for i in symbol_transaction.values:
            transaction_type = i[0]
            quantity = i[1]
            price = i[2]
            while quantity > 0:
                if transaction_type == 'buy':
                    transactions.append(price)
                else:
                    transactions.popleft()
                quantity -= 1
        transactions = np.array(transactions)
        try:
            average_price_paid = transactions.mean()
        except Exception:
            average_price_paid = 0
        finally:
            return average_price_paid

    def _get_portfolio_average_price(self, portfolio: pd.DataFrame) -> pd.Series:
        average_price_paid = {
            symbol: self._get_average_price_paid(symbol)
            for symbol
            in portfolio.index
        }
        average_price_paid = pd.Series(
            average_price_paid,
            name='average_price_paid'
        )
        return average_price_paid

    def _map_currency(self, portfolio: pd.DataFrame) -> pd.DataFrame:
        currency_mapping = {
            'CRYPTO': 'KRW',
            'KOR': 'KRW',
            'USA': 'USD',
        }
        portfolio['currency'] = [
            currency_mapping[country]
            for country
            in portfolio['country']
        ]
        return portfolio

    def summary(self) -> pd.DataFrame:
        quantity = self._get_current_stock()
        quantity = quantity[quantity['amount'] > 0]
        quantity = quantity['amount']

        earnings = self._get_earnings()
        earnings = earnings[earnings['amount'].isna()]
        total_price_paid = earnings['buy']

        data = {'quantity': quantity, 'total_price_paid': total_price_paid}
        portfolio = pd.DataFrame(data)
        portfolio.reset_index('country', inplace=True)
        portfolio_average_price = self._get_portfolio_average_price(portfolio)
        portfolio = portfolio.join(portfolio_average_price)
        portfolio = self._map_currency(portfolio)
        return portfolio

    def get_stock_by_country(self, portfolio: pd.DataFrame) -> pd.DataFrame:
        country_group = portfolio[['country', 'total_price_paid', 'currency']]
        country_group = country_group.groupby('country')
        stock_by_country = country_group.agg(
            {
                'total_price_paid': np.sum,
                'currency': lambda x: np.unique(x)[0]
            }
        )
        return stock_by_country

    def get_total_stock_value_in_krw(self, stock_by_country: pd.DataFrame) -> pd.DataFrame:
        us_stock_value_in_krw = stock_by_country.loc['USA', 'total_price_paid'] * self.forex_usd_to_won
        stock_value_in_krw = stock_by_country.drop('USA')
        stock_value_in_krw = stock_value_in_krw.agg({'total_price_paid': np.sum})
        total_stock_value_in_krw = stock_value_in_krw + us_stock_value_in_krw
        total_stock_value_in_krw.rename({'total_price_paid': 'total_stock_value'}, inplace=True)
        return total_stock_value_in_krw

    def __repr__(self) -> str:
        return f"Portfolio(name='{self.name}', table='{self.table}')"