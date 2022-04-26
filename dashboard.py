import streamlit as st
from streamlit_option_menu import option_menu
from pyrich.portfolio import Portfolio


portfolio = Portfolio('Choi Ji Woo')
st.title(f'Hello {portfolio.name} 👋🏼')

with st.sidebar:
    # https://icons.getbootstrap.com/
    selected = option_menu(
        menu_title='Main Menu',
        options=[
            'Dashboard',
            'Portfolio',
            'My Asset',
            'Transaction History',
            ], 
        icons=['house', 'stack', 'stack', 'stack'],
        menu_icon='list',
        default_index=0
    )

if selected == 'Dashboard':
    st.header('Dashboard')    
elif selected == 'Portfolio':
    st.header('Portfolio')
elif selected == 'My Asset':
    st.header('My Asset')
elif selected == 'Transaction History':
    st.header('Transaction History')
    transaction_history = portfolio.transaction_history('transaction')
    st.dataframe(transaction_history)

    st.header('Dividend History')
    dividend_history = portfolio.transaction_history('dividend')
    st.dataframe(dividend_history)