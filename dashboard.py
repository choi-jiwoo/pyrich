import numpy as np
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from pyrich import style
from pyrich.style import style_table
from pyrich.table import sort_table
from pyrich.asset import Asset
from pyrich.portfolio import Portfolio
from pyrich.dividend import Dividend
from pyrich.cash import Cash
from pyrich.visualization import draw_pie


pd.set_option('styler.format.precision', 2)
pd.set_option('styler.format.thousands', ',')

# Loading main page
portfolio = Portfolio('Choi Ji Woo', 'transaction')
st.title(f'Hello {portfolio.name} 👋🏼')

# Loding portfolio data
portfolio_table = portfolio.current_portfolio()
portfolio_value = portfolio.get_current_portfolio_value(portfolio_table)
investment_by_country = portfolio.get_investment_by_country(portfolio_table)
cash = Cash('cash')
cash_table = cash.record
total_cash = cash.get_total_cash_in_krw()
asset = Asset('current_asset')
current_asset = asset.record

# Sidebar component
with st.sidebar:
    # https://icons.getbootstrap.com/
    selected = option_menu(
        menu_title='Main Menu',
        options=[
            'Dashboard',
            'Portfolio',
            'My Asset',
            'Investment History',
            'Dividends History',
            'Transaction History',
            ], 
        icons=['house', 'stack', 'stack', 'stack', 'stack', 'stack'],  # change icon later
        menu_icon='list',
        default_index=0
    )

if selected == 'Dashboard':
    st.header(f'Hello {portfolio.name} 👋🏼')

    current_yield = portfolio_value['portfolio_gain'] / portfolio_value['invested_amount']
    color = '#fff'
    if current_yield < 0:
        color = '#a50e0e' # red
    elif current_yield > 0:
        color = '#137333' # green
    
    cur_asset = st.container()
    cur_asset.subheader('Current Asset Value')
    cur_asset_value = portfolio_value['current_value'] + total_cash.item()

    # Update current asset in the database
    portfolio.record_current_asset(cur_asset_value)

    cur_asset_text = ("<span style='font-weight: bold; font-size: 36px;'>"
                      f"{cur_asset_value:,.2f}원</span>")
    cur_asset.markdown(cur_asset_text, unsafe_allow_html=True)

    cur_investment, cur_cash = st.columns(2)
    cur_investment.subheader('Current Stock Value')
    cur_investment_text = ("<span style='font-weight: bold; font-size: 36px;'>"
                           f"{portfolio_value['current_value']:,.2f}원</span>"
                           f"<span style='color: {color};'>"
                           "<br>"
                           f"&nbsp;{portfolio_value['portfolio_gain']:,.2f}원"
                           f"&nbsp;({current_yield:,.2%})"
                           "</span>")
    cur_investment.markdown(cur_investment_text, unsafe_allow_html=True)

    cur_cash.subheader('Current Cash')
    cur_cash_text = ("<span style='font-weight: bold; font-size: 36px;'>"
                     f"{total_cash.item():,.2f}원</span>")
    cur_cash.markdown(cur_cash_text, unsafe_allow_html=True)
elif selected == 'Portfolio':
    st.header('Portfolio')

    portfolio_w_cash = portfolio.get_portfolio_w_cash(portfolio_table, total_cash.item()).to_frame(name='Values in KRW')
    portfolio_chart = draw_pie(portfolio_w_cash, values=portfolio_w_cash['Values in KRW'], names=portfolio_w_cash.index, title='Portfolio Item')
    st.write(portfolio_chart)

    st.subheader('Current portfolio')
    value_subset = ['day_change(%)', 'pct_gain(%)', 'total_gain']
    portfolio_table = sort_table(portfolio_table, by='pct_gain(%)', ascending=False)
    styled_portfolio_table = style_table(portfolio_table, style.style_change, value_subset)
    st.table(styled_portfolio_table)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Cash')
        cash_table = cash_table.set_index('currency')
        cash_table.drop(columns='id', inplace=True)
        st.table(cash_table)
    with col2:
        st.subheader('Investment')
        investment_by_country = sort_table(investment_by_country, by='total_gain', ascending=False)
        styled_investment_by_country = style_table(investment_by_country, style.style_change, ['total_gain'])
        st.table(styled_investment_by_country)
elif selected == 'My Asset':
    st.header('My Asset')

    # stock
    total_stock_value = pd.Series(portfolio_value['current_value'], index=['total_stock_value'], dtype=float)

    # total asset
    asset_table = pd.concat([total_cash, total_stock_value])
    total_asset = asset_table.agg({'total_asset': np.sum})
    total_asset_table = pd.concat([asset_table, total_asset]).to_frame(name='Values in KRW')
    total_asset_table.index = [idx.upper() for idx in total_asset_table.index]

    asset_chart = draw_pie(asset_table, values=asset_table.array, names=asset_table.index, title='Asset Ratio')
    st.write(asset_chart)
    st.table(total_asset_table)
elif selected == 'Investment History':
    st.header('Investment History')
    realized_gain = portfolio.get_realized_gain()
    realized_gain = sort_table(realized_gain, by='realized_gain', ascending=False)

    st.subheader('Realized Gain by Stock')
    styled_realized_gain = style_table(realized_gain, style.style_change, ['realized_gain'])
    st.table(styled_realized_gain)

    st.subheader('Realized Gain by Country')
    col_order = ['buy', 'sell', 'realized_gain', 'currency']
    realized_gain_by_country = realized_gain.groupby(['country', 'currency']).agg(np.sum).reset_index('currency')
    realized_gain_by_country = realized_gain_by_country[col_order]
    realized_gain_by_country = sort_table(realized_gain_by_country, by='realized_gain', ascending=False)
    styled_realized_gain_by_country = style_table(realized_gain_by_country, style.style_change, ['realized_gain'])
    st.table(styled_realized_gain_by_country)
elif selected == 'Dividends History':
    st.header('Dividends History')
    dividend = Dividend('dividend')
    dividend_history = dividend.record
    dividend_history.drop('id', axis=1, inplace=True)

    st.subheader('Total Dividends Received')
    total_dividends = dividend.get_total_dividends()
    total_dividends = {'Values in KRW': [total_dividends]}
    total_dividends_table = pd.DataFrame(total_dividends, index=['total_dividends'])
    total_dividends_table.index = [idx.upper() for idx in total_dividends_table.index]
    st.table(total_dividends_table)

    st.subheader('Total Dividends Received by Stock')
    dividends_by_stock = dividend.get_dividends_received_by_stock()
    st.table(dividends_by_stock)

    st.subheader('Dividends History')
    export_to_csv = dividend_history.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        'export to csv',
        export_to_csv,
        'dividend_history.csv',
        'text/csv',
    )
    st.dataframe(dividend_history)
elif selected == 'Transaction History':
    st.header('Transaction History')

    st.subheader('Total Transaction Amount')
    total_traded_amount = portfolio.get_total_traded_amount()
    total_traded_amount.index = [idx.upper() for idx in total_traded_amount.index]
    styled_total_traded_amount = style_table(total_traded_amount, style.style_neg_value , ['Values in KRW'])
    st.table(styled_total_traded_amount)

    st.subheader('Transaction History')
    transaction_history = portfolio.record
    transaction_history.drop('id', axis=1, inplace=True)
    styled_transaction_history = style_table(transaction_history, style.style_trade_type, ['type'])
    export_to_csv = transaction_history.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        'export to csv',
        export_to_csv,
        'transaction_history.csv',
        'text/csv',
    )
    st.table(styled_transaction_history)
