#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pandas as pd
import io
import requests
import time
import random


# In[3]:


# gets the hidden API keys
api_key = pd.read_csv('secrets.csv').api_key.to_string().split()[1]


# In[124]:


# gets data using user's parameters
def get_data(symbol, interval):
    """
    Signature: get_data(symbol, period) -> 'DataFrame'
    
    Docstring:
    Retrieves market data for the selected symbol and period.

    Parameters
    ----------
    symbol : str
        The name of the equity of your choice. For example: symbol=GOOGL.
    interval : str
        Time interval between two consecutive data points in the time series.
        The following values are supported: 1min, 5min, 15min, 30min, 60min.

    Returns
    -------
    DataFrame

    Examples
    --------
    
    >>> get_data('GOOGL', '60min')
    """

    # main url or alphavantage and selection of features from user
    BASE_URL = 'https://www.alphavantage.co/query?'
    q = {
        'function':'TIME_SERIES_INTRADAY_EXTENDED',
        'symbol':symbol,
        'interval':interval,
        'slice':'year1month1',
        'apikey':'KO4L9YMRD2VLJX8O'
    }

    df=pd.DataFrame()

    for y in range(1,3):
        for m in range(1,13):
            # create 'slices' of 1 month each. has to do with how the api functions
            q['slice'] = f'year{y}month{m}'

            # concatenate all user's selected values into one string
            q_str = "".join([i for i in [str(i) + "=" + str(q[i]) + "&" for i in q]])[:-1]

            # concatenate the base alphavantage url with the user's query
            url = BASE_URL + q_str
            print(url)
            
            # GET url
            response = requests.get(url)

            # read data into a pandas dataframe
            df=pd.concat([df, pd.read_csv(io.StringIO(response.content.decode('utf-8')))], axis=0)

            # because the free api has a limit of 5 calls per minute, we need to wait
            time.sleep(60/5)
            
    # returns a dataframe
    return(df)


# In[125]:


# auto complete function for stocks
def auto_complete_stocks(x):
    """
    Signature: auto_complete_stocks(str) -> 'json'
    
    Docstring:
    Makes use of the auto-completion function of Alpha Vantage API.
    It takes the user's input and returns a json with the coincidences.

    Parameters
    ----------
    symbol : str
        A string containing part of the symbol or description of the equity.
        For example 'amaz' would return the symbol and description for AMZN stocks, etc.

    Returns
    -------
    json
    """

    BASE_URL = 'https://www.alphavantage.co/query?'
    url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={x}&datatype=json&apikey={api_key}'
    response = requests.get(url).json()
    return(response)


# In[ ]:


# to fetch all updated stocks and ETFs supported
def get_supported_stocks():
    """
    Signature: get_supported_stocks() -> 'DataFrame'
    
    Docstring:
    Retrieves the supported list of stocks and ETFs from Alpha Vantage, using their API.
    See https://www.alphavantage.co/
    
    Returns
    -------
    DataFrame

    Examples
    --------
    
    >>> get_supported_stocks()
    """

    BASE_URL = 'https://www.alphavantage.co/query?'
    url = f'https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={api_key}'
    response = requests.get(url)
    x=pd.read_csv(io.StringIO(response.content.decode('utf-8')))
    return(x)


# In[ ]:


# to fetch all updated stocks and ETFs supported
# static version loading from .csv previously downloaded
def get_supported_stocks_static():
    """
    Signature: get_supported_stocks() -> 'DataFrame'
    
    Docstring:
    Retrieves the supported list of stocks and ETFs from Alpha Vantage, using their API.
    This 'static' version loads the list from a .csv file.
    
    Returns
    -------
    DataFrame

    Examples
    --------
    
    >>> get_supported_stocks()
    """

    x = pd.read_csv('data/stocks_etfs_list.csv')
    l1 = x['symbol'].to_list()
    l2 = x['name'].to_list()
    l3 = [str(i) + " - " + str(j) for i, j in zip(l1, l2)] 
    return(l1, l2, l3)

