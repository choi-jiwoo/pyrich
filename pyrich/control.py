import os
from dotenv import load_dotenv
from pyrich.database import PostgreSQL
from pyrich import parse
from pyrich.transaction import Transaction


def run():
    parser = parse.set_args()
    args = parser.parse_args()
    options = vars(args)
    new_record = Transaction(options)
    load_dotenv()
    database_url = os.environ.get('DATABASE_URL')
    db = PostgreSQL(database_url)

    if new_record.record['crypto']:
        # record transaction of buying or selling cryptocurrency
        pass

    if new_record.record['type'] == 'dividend':
        # record dividends received
        pass
    else:
        quantity = new_record.record['quantity']
        price = new_record.record['price']
        new_record.record['total_amount'] = quantity * price

    if new_record.record['web']:
        os.system('streamlit run dashboard.py')
