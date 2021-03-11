#!/usr/bin/env python
# coding: utf-8

# In[1]:


# simple interface module using widgets


# In[1]:


import ipywidgets as widgets
import pandas as pd


# In[2]:


def build_panel(stocks_list=None, cryptos_list=None):
    """
    Docstring:
    Creates a series of widgets to enable user selection of cryptocurrencies or stocks,
    and the name and description of the instrument chosen.
    Returns 3 widget objects.

    Parameters
    ----------
    stocks_list : list
        A list with the available stocks.
    cryptos_list: list
        A list with the available cryptocurrencies.
    """
    # ticker needs to be global for interaction with main
    global ticker 
    
    # combobox to input stocks
    ticker = widgets.Combobox(
        value='',
        placeholder='',
        options=stocks_list[2],
        description='Ticker:',
        ensure_option=True,
        disabled=False,
        continuous_update=False
    )
    
    # combobox to chose the time period
    # for now it's fixed in 1 hour
    period = widgets.Combobox(
        value='1hour',
        placeholder='',
        options=['1hour', '1day'],
        description='Period:',
        ensure_option=True,
        disabled=False,
        continuous_update=False
    )
    
    # toggle button to choose either stocks or cryptocurrencies
    tgl_btns1 = widgets.ToggleButtons(
        options=['Stocks', 'Cryptos'],
        disabled=False,
        button_style='',
        tooltips=['Stocks and ETFs', 'Cryptocurrencies'],
    )
    
    # this function runs every time tgl_btns1 is clicked
    def on_tgl_btns1_clicked(value):
        # if the selection is inside the available stock list then update
        if value['new'] == 'Stocks':
            ticker.options = stocks_list[2]
            ticker.placeholder=''
            ticker.value = ''
        # if the selection is inside the available crypto list then update
        elif value['new'] == 'Cryptos':
            ticker.options = cryptos_list
            ticker.placeholder=''
            ticker.value = ''
        #if not, do nothing
        else:
            pass

    # observe toggle buttons for change of state
    tgl_btns1.observe(on_tgl_btns1_clicked, 'value')
    
    # return a tuple with the 3 widgets
    x = (ticker, period, tgl_btns1)
    
    return(x)


# In[ ]:


# def build_panel2(stocks, cryptos, chart,rtchart):

#     global ticker 
    
#     # all the supported stock and ETF symbols and descriptions into a list to use as options in the combobox
#     l_smb = stocks['symbol'].to_list()
#     l_dsc = stocks['name'].to_list()
#     l_stocks = [str(i) + " - " + str(j) for i, j in zip(l_smb, l_dsc)] 

#     ticker = widgets.Combobox(
#         value='SPY - S&P 500 ETF TRUST ETF',
#         placeholder='AAPL, SPY, MSFT, ...',
#         options=l_stocks,
#         description='Ticker:',
#         ensure_option=True,
#         disabled=False,
#         continuous_update=False
#     )
#     period = widgets.Combobox(
#         value='1hour',
#         placeholder='',
#         options=['1hour', '1day'],
#         description='Period:',
#         ensure_option=True,
#         disabled=False,
#         continuous_update=False
#     )

#     tgl_btns1 = widgets.ToggleButtons(
#         options=['Stocks', 'Cryptos'],
#         disabled=False,
#         button_style='',
#         tooltips=['Stocks and ETFs', 'Cryptocurrencies'],
#     )
    
#     def on_button_clicked(value):

#         if value['new'] == 'Stocks':
#             ticker.options = l_stocks
#             ticker.placeholder='AAPL, SPY, MSFT, ...'
#             ticker.value = 'SPY - S&P 500 ETF TRUST ETF'

#         elif value['new'] == 'Cryptos':
#             ticker.options = cryptos
#             ticker.placeholder='BTCUSDT, ETHUSDT, ...'
#             ticker.value = 'BTCUSDT - Bitcoin USDTether (Binance)'
#         else:
#             pass
# #         print(value)
    
#     tgl_btns1.observe(on_button_clicked, 'value')
    
#     x = widgets.HBox([ticker, period, tgl_btns1])
#     return(x)

