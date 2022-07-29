from datetime import datetime
import os
from pyrich.database import PostgreSQL
from pyrich import parse
from pyrich.transaction import Transaction
from pyrich.forex import get_usd_to_krw
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
from pyrich import stock


def run():
    # Load arguments
    parser = parse.set_args()
    args = parser.parse_args()
    options = vars(args)

    if options['summary']:
        portfolio = Portfolio('Choi Ji Woo', 'transaction')
        cash = Cash('cash')
        asset = Asset('current_asset')
        
        portfolio_table, portfolio_value = portfolio_data(portfolio)
        total_cash = cash_data(cash)
        total_cash_value = total_cash.item()
        cur_asset_value = current_asset_data(portfolio_value['current_value'], total_cash_value)
        asset.record_current_asset(cur_asset_value)
        usd_to_krw = portfolio.forex_usd_to_won

        today = datetime.today()
        today_string = today.strftime('%Y %B %d %A, %X')
        print(style_terminal_text(
                text=f"\n{today_string}\n",
                color='magenta',
                style='bold'
            )
        )

        portfolio_table.reset_index('symbol', inplace=True)
        stocks = portfolio_table[['symbol', 'current_value', 'invested_amount']].values
        gain = portfolio_value['portfolio_gain']
        invested = portfolio_value['invested_amount']
        _yield = current_yield(gain, invested)
        current_value = portfolio_value['current_value']

        # Financial Summary Section
        print(style_terminal_text(
            text='FINANCIAL SUMMARY',
            style='bold',
        ))

        print(
            style_terminal_text(
                text=f"{'TOTAL ASSET':<14}",
                color='green',
                style='bold',
            ),
            "▸",
            style_terminal_text(
                text=f"{cur_asset_value:,.2f} 원",
                style='bold'
            ),
        )

        print(
            style_terminal_text(
                text=f"{'TOTAL CASH':<14}",
                color='green',
                style='bold'
            ),
            "▸",
            f"{total_cash_value:,.2f} 원"
        )

        stock_value_label = (
            style_terminal_text(
                text=f"{'STOCK VALUE':<15}",
                color='green',
                style='bold',
            ) +
            "▸"
        )
        
        ANSI_STYLE_CODE_LEN = 12
        stock_value_label_len = len(stock_value_label) - ANSI_STYLE_CODE_LEN
        print(
            stock_value_label,
            style_terminal_text(
                text=f"{current_value:,.2f} 원",
            )
        )
        total_gain_text = f"{gain:,.2f} ({_yield:,.2f} %)"
        right_align_width = stock_value_label_len + len(total_gain_text)
        print(
            style_terminal_text(
                text=f"{total_gain_text:>{right_align_width}}",
                color=style_change(_yield, 'terminal'),
            )
        )

        print(style_terminal_text(
                text=f"{'TOTAL INVESTED':<14}",
                color='green',
                style='bold',
            ),
            "▸",
            style_terminal_text(
                text=f"{invested:,.2f} 원",
            ),
        )

        print('')

        # Portfolio Components Section
        print(
            style_terminal_text(
                text='PORTFOLIO COMPONENTS',
                style='bold',
            ),
        )

        for i in stocks:
            name = i[0]
            current_stock_value = i[1]
            invested = i[2]
            # current_stock_value = i[1] * usd_to_krw
            # invested = i[2] * usd_to_krw
            gain = current_stock_value - invested
            stock_yield = current_yield(gain, invested)

            symbol_label = (
                f"({current_stock_value/current_value:,.2%})" +
                " " +
                style_terminal_text(
                    text=name,
                    color='green',
                    style='bold'
                ) +
                " ▸"
            )
            symbol_label_len = len(symbol_label) - ANSI_STYLE_CODE_LEN
            print(symbol_label, f"{current_stock_value:,.2f} 원")
            stock_gain_text = f"{gain:,.2f} ({stock_yield:,.2f} %)"
            right_align_width = symbol_label_len + len(stock_gain_text)
            print(
                style_terminal_text(
                    text=f"{stock_gain_text:>{right_align_width}}",
                    color=style_change(stock_yield, 'terminal'),
                )
            )
        
        print('')

        # Asset Components Section
        print(
            style_terminal_text(
                text='ASSET COMPONENTS',
                style='bold',
            ),
        )

        print(
            style_terminal_text(
                text='STOCK',
                color='green',
                style='bold'
            ),
            "▸",
            style_terminal_text(
                text=f"{current_value/cur_asset_value:,.2%}",
            ),
        )

        print(
            style_terminal_text(
                text=f"{'CASH':<5}",
                color='green',
                style='bold'
            ),
            "▸",
            style_terminal_text(
                text=f"{total_cash_value/cur_asset_value:,.2%}",
            ),
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

    # Search price
    if options['price']:
        price_record = options['price']
        price_record = [item.upper() for item in price_record]
        price_info = stock.get_current_price(*price_record)
        stock_ = price_record[0]
        current_price = price_info['c']
        day_change = price_info['dp']
        print(
            style_terminal_text(
                text=stock_,
                color='green',
                style='bold'
            ),
            "▸",
            f"{current_price}",
            style_terminal_text(
                text=f"({day_change:,.2f} %)",
                color=style_change(day_change, 'terminal'),
            )
        )
        return

    # Record transaction
    if options['dividend'] is None:
        headers = ['date', 'country', 'type', 'symbol', 'quantity', 'price']
        transaction = Transaction(options['transaction'], headers=headers)
        transaction_record = transaction.record
        transaction_record['total_price_paid'] = transaction_record['quantity'] * transaction_record['price']
        transaction_record['total_price_paid_in_krw'] = transaction_record['total_price_paid']
        if transaction_record['country'] == 'USA':
            usd_to_krw = get_usd_to_krw()
            transaction_record['total_price_paid_in_krw'] *= usd_to_krw
        db.insert('transaction', transaction_record)
    else:
        headers = ['date', 'symbol', 'dividend', 'currency']
        dividends = Transaction(options['dividend'], headers=headers)
        dividends_record = dividends.record
        db.insert('dividend', dividends_record)
