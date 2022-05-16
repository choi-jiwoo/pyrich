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
    if options['delete']:
        table_name = options['delete']
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
    new_record = Transaction(options)

    if new_record.record['type'] == 'dividend':
        keys = ['date', 'symbol', 'price']
        record = new_record.record_dividends(keys)
        db.insert('dividend', record)
    else:
        record = new_record.record_transactions()
        db.insert('transaction', record)
