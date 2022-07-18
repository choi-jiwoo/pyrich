from datetime import datetime
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
from pyrich.summary import current_yield
from pyrich.style import style_change
from pyrich.style import style_terminal_text


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
    asset.record_current_asset(cur_asset_value)
    portfolio_w_cash = portfolio.get_portfolio_w_cash(portfolio_table, total_cash_value).to_frame(name='Values in KRW')

    if options['summary']:
        today = datetime.today()
        today_string = today.strftime('%Y %B %d %A, %X')
        print(style_terminal_text(
                text=f"\n{today_string}\n",
                color='magenta',
                style='bold'
            )
        )

        portfolio_table.reset_index('symbol', inplace=True)
        stocks = portfolio_table[['symbol', 'current_price', 'currency', 'pct_gain(%)']].values
        gain = portfolio_value['portfolio_gain']
        invested = portfolio_value['invested_amount']
        _yield = current_yield(gain, invested)
        current_value = portfolio_value['current_value']
        print(style_terminal_text(
            text='FINANCIAL SUMMARY',
            style='bold',
        ))
        print(style_terminal_text(
                text='PORTFOLIO',
                color='red',
                style='bold',
            ),
            f"▸",
            style_terminal_text(
                text=f"{cur_asset_value:,.2f} 원",
                style='bold',
            ),
            style_terminal_text(
                text=f"({_yield:,.2f} %)",
                color=style_change(_yield, 'terminal'),
            )
        )
        print(style_terminal_text(
                text='INVESTED',
                color='red',
                style='bold',
            ),
            f" ▸",
            style_terminal_text(
                text=f"{invested:,.2f} 원",
            ),
        )

        print(style_terminal_text(
            text=f'\nPORTFOLIO SUMMARY',
            style='bold',
        ))
        for i in stocks:
            pct_change = i[3]
            print(
                style_terminal_text(
                    text=i[0],
                    color='red',
                    style='bold',
                ),
                f"▸ {i[1]} {i[2]}",
                style_terminal_text(
                    text=f"({i[3]} %)",
                    color=style_change(pct_change, 'terminal'),
                )
            )
        
        print('')

        for i in range(3):
            item = portfolio_w_cash.iloc[i].name
            amount_krw = portfolio_w_cash.iloc[i, 0]
            print(
                style_terminal_text(
                    text=f"({amount_krw/cur_asset_value:>6,.2%})",
                    color='yellow',
                ),
                style_terminal_text(
                    text=f"{item}",
                    color='red',
                    style='bold'
                ),
                f"▸ {amount_krw:,.2f} 원"
            )

        print(
            style_terminal_text(
                text=f'\nCURRENT ASSET COMPONENTS',
                style='bold',
            )
        )

        print(
            style_terminal_text(
                text=f"({current_value/cur_asset_value:>6,.2%})",
                color='yellow',
            ),
            style_terminal_text(
                text='STOCK',
                color='red',
                style='bold'
            ),
            f"▸ {current_value:,.2f} 원"
        )

        print(
            style_terminal_text(
                text=f"({total_cash_value/cur_asset_value:>6,.2%})",
                color='yellow',
            ),
            style_terminal_text(
                text=f"{'CASH':>5}",
                color='red',
                style='bold'
            ),
            f"▸ {total_cash_value:,.2f} 원"
        )

        print('')
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
