import os
from pyrich.database import PostgreSQL
from pyrich import parse
from pyrich.transaction import Transaction
from pyrich.error import CurrencyError


def run():
    # Load arguments
    parser = parse.set_args()
    args = parser.parse_args()
    options = vars(args)

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
