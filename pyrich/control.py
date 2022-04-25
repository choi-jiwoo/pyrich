import os
from dotenv import load_dotenv
from pyrich.database import PostgreSQL
from pyrich import parse
from pyrich.transaction import Transaction


def run():
    # Set up database connection
    load_dotenv()
    database_url = os.environ.get('DATABASE_URL')
    db = PostgreSQL(database_url)

    # Load arguments
    parser = parse.set_args()
    args = parser.parse_args()
    options = vars(args)

    # Copy record from csv file
    if options['csv']:
        table_name = options['csv']
        db.copy_from_csv(table_name)
        return

    # Disaply database table
    if options['show']:
        table_name = options['show']
        db.show_table(table_name)
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

    # Open a portfolio dashboards
    if options['web']:
        os.system('streamlit run dashboard.py')
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

