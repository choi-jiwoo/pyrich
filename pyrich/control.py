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

    # Record transaction 
    new_record = Transaction(options)

    if new_record.record['type'] == 'dividend':
        keys = ['date', 'symbol', 'price']
        record = new_record.record_dividends(keys)
        db.insert('dividend', record)
    else:
        record = new_record.record_transactions()
        db.insert('transaction', record)

    if new_record.record['web']:
        os.system('streamlit run dashboard.py')
