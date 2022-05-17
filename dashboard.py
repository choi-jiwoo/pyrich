import streamlit as st
from streamlit_option_menu import option_menu
from pyrich.portfolio import Portfolio
from pyrich.dividend import Dividend
from pyrich.cash import Cash


# Loading main page
portfolio = Portfolio('Choi Ji Woo', 'transaction')
st.title(f'Hello {portfolio.name} 👋🏼')

# Loding portfolio data
portfolio_table = portfolio.current_portfolio()
portfolio_value = portfolio.get_current_portfolio_value(portfolio_table)

# Sidebar component
with st.sidebar:
    # https://icons.getbootstrap.com/
    selected = option_menu(
        menu_title='Main Menu',
        options=[
            'Dashboard',
            'Portfolio',
            'My Asset',
            'Transaction History',
            'Dividend History',
            ], 
        icons=['house', 'stack', 'stack', 'stack', 'stack'],
        menu_icon='list',
        default_index=0
    )

if selected == 'Dashboard':
    st.header('Dashboard')
elif selected == 'Portfolio':
    st.header('Portfolio')
    st.subheader('Portfolio Value')

    current_yield = portfolio_value['portfolio_gain'] / portfolio_value['invested_amount']
    color = '#fff'
    if current_yield < 0:
        color = '#a50e0e' # red
    elif current_yield > 0:
        color = '#137333' # green

    current_value_text = ("<span style='font-weight: bold; font-size: 42px;'>"
                          f"{portfolio_value['current_value']:,.2f}원"
                          "</span>"
                          f"<span style='color: {color};'>"
                          f"&nbsp;{portfolio_value['portfolio_gain']:,.2f}원"
                          f"&nbsp;({current_yield:,.2%})"
                          "</span>")
    st.markdown(current_value_text, unsafe_allow_html=True)

    st.subheader('Current portfolio')
    st.table(portfolio_table)
elif selected == 'My Asset':
    st.header('My Asset')
    col1, col2 = st.columns(2)
    cash = Cash('cash')
    cash_table = cash.record
    with col1:
        st.table(cash_table)
    with col2:
        with st.form('Current Cash', clear_on_submit=True):
            cash_amount = st.text_input('Current Cash', placeholder=0)
            currency = st.radio('Currency', ['KRW', 'USD'])
            submitted = st.form_submit_button('Submit')
            if submitted:
                cash.update_current_cash('amount', cash_amount, currency)
                st.experimental_rerun()

elif selected == 'Transaction History':
    st.header('Transaction History')
    transaction_history = portfolio.record
    st.dataframe(transaction_history)
elif selected == 'Dividend History':
    st.header('Dividend History')
    dividend = Dividend('dividend')
    dividend_history = dividend.record
    st.dataframe(dividend_history)