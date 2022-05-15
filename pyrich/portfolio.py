from collections import deque
import pandas as pd
import numpy as np
from pyrich.record import Record
from pyrich import stock


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
        stock['quantity'] = stock['buy'] - stock['sell']
        return stock

    def _get_earnings(self) -> pd.DataFrame:
        earnings = self._get_pivot_table('total_price_paid')
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

    def _get_stock_quote(self, portfolio: pd.DataFrame) -> pd.DataFrame:
        portfolio_stock_price = []

        for symbol in portfolio.index:
            country = portfolio.loc[symbol, 'country']
            current_stock_data = stock.get_current_price(symbol, country)
            portfolio_stock_price.append(current_stock_data)

        day_change = pd.DataFrame(portfolio_stock_price)
        day_change['dp'] = day_change['dp'].apply(round, args=(2,))
        col_name = ['current_price', 'day_change(%)']
        day_change.columns = col_name
        day_change.index = portfolio.index
        current_portfolio = portfolio.join(day_change)
        return current_portfolio

    def _get_gain(self, current_portfolio: pd.DataFrame) -> tuple:
        price_data = current_portfolio[['current_value', 'invested_amount']]
        total_gain = price_data.agg(lambda x: x[0]-x[1], axis=1)
        pct_gain = price_data.agg(lambda x: (x[0]-x[1])/x[1], axis=1)
        pct_gain *= 100
        pct_gain = round(pct_gain, 2)
        return total_gain, pct_gain

    def _get_current_stock_value(self, current_portfolio: pd.DataFrame) -> pd.Series:
        investment = current_portfolio[['quantity', 'current_price']]
        current_stock_value = investment.agg(np.prod, axis=1)
        return current_stock_value

    def current_portfolio(self) -> pd.DataFrame:
        quantity = self._get_current_stock()
        earnings = self._get_earnings()
        transaction_summary = earnings.join(quantity['quantity'])
        
        currently_owned_stock = transaction_summary[transaction_summary['quantity'] > 0]
        currently_owned_stock = currently_owned_stock.fillna(0)
        currently_owned_stock['invested_amount'] = currently_owned_stock['buy'] - currently_owned_stock['sell']
        currently_owned_stock.drop(['buy', 'sell'], axis=1, inplace=True)
        
        portfolio = pd.DataFrame(currently_owned_stock)
        portfolio.reset_index('country', inplace=True)
        portfolio_average_price = self._get_portfolio_average_price(portfolio)
        portfolio = portfolio.join(portfolio_average_price)
        portfolio = self._map_currency(portfolio)

        current_portfolio = self._get_stock_quote(portfolio)
        current_stock_value = self._get_current_stock_value(current_portfolio)
        current_portfolio['current_value'] = current_stock_value
        total_gain, pct_gain = self._get_gain(current_portfolio)
        current_portfolio['total_gain'] = total_gain
        current_portfolio['pct_gain(%)'] = pct_gain

        col_order = [
            'country',
            'quantity',
            'current_price',
            'day_change(%)',
            'average_price_paid',
            'pct_gain(%)',
            'current_value',
            'invested_amount',
            'total_gain',
            'currency',
        ]
        current_portfolio = current_portfolio[col_order]
        return current_portfolio

    def get_investment_by_country(self, portfolio: pd.DataFrame) -> pd.DataFrame:
        country_group = portfolio[['country', 'invested_amount', 'currency']]
        country_group = country_group.groupby('country')
        investment_by_country = country_group.agg(
            {
                'invested_amount': np.sum,
                'currency': lambda x: np.unique(x)[0]
            }
        )
        return investment_by_country

    def __repr__(self) -> str:
        return f"Portfolio(name='{self.name}', table='{self.table}')"