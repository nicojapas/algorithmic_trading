#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# code to plot charts and visualize results of the chosen strategy
# use plotly


# In[1]:


import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from datetime import timedelta, datetime


# In[2]:


def get_breaks(df):
    # get start and end date
    str_date = df['time'][df.shape[0]-1]
    end_date = df['time'][0]
    # convert strings into dates
    str_date = datetime.strptime(str_date, '%Y-%m-%d %H:%M:%S')
    end_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')


    def daterange(d1, d2):
        for n in range(int((d2 - d1).days)+1):
            yield d1 + timedelta(n)

    all_dates = []
    for dt in daterange(str_date, end_date):
        all_dates.append(dt.strftime("%Y-%m-%d"))

    break_dates = all_dates
    for i in range(data.shape[0]):
        d = datetime.strptime(data.iloc[i]['time'], '%Y-%m-%d %H:%M:%S')
        d = d.strftime("%Y-%m-%d")
        if d in break_dates:
            break_dates.remove(d)
    
    return(break_dates)


# In[5]:


def plot_candles(df,title,symbol):

    candlestick = go.Candlestick(
        x=df.open_time,
        open=df.open,
        high=df.high,
        low=df.low,
        close=df.close
    )
    fig = go.Figure(data=[candlestick])

    fig.update_layout(
        title=title,
        yaxis_title=symbol,
        template='plotly_dark'
    )
    # Default template: 'plotly'
    # Available templates:
    # ['ggplot2', 'seaborn', 'simple_white', 'plotly',
    # 'plotly_white', 'plotly_dark', 'presentation', 'xgridoff',
    # 'ygridoff', 'gridon', 'none']

    fig.update_xaxes(
        rangeslider_visible=False,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="hour", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        ),
#         hide x values (they are already in the volume plot)
        ticktext=[""],
        tickvals=[""]
    )
    fig.update_yaxes(
        type="log"
    )



    return(fig)


# In[ ]:


def plot_chart(data):
    """
    fñalsdnfñaldsnf
    """
    price = go.Candlestick(
        x=data.index,
        open=data.open,
        high=data.high,
        low=data.low,
        close=data.close,
    )

    volume = go.Scatter(
        x=data.index, y=data.volume
    )

    fig = make_subplots(rows=2, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.1,
                        subplot_titles=('', 'volume'),
                        row_width=[0.15, 0.45],
                       )

    fig.append_trace(price, 1, 1)
    fig.append_trace(volume, 2, 1)

    fig.update_layout(
        title="Bitcoin/TetherUS",
        yaxis_title="",
        template='plotly_dark',
        height=600,
    )
    fig.update_xaxes(
        rangeslider_visible=False,
    )
    fig.update_yaxes(
        type='log'
#         range=[0, 400000], row=2, col=1
    )
    fig['data'][1]['line']['color']='darkorange'

    figwid = go.FigureWidget(fig)
    return(figwid)


# In[1]:


def plot_realtime(data):
    candles = go.Candlestick(
            x=data.index,
            open=data.o,
            high=data.h,
            low=data.l,
            close=data.c,
    )
    fig = go.Figure(candles)
    
    fig.update_layout(
        title="1min candles",
        yaxis_title="",
        template='plotly_dark',
        height=400,
        width=500,
        
    )
    fig.update_xaxes(
        rangeslider_visible=False
    )
    fig.update_yaxes(
#         showticklabels=False,
    )

    figwid = go.FigureWidget(fig)
    return(figwid)


# In[ ]:


def gauge():
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = 420,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Speed", 'font': {'size': 24}},
        delta = {'reference': 400, 'increasing': {'color': "RebeccaPurple"}},
        gauge = {
            'axis': {'range': [None, 500], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 250], 'color': 'cyan'},
                {'range': [250, 400], 'color': 'royalblue'}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 490}}))

    fig.update_layout(paper_bgcolor = "lavender", font = {'color': "darkblue", 'family': "Arial"})

    return(fig)

