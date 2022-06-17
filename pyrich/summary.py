from pyrich.portfolio import Portfolio
from pyrich.asset import Asset
from pyrich.cash import Cash


class FinancialSummary:

    @property
    def portfolio(self):
        return Portfolio('Choi Ji Woo', 'transaction')

    @property
    def cash(self):
        return Cash('cash')

    @property
    def asset(self):
        return Asset('current_asset')