#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import pandas as pd
import datetime
import random
from binance.client import Client
from binance.websockets import BinanceSocketManager


# In[ ]:


def get_supported_cryptos():
    """
    Signature: get_supported_cryptos() -> 'DataFrame'
    
    Docstring:
    Retrieves the supported list of cryptocurrencies.
    It makes use of Binance' API ('https://api.binance.com/api/v3/')
    
    Returns
    -------
    DataFrame

    Examples
    --------
    
    >>> get_supported_cryptos()
    """

    API_BASE = 'https://api.binance.com/api/v3/'
    x = []
    for i in requests.get(f'{API_BASE}exchangeInfo').json()['symbols']:
        x.append(i['symbol'])
    
    return(x)


# In[ ]:


def get_supported_cryptos_static():
    """
    Signature: get_supported_cryptos_static() -> 'DataFrame'
    
    Docstring:
    Retrieves the supported list of cryptocurrencies.
    This 'static' version loads the list from a .csv file.

    Returns
    -------
    DataFrame

    Examples
    --------
    
    >>> get_supported_cryptos_static()
    """
    x = pd.read_csv('project_files/crypto_list.csv')['0'].values.tolist()
    return(x)


# In[ ]:


def start_socket():
    """
    Signature: startsocket() -> 'BinanceSocketManager'
    
    Docstring:
    Initializes a Socket Manager to recieve real-time information from Binance.

    Returns
    -------
    BinanceSocketManager

    Examples
    --------
    
    >>> start_socket()
    """
   
    client = Client("", "")
    bm = BinanceSocketManager(client)
    bm.start()
    return(bm)


# In[ ]:


def close_socket(x):
    """
    Signature: close_socket()
    
    Docstring:
    Closes a socket to stop the real-time data fetching.

    Parameters
    ----------
    x : BinanceSocketManager
        An instance of a BinanceSocketManager.

    Examples
    --------
    
    >>> close_socket()
    """

    x.close()
    pass


# In[ ]:


def load_data_btc():
    """
    Signature: load_data_btc() --> DataFrame
    
    Docstring:
    Loads the .csv file corresponding to the BTCUSDT data for 1h candles.
    Changes the index to datetime, interpolates the null values created
    due to missing data for some hours.
    Creates 'average' column using high and low prices.
    Returns a DataFrame with everything.

    Example
    --------
    
    >>> load_data_btc()
    """

    # read from file
    df = pd.read_csv('data/BTCUSDT_1h.csv', parse_dates=['time'])
    
    # set index as datetime
    df.index = pd.DatetimeIndex(df.time)

    # drop the time which isn't needed anymore
    df = df.drop('time', axis=1)
    
    # IMPORTANT: assign a frequency to the index
    df = df.asfreq('1h')
    
    # creates 'average' column taking 'high' and 'low'
    df['average'] = (df.high + df.low)/2
    
    # make a subset of the whole data for simplicity
    df = df.copy().tail(2000)
    
    # interpolates nans for relevant columns
    for i in ['open', 'high', 'low', 'close', 'volume']:
        df[i] = df[i].interpolate(method='time')
    
    # returns DataFrame
    return(df)


# In[ ]:


def create_empty_realtime_df():
    """
    Signature: create_empty_realtime_df()
    
    Docstring:
    Creates an empty pandas DataFrame formatted with the necessary columns for real-time
    aggregation of financial data using a socket from Binance.

    Examples
    --------
    
    >>> create_empty_realtime_df()
    """
    
    x = pd.DataFrame(columns=['t','o','h','l','c','v','T','q','n','V','Q','B'])
    return(x)

