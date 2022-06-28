import os
from pyrich.database import PostgreSQL
from pyrich import parse
from pyrich.transaction import Transaction
from pyrich.error import CurrencyError
from pyrich.asset import Asset
from pyrich.portfolio import Portfolio
from pyrich.cash import Cash
from pyrich.summary import portfolio_data
from pyrich.summary import cash_data
from pyrich.summary import current_asset_data
from pyrich.visualization import draw_current_asset


def run():
    # Load arguments
    parser = parse.set_args()
    args = parser.parse_args()
    options = vars(args)

    portfolio = Portfolio('Choi Ji Woo', 'transaction')
    cash = Cash('cash')
    asset = Asset('current_asset')
    
    portfolio_table, portfolio_value = portfolio_data(portfolio)
    total_cash = cash_data(cash)
    total_cash_value = total_cash.item()
    cur_asset_value = current_asset_data(portfolio_value['current_value'], total_cash_value)
    current_asset = asset.record
    asset.record_current_asset(cur_asset_value)

    if options['summary']:
        print(f"{'Current Portfolio Value':<24}: {cur_asset_value:>5,.2f}원\n"
              f"{'Current Stock Value':<24}: {portfolio_value['current_value']:>5,.2f}원\n"
              f"{'Current Cash':<24}: {total_cash_value:>5,.2f}원\n")
        
        fig = draw_current_asset(current_asset['date'], current_asset['amount'], title='Portfolio Summary', color='blue')
        fig.show()
        return

    # Open a portfolio dashboards
    if options['web']:
        os.system('streamlit run dashboard.py')
        return

    # Set up database connection
    db = PostgreSQL()

    # Copy record from csv file
    if options['csv']:
        table_name = options['csv']
        db.copy_from_csv(table_name)
        return

    # Disaply database table
    if options['show']:
        table_name = options['show']
        table = db.show_table(table_name, msg=False)
        print(table)
        return

    # Handling delete option
    if options['deletelast']:
        table_name = options['deletelast']
        db.delete_rows(table_name)
        return

    if options['deleteall']:
        table_name = options['deleteall']
        db.delete_rows(table_name, all_rows=True)
        return

    # Update current cash
    if options['cash']:
        cash_record = options['cash']
        currency_id = {
            'KRW': 1,
            'USD': 2,
        }
        amount = cash_record[0]
        currency = cash_record[1]
        try:
            _id = currency_id[currency]
            cols_to_update = ['amount']
            db.update('cash', cols_to_update, [amount], _id)
        except KeyError:
            raise CurrencyError('Currency should be either USD or KRW.')
        else:
            return

    # Record transaction
    if options['dividend'] is None:
        headers = ['date', 'country', 'type', 'symbol', 'quantity', 'price']
        transaction = Transaction(options['transaction'], headers=headers)
        transaction_record = transaction.record
        transaction_record['total_price_paid'] = transaction_record['quantity'] * transaction_record['price']
        db.insert('transaction', transaction_record)
    else:
        headers = ['date', 'symbol', 'dividend', 'currency']
        dividends = Transaction(options['dividend'], headers=headers)
        dividends_record = dividends.record
        db.insert('dividend', dividends_record)
