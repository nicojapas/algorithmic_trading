#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# standard libraries
import pandas as pd

# Binance wrapper libraries
from binance.client import Client
from binance.websockets import BinanceSocketManager


# In[ ]:


def web_socket_modularized():
    """
    Signature: web_socket() -> 'BinanceSocketManager'
    
    Docstring:
    Deals with real-time data.
    Also takes care of plotting.
    It makes use of Binance' API ('https://api.binance.com/api/v3/')
    
    Returns
    -------
    BinanceSocketManager

    Example
    -------
    
    >>> web_socket()
    """

    # real-time data and chart
    # have to be global for real-time interaction
    global rtdata
    global rtchart

    # initialize client without API keys, as they are not needed for now
    client = Client("", "")

    # this function runs every time the socket receives new data
    def process_message(x):
        global rtdata
        global rtchart

        # get the last minute from the existing data
        t1 = pd.to_datetime(rtdata.tail(1).index.values[0])
        
        # get the last minute from the new data
        t2 = pd.to_datetime(x['k']['t'], unit='ms')
        
        # convert the new data (kline tipe) into a dataframe
        new_df = pd.DataFrame([x['k']])
        
        # change the data type for t
        new_df['t'] = pd.to_datetime(new_df['t'], unit='ms')
        
        # change the data type for T
        new_df['T'] = pd.to_datetime(new_df['T'], unit='ms')
        
        # change to index into datetime with frequency = minutes
        new_df.index = pd.DatetimeIndex(new_df.t, freq='min')
        
        # drop the t column as it is now the index
        new_df = new_df.drop('t', axis=1)
        
        # reindex the dataframe using the existing data as a reference
        new_df.reindex(columns=rtdata.columns)

        # if the timestamps are different then append new values
        if t1 != t2:
            rtdata = pd.concat([rtdata, new_df], axis=0)
        
        #if it's still the same minute then update the value
        #this way we can see every change even before the candle is over
        else:
            rtdata.loc[rtdata.index[-1]] = new_df.loc[new_df.index[-1]]
        
        # update the chart
        rtchart.data[0].x=rtdata.index
        rtchart.data[0].open=rtdata.o
        rtchart.data[0].high=rtdata.h
        rtchart.data[0].low=rtdata.l
        rtchart.data[0].close=rtdata.c
        
        # recenter the plot leaving some space for predictions
        rtchart.update_xaxes(range=[rtdata.index[-16],rtdata.index[-1] + pd.Timedelta(minutes=5)])
        pass

    # get the last 1 hour of 1-minute candles data
    klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, "1 hour ago UTC")
    
    # convert to a dataframe using the appropriate format provided by the API documentation
    rtdata = pd.DataFrame(columns=['t','o','h','l','c','v','T','q','n','V','Q','B'])
    
    # concatenate every candle
    rtdata = pd.concat([rtdata, pd.DataFrame([i for i in klines], columns=rtdata.columns)], axis=0)
    
    # change the data type for t
    rtdata['t'] = pd.to_datetime(rtdata['t'], unit='ms')
    
    # change the data type for T
    rtdata['T'] = pd.to_datetime(rtdata['T'], unit='ms')
    
    # change to index into datetime with frequency = minutes
    rtdata.index = pd.DatetimeIndex(rtdata.t, freq='min')
    
    # drop the t column as it is now the index
    rtdata = rtdata.drop('t', axis=1)

    # initialize a socket manager
    bm = BinanceSocketManager(client)
    
    # start the kline socket to get bitcoin data in realtime
    bm.start_kline_socket("BTCUSDT", process_message)
    
    # adjust the plot's y-range
    rtchart.update_yaxes(range=[rtdata['l'].tail(15).min(),rtdata['h'].tail(15).max()])
    
    # return the socket manager
    return(bm)


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

