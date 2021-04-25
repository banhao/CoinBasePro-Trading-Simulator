#!/usr/bin/env python3

# Author: banhao@gmail.com
# Version: 1.4
# Issue Date: April 25, 2021
# Release Note: rearrange the plot windows, plot1 and plot2 can display on the same screen and use half of the screen. Add "close_plot_second" parameter, if "close_plot_second" = 0 plots will close immediately. if you want to close plot windows manually please uncomment the "input("Press [enter] to continue.")" 


import json, hmac, hashlib, time, requests, base64, collections
from requests.auth import AuthBase
from datetime import datetime, timedelta, date
from tqdm import tqdm
import pandas as pd
import numpy as np
import dateutil.parser as dp
import matplotlib
import matplotlib.pyplot as plt
import mplfinance as mpf
import pylab
import ta
import xml.etree.ElementTree as ET
from ta import add_all_ta_features
from ta.utils import dropna
from pandas import DataFrame
from math import isnan
from xml.dom import minidom
from variable import *


# Create custom authentication for Exchange
class CoinbaseExchangeAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        if type(request.body) is bytes:
                message = (timestamp + request.method + request.path_url + (request.body.decode('utf-8') or '')).encode('utf-8')
        else:
                message = (timestamp + request.method + request.path_url + (request.body or '')).encode('utf-8')

        hmac_key = base64.b64decode(bytes(self.secret_key, 'utf-8'))
        signature = hmac.new(hmac_key, message, hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest())

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request


def min_max_price(Long_Term_Indicator_days, id):
    global min_max_list
    low_price_list = []
    high_price_list = []
    regress_history_data_price = requests.get(api_url + 'products/'+id+'/candles?start='+start_datetime+'&end='+end_datetime+'&granularity='+str(Long_Term_Indicator_days_granularity), auth=auth)
    time.sleep(1)
    if regress_history_data_price.json():
        for i in range(len(regress_history_data_price.json())):
            high_price_list.append([regress_history_data_price.json()[i][0], regress_history_data_price.json()[i][2]])
            low_price_list.append([regress_history_data_price.json()[i][0], regress_history_data_price.json()[i][1]])
        max_value, max_index = max((row[1], i)
                           for i, row in enumerate(high_price_list))
        #print(id, len(regress_history_data_price.json()), "days hightest price", datetime.utcfromtimestamp(high_price_list[max_index][0]).isoformat(), max_value)
        min_value, min_index = min((row[1], i)
                           for i, row in enumerate(low_price_list))
        #print(id, len(regress_history_data_price.json()), "days lowest price", datetime.utcfromtimestamp(low_price_list[min_index][0]).isoformat(), min_value)
    min_max_list.append([id, len(regress_history_data_price.json()), datetime.utcfromtimestamp(high_price_list[max_index][0]).__format__('%Y-%m-%d %H:%M:%S'), max_value, datetime.utcfromtimestamp(low_price_list[min_index][0]).__format__('%Y-%m-%d %H:%M:%S'), min_value])
    if ((datetime.utcfromtimestamp(current_datetime.json()['epoch']) - datetime.utcfromtimestamp(high_price_list[max_index][0])).days) * 10 <= (datetime.utcfromtimestamp(current_datetime.json()['epoch']) - datetime.utcfromtimestamp(low_price_list[min_index][0])).days :
        sell_signal = False
    else:
        sell_signal = True
    print('%12s' % id," | ", '%4s' % len(regress_history_data_price.json())," | hightest price date:",datetime.utcfromtimestamp(high_price_list[max_index][0]).__format__('%Y-%m-%d %H:%M:%S')," | ", '%12s' % max_value," | lowest price date:", datetime.utcfromtimestamp(low_price_list[min_index][0]).__format__('%Y-%m-%d %H:%M:%S')," | ", '%12s' % min_value," | sell signal:", '%8s' % sell_signal)


def plotdata_Max_Min(long_term_simulation_data):
    sigPriceBuy = []
    sigPriceSell = []
    highPriceDate = min_max_list[i][2]
    highPrice = min_max_list[i][3]
    lowPriceDate = min_max_list[i][4]
    lowPrice = min_max_list[i][5]
    for j in list(long_term_simulation_data.index):
        if str(j) == str(highPriceDate) and str(j) == str(lowPriceDate):
            sigPriceBuy.append(lowPrice)
            sigPriceSell.append(highPrice)
        elif str(j) == str(highPriceDate):
            sigPriceBuy.append(np.nan)
            sigPriceSell.append(highPrice)
        elif str(j) == str(lowPriceDate):
            sigPriceBuy.append(lowPrice)
            sigPriceSell.append(np.nan)
        else:
            sigPriceBuy.append(np.nan)
            sigPriceSell.append(np.nan)
    return(sigPriceBuy, sigPriceSell)


def plotdata_Prediction_Simulate(short_term_simulation_data):
    global buy_indicator,sell_indicator
    buy_indicator = long_term_simulation_data[long_term_simulation_data['Buy_signal_Price'].notnull()]
    sell_indicator = long_term_simulation_data[long_term_simulation_data['Sell_Signal_price'].notnull()]
    buy_indicator = buy_indicator[buy_indicator['RSI14'].notnull()]
    sell_indicator = sell_indicator[sell_indicator['RSI14'].notnull()]
    if len(buy_indicator) != 0 and len(sell_indicator) != 0:
        buy_indicator = buy_indicator.loc[ [buy_indicator['RSI7'].idxmin()],['MACD','MACD_DIFF','MACD_SIGNAL','RSI7','RSI14','ARRON_DOWN','ARRON_UP','ARRON','EMA','WMA'] ]
        sell_indicator = sell_indicator.loc[ [sell_indicator['High'].idxmax()],['MACD','MACD_DIFF','MACD_SIGNAL','RSI7','RSI14','ARRON_DOWN','ARRON_UP','ARRON','EMA','WMA'] ]
    elif len(buy_indicator) != 0 and len(sell_indicator) == 0:
        buy_indicator = buy_indicator.loc[ [buy_indicator['RSI7'].idxmin()],['MACD','MACD_DIFF','MACD_SIGNAL','RSI7','RSI14','ARRON_DOWN','ARRON_UP','ARRON','EMA','WMA'] ]
        sell_indicator = []
    else:
        buy_indicator = []
        sell_indicator = []
    sigPriceBuy = []
    sigPriceSell = []
    flag = -1
    buy_price = 0
    if len(buy_indicator) != 0 and len(sell_indicator) != 0:
        for j in list(short_term_simulation_data.index):
            if np.isnan(short_term_simulation_data['CCI'][j]):
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)
            else:
                if short_term_simulation_data['Close'][j] > short_term_simulation_data['Open'][j] and short_term_simulation_data['Close'][j] < short_term_simulation_data['BOLLINGER_LBAND'][j] and short_term_simulation_data['CCI'][j] < -100:
                    if flag != 1:
                        sigPriceBuy.append(short_term_simulation_data['Close'][j])
                        sigPriceSell.append(np.nan)
                        flag = 1
                        buy_price = short_term_simulation_data['Close'][j]
                    else:
                        sigPriceBuy.append(np.nan)
                        sigPriceSell.append(np.nan)
                elif short_term_simulation_data['Close'][j] < short_term_simulation_data['Open'][j] and short_term_simulation_data['Open'][j] < short_term_simulation_data['BOLLINGER_LBAND'][j] and short_term_simulation_data['CCI'][j] < -100:
                    if flag != 1:
                        sigPriceBuy.append(short_term_simulation_data['Close'][j])
                        sigPriceSell.append(np.nan)
                        flag = 1
                        buy_price = short_term_simulation_data['Close'][j]
                    else:
                        sigPriceBuy.append(np.nan)
                        sigPriceSell.append(np.nan)
                elif short_term_simulation_data['Close'][j] < short_term_simulation_data['Open'][j] and short_term_simulation_data['Close'][j] > short_term_simulation_data['BOLLINGER_HBAND'][j] and short_term_simulation_data['CCI'][j] > 100 and short_term_simulation_data['Close'][j] >= buy_price*profit_rate and buy_price != 0:
                    if flag != 0:
                        sigPriceBuy.append(np.nan)
                        sigPriceSell.append(short_term_simulation_data['Close'][j])
                        flag = 0
                        buy_price = 0
                    else:
                        sigPriceBuy.append(np.nan)
                        sigPriceSell.append(np.nan)
                elif short_term_simulation_data['Close'][j] > short_term_simulation_data['Open'][j] and short_term_simulation_data['Open'][j] > short_term_simulation_data['BOLLINGER_HBAND'][j] and short_term_simulation_data['CCI'][j] > 100 and short_term_simulation_data['Close'][j] >= buy_price*profit_rate and buy_price != 0:
                    if flag != 0:
                        sigPriceBuy.append(np.nan)
                        sigPriceSell.append(short_term_simulation_data['Close'][j])
                        flag = 0
                        buy_price = 0
                    else:
                        sigPriceBuy.append(np.nan)
                        sigPriceSell.append(np.nan)
                else:
                    sigPriceBuy.append(np.nan)
                    sigPriceSell.append(np.nan)
    else:
        for j in list(short_term_simulation_data.index):
            sigPriceBuy.append(np.nan)
            sigPriceSell.append(np.nan)
    return(sigPriceBuy, sigPriceSell)


def plotdata_Buy_Sell_indicator_simulate(long_term_simulation_data):
    sigPriceBuy = []
    sigPriceSell = []
    k = 0
    l = k
    init_buy_price = long_term_simulation_data['Close'][k]
    sigPriceBuy.append(long_term_simulation_data['Close'][k])
    sigPriceSell.append(np.nan)
    k += 1
    #print(len(long_term_simulation_data))
    while k < len(long_term_simulation_data):
        if long_term_simulation_data['Close'][k] >= init_buy_price*profit_rate:
            if k < (len(long_term_simulation_data)-1):
                init_buy_price = long_term_simulation_data['Close'][k+1]
            l = k+1
            sigPriceBuy.append(np.nan)
            sigPriceSell.append(long_term_simulation_data['Close'][k])
            if k < (len(long_term_simulation_data)-1):
                sigPriceBuy.append(long_term_simulation_data['Close'][k+1])
                sigPriceSell.append(np.nan)
            k += 1
        elif long_term_simulation_data['Close'][k] < init_buy_price:
            sigPriceBuy[l] = np.nan
            init_buy_price = long_term_simulation_data['Close'][k]
            sigPriceBuy.append(long_term_simulation_data['Close'][k])
            sigPriceSell.append(np.nan)
            l = k
        else:
            sigPriceBuy.append(np.nan)
            sigPriceSell.append(np.nan)
        k += 1
        #print(sigPriceBuy)
        #print(sigPriceSell)
    if np.count_nonzero(~np.isnan(sigPriceBuy)) > np.count_nonzero(~np.isnan(sigPriceSell)):
        sigPriceBuy.reverse()
        sigPriceBuy[sigPriceBuy.index(next(filter(lambda x: not isnan(x), sigPriceBuy)))] = np.nan
        sigPriceBuy.reverse()
    return(sigPriceBuy, sigPriceSell)


def draw_Buy_Sell_indicator_simulate(buy_sell,id):
    if np.count_nonzero(~np.isnan(buy_sell[0])) != 0 and np.count_nonzero(~np.isnan(buy_sell[1])) == 0:
        TA_plot = [ mpf.make_addplot(long_term_simulation_data['Min_signal_Price'], type='scatter', markersize=100, marker=r'$\Uparrow$', color = 'blue'),
            mpf.make_addplot(long_term_simulation_data['Max_Signal_price'], type='scatter', markersize=100, marker=r'$\Downarrow$', color = 'blue'),
            mpf.make_addplot(long_term_simulation_data['Buy_signal_Price'], type='scatter', markersize=50, marker=r'$\bigtriangleup$', color = 'red'),
            #mpf.make_addplot(long_term_simulation_data['Sell_Signal_price'], type='scatter', markersize=50, marker=r'$\bigtriangledown$', color = 'green'),
            mpf.make_addplot(long_term_simulation_data['EMA'], color = 'orange', linestyle ='dotted'), #mpf.make_addplot(long_term_simulation_data['WMA'], color = 'purple', linestyle ='dotted'),
            mpf.make_addplot(long_term_simulation_data['SMA5'], color = 'blue'),mpf.make_addplot(long_term_simulation_data['SMA10'], color = 'Orange'),mpf.make_addplot(long_term_simulation_data['SMA20'], color = 'Green'),
            mpf.make_addplot(long_term_simulation_data['BOLLINGER_HBAND'], color = 'green', linestyle ='-.'),mpf.make_addplot(long_term_simulation_data['BOLLINGER_LBAND'], color = 'red', linestyle ='-.'),mpf.make_addplot(long_term_simulation_data['BOLLINGER_MAVG'], color = 'Fuchsia'),
            mpf.make_addplot(cci, panel=2, ylabel='CCI'),
            mpf.make_addplot(macd['MACD_DIFF'], type='bar', panel=3, ylabel='MACD', alpha=1,secondary_y=False),
            mpf.make_addplot(macd['MACD'],panel=3,color='fuchsia',secondary_y=True),
            mpf.make_addplot(macd['MACD_SIGNAL'],panel=3,color='blue',secondary_y=True),
            mpf.make_addplot(aroon, panel=4, ylabel='AROON'), mpf.make_addplot(rsi['RSI7'], panel=5, ylabel='RSI',color = 'black'), mpf.make_addplot(rsi['RSI14'], panel=5, ylabel='RSI',color = 'red')
        ]
        ymin = df.loc[df['Low'].idxmin()]['Low']*0.95
        ymax = df.loc[df['High'].idxmax()]['High']*1.05
        mpf.plot( df, type='candle', style='yahoo', addplot=TA_plot, title=id, figscale=1.0, volume=True, ylim=(ymin,ymax), panel_ratios=(4,1),returnfig=True)
        fm = plt.get_current_fig_manager()
        fm.window.setGeometry(10,30,int((screen_width-30)/2),int(screen_height/2))
        plt.ion()
        plt.show()
        plt.draw()
        plt.pause(1)
    elif np.count_nonzero(~np.isnan(buy_sell[0])) == 0 and np.count_nonzero(~np.isnan(buy_sell[1])) != 0:
        TA_plot = [ mpf.make_addplot(long_term_simulation_data['Min_signal_Price'], type='scatter', markersize=100, marker=r'$\Uparrow$', color = 'blue'),
            mpf.make_addplot(long_term_simulation_data['Max_Signal_price'], type='scatter', markersize=100, marker=r'$\Downarrow$', color = 'blue'),
            #mpf.make_addplot(long_term_simulation_data['Buy_signal_Price'], type='scatter', markersize=50, marker=r'$\bigtriangleup$', color = 'red'),
            mpf.make_addplot(long_term_simulation_data['Sell_Signal_price'], type='scatter', markersize=50, marker=r'$\bigtriangledown$', color = 'green'),
            mpf.make_addplot(long_term_simulation_data['EMA'], color = 'orange', linestyle ='dotted'), #mpf.make_addplot(long_term_simulation_data['WMA'], color = 'purple', linestyle ='dotted'),
            mpf.make_addplot(long_term_simulation_data['SMA5'], color = 'blue'),mpf.make_addplot(long_term_simulation_data['SMA10'], color = 'Orange'),mpf.make_addplot(long_term_simulation_data['SMA20'], color = 'Green'),
            mpf.make_addplot(long_term_simulation_data['BOLLINGER_HBAND'], color = 'green', linestyle ='-.'),mpf.make_addplot(long_term_simulation_data['BOLLINGER_LBAND'], color = 'red', linestyle ='-.'),mpf.make_addplot(long_term_simulation_data['BOLLINGER_MAVG'], color = 'Fuchsia'),
            mpf.make_addplot(cci, panel=2, ylabel='CCI'),
            mpf.make_addplot(macd['MACD_DIFF'], type='bar', panel=3, ylabel='MACD', alpha=1,secondary_y=False),
            mpf.make_addplot(macd['MACD'],panel=3,color='fuchsia',secondary_y=True),
            mpf.make_addplot(macd['MACD_SIGNAL'],panel=3,color='blue',secondary_y=True),
            mpf.make_addplot(aroon, panel=4, ylabel='AROON'), mpf.make_addplot(rsi['RSI7'], panel=5, ylabel='RSI',color = 'black'), mpf.make_addplot(rsi['RSI14'], panel=5, ylabel='RSI',color = 'red')
        ]
        ymin = df.loc[df['Low'].idxmin()]['Low']*0.95
        ymax = df.loc[df['High'].idxmax()]['High']*1.05
        mpf.plot( df, type='candle', style='yahoo', addplot=TA_plot, title=id, figscale=1.0, volume=True, ylim=(ymin,ymax), panel_ratios=(4,1),returnfig=True)
        fm = plt.get_current_fig_manager()
        fm.window.setGeometry(10,30,int((screen_width-30)/2),int(screen_height/2))
        plt.ion()
        plt.show()
        plt.draw()
        plt.pause(1)
    elif np.count_nonzero(~np.isnan(buy_sell[0])) == 0 and np.count_nonzero(~np.isnan(buy_sell[1])) == 0:
        TA_plot = [ mpf.make_addplot(long_term_simulation_data['Min_signal_Price'], type='scatter', markersize=100, marker=r'$\Uparrow$', color = 'blue'),
            mpf.make_addplot(long_term_simulation_data['Max_Signal_price'], type='scatter', markersize=100, marker=r'$\Downarrow$', color = 'blue'),
            #mpf.make_addplot(long_term_simulation_data['Buy_signal_Price'], type='scatter', markersize=50, marker=r'$\bigtriangleup$', color = 'red'),
            #mpf.make_addplot(long_term_simulation_data['Sell_Signal_price'], type='scatter', markersize=50, marker=r'$\bigtriangledown$', color = 'green'),
            mpf.make_addplot(long_term_simulation_data['EMA'], color = 'orange', linestyle ='dotted'), #mpf.make_addplot(long_term_simulation_data['WMA'], color = 'purple', linestyle ='dotted'),
            mpf.make_addplot(long_term_simulation_data['SMA5'], color = 'blue'),mpf.make_addplot(long_term_simulation_data['SMA10'], color = 'Orange'),mpf.make_addplot(long_term_simulation_data['SMA20'], color = 'Green'),
            mpf.make_addplot(long_term_simulation_data['BOLLINGER_HBAND'], color = 'green', linestyle ='-.'),mpf.make_addplot(long_term_simulation_data['BOLLINGER_LBAND'], color = 'red', linestyle ='-.'),mpf.make_addplot(long_term_simulation_data['BOLLINGER_MAVG'], color = 'Fuchsia'),
            mpf.make_addplot(cci, panel=2, ylabel='CCI'),
            mpf.make_addplot(macd['MACD_DIFF'], type='bar', panel=3, ylabel='MACD', alpha=1,secondary_y=False),
            mpf.make_addplot(macd['MACD'],panel=3,color='fuchsia',secondary_y=True),
            mpf.make_addplot(macd['MACD_SIGNAL'],panel=3,color='blue',secondary_y=True),
            mpf.make_addplot(aroon, panel=4, ylabel='AROON'), mpf.make_addplot(rsi['RSI7'], panel=5, ylabel='RSI',color = 'black'), mpf.make_addplot(rsi['RSI14'], panel=5, ylabel='RSI',color = 'red')
        ]
        ymin = df.loc[df['Low'].idxmin()]['Low']*0.95
        ymax = df.loc[df['High'].idxmax()]['High']*1.05
        mpf.plot( df, type='candle', style='yahoo', addplot=TA_plot, title=id, figscale=1.0, volume=True, ylim=(ymin,ymax), panel_ratios=(4,1),returnfig=True)
        fm = plt.get_current_fig_manager()
        fm.window.setGeometry(10,30,int((screen_width-30)/2),int(screen_height/2))
        plt.ion()
        plt.show()
        plt.draw()
        plt.pause(1)
    else:
        TA_plot = [ mpf.make_addplot(long_term_simulation_data['Min_signal_Price'], type='scatter', markersize=100, marker=r'$\Uparrow$', color = 'blue'),
            mpf.make_addplot(long_term_simulation_data['Max_Signal_price'], type='scatter', markersize=100, marker=r'$\Downarrow$', color = 'blue'),
            mpf.make_addplot(long_term_simulation_data['Buy_signal_Price'], type='scatter', markersize=50, marker=r'$\bigtriangleup$', color = 'red'),
            mpf.make_addplot(long_term_simulation_data['Sell_Signal_price'], type='scatter', markersize=50, marker=r'$\bigtriangledown$', color = 'green'),
            mpf.make_addplot(long_term_simulation_data['EMA'], color = 'orange', linestyle ='dotted'), #mpf.make_addplot(long_term_simulation_data['WMA'], color = 'purple', linestyle ='dotted'),
            mpf.make_addplot(long_term_simulation_data['SMA5'], color = 'blue'),mpf.make_addplot(long_term_simulation_data['SMA10'], color = 'Orange'),mpf.make_addplot(long_term_simulation_data['SMA20'], color = 'Green'),
            mpf.make_addplot(long_term_simulation_data['BOLLINGER_HBAND'], color = 'green', linestyle ='-.'),mpf.make_addplot(long_term_simulation_data['BOLLINGER_LBAND'], color = 'red', linestyle ='-.'),mpf.make_addplot(long_term_simulation_data['BOLLINGER_MAVG'], color = 'Fuchsia'),
            mpf.make_addplot(cci, panel=2, ylabel='CCI'),
            mpf.make_addplot(macd['MACD_DIFF'], type='bar', panel=3, ylabel='MACD', alpha=1,secondary_y=False),
            mpf.make_addplot(macd['MACD'],panel=3,color='fuchsia',secondary_y=True),
            mpf.make_addplot(macd['MACD_SIGNAL'],panel=3,color='blue',secondary_y=True),
            mpf.make_addplot(aroon, panel=4, ylabel='AROON'), mpf.make_addplot(rsi['RSI7'], panel=5, ylabel='RSI',color = 'black'), mpf.make_addplot(rsi['RSI14'], panel=5, ylabel='RSI',color = 'red')
        ]
        ymin = df.loc[df['Low'].idxmin()]['Low']*0.95
        ymax = df.loc[df['High'].idxmax()]['High']*1.05
        mpf.plot( df, type='candle', style='yahoo', addplot=TA_plot, title=id, figscale=1.0, volume=True, ylim=(ymin,ymax), panel_ratios=(4,1),returnfig=True)
        fm = plt.get_current_fig_manager()
        fm.window.setGeometry(10,30,int((screen_width-30)/2),int(screen_height/2))
        plt.ion()
        plt.show()
        plt.draw()
        plt.pause(1)


def draw_Prediction_Simulate(buy_sell,id):
    if np.count_nonzero(~np.isnan(buy_sell[0])) != 0 and np.count_nonzero(~np.isnan(buy_sell[1])) == 0:
        TA_plot = [ #mpf.make_addplot(short_term_simulation_data['Min_signal_Price'], type='scatter', markersize=100, marker=r'$\Uparrow$', color = 'blue'),
            #mpf.make_addplot(short_term_simulation_data['Max_Signal_price'], type='scatter', markersize=100, marker=r'$\Downarrow$', color = 'blue'),
            mpf.make_addplot(short_term_simulation_data['Buy_signal_Price'], type='scatter', markersize=150, marker=r'$\Uparrow$', color = 'Red'),
            #mpf.make_addplot(short_term_simulation_data['Sell_Signal_price'], type='scatter', markersize=150, marker=r'$\Downarrow$', color = 'Green'),
            mpf.make_addplot(short_term_simulation_data['EMA'], color = 'orange', linestyle ='dotted'), #mpf.make_addplot(short_term_simulation_data['WMA'], color = 'purple', linestyle ='dotted'),
            mpf.make_addplot(short_term_simulation_data['SMA5'], color = 'blue'),mpf.make_addplot(short_term_simulation_data['SMA10'], color = 'Orange'),mpf.make_addplot(short_term_simulation_data['SMA20'], color = 'Green'),
            mpf.make_addplot(short_term_simulation_data['BOLLINGER_HBAND'], color = 'green', linestyle ='-.'),mpf.make_addplot(short_term_simulation_data['BOLLINGER_LBAND'], color = 'red', linestyle ='-.'),mpf.make_addplot(short_term_simulation_data['BOLLINGER_MAVG'], color = 'Fuchsia'),
            mpf.make_addplot(cci, panel=2, ylabel='CCI'),
            mpf.make_addplot(macd['MACD_DIFF'], type='bar', panel=3, ylabel='MACD', alpha=1,secondary_y=False),
            mpf.make_addplot(macd['MACD'],panel=3,color='fuchsia',secondary_y=True),
            mpf.make_addplot(macd['MACD_SIGNAL'],panel=3,color='blue',secondary_y=True),
            mpf.make_addplot(aroon, panel=4, ylabel='AROON'), mpf.make_addplot(rsi['RSI7'], panel=5, ylabel='RSI',color = 'black'), mpf.make_addplot(rsi['RSI14'], panel=5, ylabel='RSI',color = 'red')
        ]
        ymin = df2.loc[df2['Low'].idxmin()]['Low']*0.95
        ymax = df2.loc[df2['High'].idxmax()]['High']*1.05
        mpf.plot( df2, type='candle', style='yahoo', addplot=TA_plot, title=id, figscale=1.0, volume=True, ylim=(ymin,ymax), panel_ratios=(4,1),returnfig=True)
        fm = plt.get_current_fig_manager()
        fm.window.setGeometry(int((screen_width-30)/2)+20,30,int((screen_width-30)/2),int(screen_height/2))
        plt.ion()
        plt.show()
        plt.draw()
        if close_plot_second == 0:
            plt.close('all')
        else:
            plt.pause(close_plot_second)
            input("Press [enter] to continue.")
            plt.close('all')
    elif np.count_nonzero(~np.isnan(buy_sell[0])) == 0 and np.count_nonzero(~np.isnan(buy_sell[1])) != 0:
        TA_plot = [ #mpf.make_addplot(short_term_simulation_data['Min_signal_Price'], type='scatter', markersize=100, marker=r'$\Uparrow$', color = 'blue'),
            #mpf.make_addplot(short_term_simulation_data['Max_Signal_price'], type='scatter', markersize=100, marker=r'$\Downarrow$', color = 'blue'),
            #mpf.make_addplot(short_term_simulation_data['Buy_signal_Price'], type='scatter', markersize=150, marker=r'$\Uparrow$', color = 'Red'),
            mpf.make_addplot(short_term_simulation_data['Sell_Signal_price'], type='scatter', markersize=150, marker=r'$\Downarrow$', color = 'Green'),
            mpf.make_addplot(short_term_simulation_data['EMA'], color = 'orange', linestyle ='dotted'), #mpf.make_addplot(short_term_simulation_data['WMA'], color = 'purple', linestyle ='dotted'),
            mpf.make_addplot(short_term_simulation_data['SMA5'], color = 'blue'),mpf.make_addplot(short_term_simulation_data['SMA10'], color = 'Orange'),mpf.make_addplot(short_term_simulation_data['SMA20'], color = 'Green'),
            mpf.make_addplot(short_term_simulation_data['BOLLINGER_HBAND'], color = 'green', linestyle ='-.'),mpf.make_addplot(short_term_simulation_data['BOLLINGER_LBAND'], color = 'red', linestyle ='-.'),mpf.make_addplot(short_term_simulation_data['BOLLINGER_MAVG'], color = 'Fuchsia'),
            mpf.make_addplot(cci, panel=2, ylabel='CCI'),
            mpf.make_addplot(macd['MACD_DIFF'], type='bar', panel=3, ylabel='MACD', alpha=1,secondary_y=False),
            mpf.make_addplot(macd['MACD'],panel=3,color='fuchsia',secondary_y=True),
            mpf.make_addplot(macd['MACD_SIGNAL'],panel=3,color='blue',secondary_y=True),
            mpf.make_addplot(aroon, panel=4, ylabel='AROON'), mpf.make_addplot(rsi['RSI7'], panel=5, ylabel='RSI',color = 'black'), mpf.make_addplot(rsi['RSI14'], panel=5, ylabel='RSI',color = 'red')
        ]
        ymin = df2.loc[df2['Low'].idxmin()]['Low']*0.95
        ymax = df2.loc[df2['High'].idxmax()]['High']*1.05
        mpf.plot( df2, type='candle', style='yahoo', addplot=TA_plot, title=id, figscale=1.0, volume=True, ylim=(ymin,ymax), panel_ratios=(4,1),returnfig=True)
        fm = plt.get_current_fig_manager()
        fm.window.setGeometry(int((screen_width-30)/2)+20,30,int((screen_width-30)/2),int(screen_height/2))
        plt.ion()
        plt.show()
        plt.draw()
        if close_plot_second == 0:
            plt.close('all')
        else:
            plt.pause(close_plot_second)
            input("Press [enter] to continue.")
            plt.close('all')
    elif np.count_nonzero(~np.isnan(buy_sell[0])) == 0 and np.count_nonzero(~np.isnan(buy_sell[1])) == 0:
        TA_plot = [ #mpf.make_addplot(short_term_simulation_data['Min_signal_Price'], type='scatter', markersize=100, marker=r'$\Uparrow$', color = 'blue'),
            #mpf.make_addplot(short_term_simulation_data['Max_Signal_price'], type='scatter', markersize=100, marker=r'$\Downarrow$', color = 'blue'),
            #mpf.make_addplot(short_term_simulation_data['Buy_signal_Price'], type='scatter', markersize=150, marker=r'$\Uparrow$', color = 'Red'),
            #mpf.make_addplot(short_term_simulation_data['Sell_Signal_price'], type='scatter', markersize=150, marker=r'$\Downarrow$', color = 'Green'),
            mpf.make_addplot(short_term_simulation_data['EMA'], color = 'orange', linestyle ='dotted'), #mpf.make_addplot(short_term_simulation_data['WMA'], color = 'purple', linestyle ='dotted'),
            mpf.make_addplot(short_term_simulation_data['SMA5'], color = 'blue'),mpf.make_addplot(short_term_simulation_data['SMA10'], color = 'Orange'),mpf.make_addplot(short_term_simulation_data['SMA20'], color = 'Green'),
            mpf.make_addplot(short_term_simulation_data['BOLLINGER_HBAND'], color = 'green', linestyle ='-.'),mpf.make_addplot(short_term_simulation_data['BOLLINGER_LBAND'], color = 'red', linestyle ='-.'),mpf.make_addplot(short_term_simulation_data['BOLLINGER_MAVG'], color = 'Fuchsia'),
            mpf.make_addplot(cci, panel=2, ylabel='CCI'),
            mpf.make_addplot(macd['MACD_DIFF'], type='bar', panel=3, ylabel='MACD', alpha=1,secondary_y=False),
            mpf.make_addplot(macd['MACD'],panel=3,color='fuchsia',secondary_y=True),
            mpf.make_addplot(macd['MACD_SIGNAL'],panel=3,color='blue',secondary_y=True),
            mpf.make_addplot(aroon, panel=4, ylabel='AROON'), mpf.make_addplot(rsi['RSI7'], panel=5, ylabel='RSI',color = 'black'), mpf.make_addplot(rsi['RSI14'], panel=5, ylabel='RSI',color = 'red')
        ]
        ymin = df2.loc[df2['Low'].idxmin()]['Low']*0.95
        ymax = df2.loc[df2['High'].idxmax()]['High']*1.05
        mpf.plot( df2, type='candle', style='yahoo', addplot=TA_plot, title=id, figscale=1.0, volume=True, ylim=(ymin,ymax), panel_ratios=(4,1),returnfig=True)
        fm = plt.get_current_fig_manager()
        fm.window.setGeometry(int((screen_width-30)/2)+20,30,int((screen_width-30)/2),int(screen_height/2))
        plt.ion()
        plt.show()
        plt.draw()
        if close_plot_second == 0:
            plt.close('all')
        else:
            plt.pause(close_plot_second)
            input("Press [enter] to continue.")
            plt.close('all')
    else:
        TA_plot = [ #mpf.make_addplot(short_term_simulation_data['Min_signal_Price'], type='scatter', markersize=100, marker=r'$\Uparrow$', color = 'blue'),
            #mpf.make_addplot(short_term_simulation_data['Max_Signal_price'], type='scatter', markersize=100, marker=r'$\Downarrow$', color = 'blue'),
            mpf.make_addplot(short_term_simulation_data['Buy_signal_Price'], type='scatter', markersize=150, marker=r'$\Uparrow$', color = 'Red'),
            mpf.make_addplot(short_term_simulation_data['Sell_Signal_price'], type='scatter', markersize=150, marker=r'$\Downarrow$', color = 'Green'),
            mpf.make_addplot(short_term_simulation_data['EMA'], color = 'orange', linestyle ='dotted'), #mpf.make_addplot(short_term_simulation_data['WMA'], color = 'purple', linestyle ='dotted'),
            mpf.make_addplot(short_term_simulation_data['SMA5'], color = 'blue'),mpf.make_addplot(short_term_simulation_data['SMA10'], color = 'Orange'),mpf.make_addplot(short_term_simulation_data['SMA20'], color = 'Green'),
            mpf.make_addplot(short_term_simulation_data['BOLLINGER_HBAND'], color = 'green', linestyle ='-.'),mpf.make_addplot(short_term_simulation_data['BOLLINGER_LBAND'], color = 'red', linestyle ='-.'),mpf.make_addplot(short_term_simulation_data['BOLLINGER_MAVG'], color = 'Fuchsia'),
            mpf.make_addplot(cci, panel=2, ylabel='CCI'),
            mpf.make_addplot(macd['MACD_DIFF'], type='bar', panel=3, ylabel='MACD', alpha=1,secondary_y=False),
            mpf.make_addplot(macd['MACD'],panel=3,color='fuchsia',secondary_y=True),
            mpf.make_addplot(macd['MACD_SIGNAL'],panel=3,color='blue',secondary_y=True),
            mpf.make_addplot(aroon, panel=4, ylabel='AROON'), mpf.make_addplot(rsi['RSI7'], panel=5, ylabel='RSI',color = 'black'), mpf.make_addplot(rsi['RSI14'], panel=5, ylabel='RSI',color = 'red')
        ]
        ymin = df2.loc[df2['Low'].idxmin()]['Low']*0.90
        ymax = df2.loc[df2['High'].idxmax()]['High']*1.05
        mpf.plot( df2, type='candle', style='yahoo', addplot=TA_plot, title=id, figscale=1.0, volume=True, ylim=(ymin,ymax), panel_ratios=(4,1),returnfig=True)
        fm = plt.get_current_fig_manager()
        fm.window.setGeometry(int((screen_width-30)/2)+20,30,int((screen_width-30)/2),int(screen_height/2))
        plt.ion()
        plt.show()
        plt.draw()
        if close_plot_second == 0:
            plt.close('all')
        else:
            plt.pause(close_plot_second)
            input("Press [enter] to continue.")
            plt.close('all')


def Long_Term_Indicator(Long_Term_Indicator_days, id):
    global df,long_term_simulation_data,macd,aroon,rsi,cci,match_profit_rate_list
    regress_history_data_price = requests.get(api_url + 'products/'+id+'/candles?start='+start_datetime+'&end='+end_datetime+'&granularity='+str(Long_Term_Indicator_days_granularity), auth=auth)
    time.sleep(1)
    df = regress_history_data_price.json()
    df.reverse()
    labels = ['Date', 'Low', 'High', 'Open', 'Close', 'Volume']
    df = pd.DataFrame.from_records(df, columns=labels)
    df['Date'] = pd.to_datetime(df['Date'], unit='s')
    df = df.set_index('Date')
    df = dropna(df)
    indicator_MACD = ta.trend.MACD(df['Close'], window_slow = 26, window_fast = 12, window_sign = 9, fillna = False)
    indicator_RSI7 = ta.momentum.RSIIndicator(df['Close'], window=7, fillna=False)
    indicator_RSI14 = ta.momentum.RSIIndicator(df['Close'], window=14, fillna=False)
    indicator_AROON = ta.trend.AroonIndicator(df['Close'], window=14, fillna=False)
    indicator_SMA5 = ta.trend.SMAIndicator(df['Close'], window=5, fillna=False)
    indicator_SMA10 = ta.trend.SMAIndicator(df['Close'], window=10, fillna=False)
    indicator_SMA20 = ta.trend.SMAIndicator(df['Close'], window=20, fillna=False)
    indicator_EMA = ta.trend.EMAIndicator(df['Close'], window=20, fillna=False)
    indicator_WMA = ta.trend.WMAIndicator(df['Close'], window=20, fillna=False)
    indicator_BOLLINGER = ta.volatility.BollingerBands(df['Close'], window=60,window_dev=2,fillna=False)
    indicator_CCI = ta.trend.CCIIndicator(df['High'], df['Low'], df['Close'], window=144, constant=0.015, fillna=False)
    long_term_simulation_data = pd.DataFrame()
    long_term_simulation_data = df
    long_term_simulation_data['MACD'] = indicator_MACD.macd()
    long_term_simulation_data['MACD_DIFF'] = indicator_MACD.macd_diff()
    long_term_simulation_data['MACD_SIGNAL'] = indicator_MACD.macd_signal()
    long_term_simulation_data['RSI7'] = indicator_RSI7.rsi()
    long_term_simulation_data['RSI14'] = indicator_RSI14.rsi()
    long_term_simulation_data['ARRON_DOWN'] = indicator_AROON.aroon_down()
    long_term_simulation_data['ARRON_UP'] = indicator_AROON.aroon_up()
    long_term_simulation_data['ARRON'] = indicator_AROON.aroon_indicator()
    long_term_simulation_data['SMA5'] = indicator_SMA5.sma_indicator()
    long_term_simulation_data['SMA10'] = indicator_SMA10.sma_indicator()
    long_term_simulation_data['SMA20'] = indicator_SMA20.sma_indicator()
    long_term_simulation_data['EMA'] = indicator_EMA.ema_indicator()
    long_term_simulation_data['WMA'] = indicator_WMA.wma()
    long_term_simulation_data['BOLLINGER_HBAND'] = indicator_BOLLINGER.bollinger_hband()
    long_term_simulation_data['BOLLINGER_HBAND_INDICATOR'] = indicator_BOLLINGER.bollinger_hband_indicator()
    long_term_simulation_data['BOLLINGER_LBAND'] = indicator_BOLLINGER.bollinger_lband()
    long_term_simulation_data['BOLLINGER_LBAND_INDICATOR'] = indicator_BOLLINGER.bollinger_lband_indicator()
    long_term_simulation_data['BOLLINGER_MAVG'] = indicator_BOLLINGER.bollinger_mavg()
    long_term_simulation_data['BOLLINGER_PBAND'] = indicator_BOLLINGER.bollinger_pband()
    long_term_simulation_data['BOLLINGER_WBAND'] = indicator_BOLLINGER.bollinger_wband()
    long_term_simulation_data['CCI'] = indicator_CCI.cci()
    macd = pd.DataFrame()
    macd['MACD'] = long_term_simulation_data['MACD']
    macd['MACD_DIFF'] = long_term_simulation_data['MACD_DIFF']
    macd['MACD_SIGNAL'] = long_term_simulation_data['MACD_SIGNAL']
    aroon = pd.DataFrame()
    aroon['ARRON_DOWN'] = long_term_simulation_data['ARRON_DOWN']
    aroon['ARRON_UP'] = long_term_simulation_data['ARRON_UP']
    aroon['ARRON'] = long_term_simulation_data['ARRON']
    rsi = pd.DataFrame()
    rsi['RSI7'] = long_term_simulation_data['RSI7']
    rsi['RSI14'] = long_term_simulation_data['RSI14']
    cci = pd.DataFrame()
    cci['CCI'] = long_term_simulation_data['CCI']
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 150)
    new_content = []
    print('------------------------------------------------------------------------------------------------------')
    print(id)
    print(long_term_simulation_data.loc[ [min_max_list[i][2]],['High','MACD','MACD_DIFF','MACD_SIGNAL','RSI7','RSI14','ARRON_DOWN','ARRON_UP','ARRON','BOLLINGER_HBAND','BOLLINGER_HBAND_INDICATOR','BOLLINGER_LBAND','BOLLINGER_LBAND_INDICATOR','BOLLINGER_MAVG','BOLLINGER_PBAND','BOLLINGER_WBAND'] ])
    print(long_term_simulation_data.loc[ [min_max_list[i][4]],['Low' ,'MACD','MACD_DIFF','MACD_SIGNAL','RSI7','RSI14','ARRON_DOWN','ARRON_UP','ARRON','BOLLINGER_HBAND','BOLLINGER_HBAND_INDICATOR','BOLLINGER_LBAND','BOLLINGER_LBAND_INDICATOR','BOLLINGER_MAVG','BOLLINGER_PBAND','BOLLINGER_WBAND'] ])
    max_min = plotdata_Max_Min(long_term_simulation_data)   ##### Get the Highest and Lowest price points in the predefined period of time #####
    long_term_simulation_data['Min_signal_Price'] = max_min[0]
    long_term_simulation_data['Max_Signal_price'] = max_min[1]
    print('------------------------------------------------------------------------------------------------------')
    buy_sell = plotdata_Buy_Sell_indicator_simulate(long_term_simulation_data)   ##### Get the Buy and Sell points in the predefined profit percent #####
    long_term_simulation_data['Buy_signal_Price'] = buy_sell[0]
    long_term_simulation_data['Sell_Signal_price'] = buy_sell[1]
    print("Match profit_rate Buy Opportunity", np.count_nonzero(~np.isnan(buy_sell[0])))
    print("Match profit_rate Sell Opportunity", np.count_nonzero(~np.isnan(buy_sell[1])))
    match_profit_rate_list.append( [id,np.count_nonzero(~np.isnan(buy_sell[0])),np.count_nonzero(~np.isnan(buy_sell[1]))] )
    print(long_term_simulation_data[long_term_simulation_data['Buy_signal_Price'].notnull()])
    print(long_term_simulation_data[long_term_simulation_data['Sell_Signal_price'].notnull()])
    with open(output_data_file, 'r') as in_file:
        for line in in_file.readlines():
            new_content += line
    new_content += "{}".format(id)
    new_content += "\n"
    new_content += "{}".format(long_term_simulation_data.loc[ [min_max_list[i][2]],['High','MACD','MACD_DIFF','MACD_SIGNAL','RSI7','RSI14','ARRON_DOWN','ARRON_UP','ARRON','BOLLINGER_HBAND','BOLLINGER_HBAND_INDICATOR','BOLLINGER_LBAND','BOLLINGER_LBAND_INDICATOR','BOLLINGER_MAVG','BOLLINGER_PBAND','BOLLINGER_WBAND'] ])
    new_content += "\n"
    new_content += "{}".format(long_term_simulation_data.loc[ [min_max_list[i][4]],['Low' ,'MACD','MACD_DIFF','MACD_SIGNAL','RSI7','RSI14','ARRON_DOWN','ARRON_UP','ARRON','BOLLINGER_HBAND','BOLLINGER_HBAND_INDICATOR','BOLLINGER_LBAND','BOLLINGER_LBAND_INDICATOR','BOLLINGER_MAVG','BOLLINGER_PBAND','BOLLINGER_WBAND'] ])
    new_content += "\n"
    new_content += "{}".format(long_term_simulation_data[long_term_simulation_data['Buy_signal_Price'].notnull()])
    new_content += "\n"
    new_content += "{}".format(long_term_simulation_data[long_term_simulation_data['Sell_Signal_price'].notnull()])
    new_content += "\n"
    new_content += "{}".format("------------------------------------------------------------------------------------------------------")
    new_content += "\n"
    with open(output_data_file, 'w') as out_file:
        out_file.writelines(new_content)
    in_file.close()
    out_file.close()
    print('======================================================================================================')
    if np.count_nonzero(~np.isnan(cci['CCI'])) == 0:
        print("CCI is empty, skip the plot")
    elif np.count_nonzero(~np.isnan(macd['MACD'])) == 0 or np.count_nonzero(~np.isnan(macd['MACD_DIFF'])) == 0 or np.count_nonzero(~np.isnan(macd['MACD_SIGNAL'])) == 0:
        print("MACD is empty, skip the plot")
    elif np.count_nonzero(~np.isnan(aroon['ARRON_DOWN'])) == 0 or np.count_nonzero(~np.isnan(aroon['ARRON_UP'])) == 0 or np.count_nonzero(~np.isnan(aroon['ARRON'])) == 0:
        print("AROON is empty, skip the plot")
    elif np.count_nonzero(~np.isnan(rsi['RSI7'])) == 0 or np.count_nonzero(~np.isnan(rsi['RSI14'])) == 0 :
        print("RSI is empty")
    else:
        draw_Buy_Sell_indicator_simulate(buy_sell,id)


def Short_Term_Indicator(Short_Term_Indicator_days, id):
    global df2,short_term_simulation_data,macd,aroon,rsi,cci,match_indicator_simulate_list
    regress_history_data_price = requests.get(api_url + 'products/'+id+'/candles?start='+start_datetime+'&end='+end_datetime+'&granularity='+str(Short_Term_Indicator_days_granularity), auth=auth)
    time.sleep(1)
    df2 = regress_history_data_price.json()
    print(len(df2))
    df2.reverse()
    labels = ['Date', 'Low', 'High', 'Open', 'Close', 'Volume']
    df2 = pd.DataFrame.from_records(df2, columns=labels)
    df2['Date'] = pd.to_datetime(df2['Date'], unit='s')
    df2 = df2.set_index('Date')
    df2 = dropna(df2)
    indicator_MACD = ta.trend.MACD(df2['Close'], window_slow = 26, window_fast = 12, window_sign = 9, fillna = False)
    indicator_RSI7 = ta.momentum.RSIIndicator(df2['Close'], window=7, fillna=False)
    indicator_RSI14 = ta.momentum.RSIIndicator(df2['Close'], window=14, fillna=False)
    indicator_AROON = ta.trend.AroonIndicator(df2['Close'], window=14, fillna=False)
    indicator_SMA5 = ta.trend.SMAIndicator(df2['Close'], window=5, fillna=False)
    indicator_SMA10 = ta.trend.SMAIndicator(df2['Close'], window=10, fillna=False)
    indicator_SMA20 = ta.trend.SMAIndicator(df2['Close'], window=20, fillna=False)
    indicator_EMA = ta.trend.EMAIndicator(df2['Close'], window=20, fillna=False)
    indicator_WMA = ta.trend.WMAIndicator(df2['Close'], window=20, fillna=False)
    indicator_BOLLINGER = ta.volatility.BollingerBands(df2['Close'], window=60,window_dev=2,fillna=False)
    indicator_CCI = ta.trend.CCIIndicator(df2['High'], df2['Low'], df2['Close'], window=144, constant=0.015, fillna=False)
    short_term_simulation_data = pd.DataFrame()
    short_term_simulation_data = df2
    short_term_simulation_data['MACD'] = indicator_MACD.macd()
    short_term_simulation_data['MACD_DIFF'] = indicator_MACD.macd_diff()
    short_term_simulation_data['MACD_SIGNAL'] = indicator_MACD.macd_signal()
    short_term_simulation_data['RSI7'] = indicator_RSI7.rsi()
    short_term_simulation_data['RSI14'] = indicator_RSI14.rsi()
    short_term_simulation_data['ARRON_DOWN'] = indicator_AROON.aroon_down()
    short_term_simulation_data['ARRON_UP'] = indicator_AROON.aroon_up()
    short_term_simulation_data['ARRON'] = indicator_AROON.aroon_indicator()
    short_term_simulation_data['SMA5'] = indicator_SMA5.sma_indicator()
    short_term_simulation_data['SMA10'] = indicator_SMA10.sma_indicator()
    short_term_simulation_data['SMA20'] = indicator_SMA20.sma_indicator()
    short_term_simulation_data['EMA'] = indicator_EMA.ema_indicator()
    short_term_simulation_data['WMA'] = indicator_WMA.wma()
    short_term_simulation_data['BOLLINGER_HBAND'] = indicator_BOLLINGER.bollinger_hband()
    short_term_simulation_data['BOLLINGER_HBAND_INDICATOR'] = indicator_BOLLINGER.bollinger_hband_indicator()
    short_term_simulation_data['BOLLINGER_LBAND'] = indicator_BOLLINGER.bollinger_lband()
    short_term_simulation_data['BOLLINGER_LBAND_INDICATOR'] = indicator_BOLLINGER.bollinger_lband_indicator()
    short_term_simulation_data['BOLLINGER_MAVG'] = indicator_BOLLINGER.bollinger_mavg()
    short_term_simulation_data['BOLLINGER_PBAND'] = indicator_BOLLINGER.bollinger_pband()
    short_term_simulation_data['BOLLINGER_WBAND'] = indicator_BOLLINGER.bollinger_wband()
    short_term_simulation_data['CCI'] = indicator_CCI.cci()
    macd = pd.DataFrame()
    macd['MACD'] = short_term_simulation_data['MACD']
    macd['MACD_DIFF'] = short_term_simulation_data['MACD_DIFF']
    macd['MACD_SIGNAL'] = short_term_simulation_data['MACD_SIGNAL']
    aroon = pd.DataFrame()
    aroon['ARRON_DOWN'] = short_term_simulation_data['ARRON_DOWN']
    aroon['ARRON_UP'] = short_term_simulation_data['ARRON_UP']
    aroon['ARRON'] = short_term_simulation_data['ARRON']
    rsi = pd.DataFrame()
    rsi['RSI7'] = short_term_simulation_data['RSI7']
    rsi['RSI14'] = short_term_simulation_data['RSI14']
    cci = pd.DataFrame()
    cci['CCI'] = short_term_simulation_data['CCI']
    buy_sell = plotdata_Prediction_Simulate(short_term_simulation_data)
    short_term_simulation_data['Buy_signal_Price'] = buy_sell[0]
    short_term_simulation_data['Sell_Signal_price'] = buy_sell[1]
    print("Simulation Buy Opportunity", np.count_nonzero(~np.isnan(buy_sell[0])))
    print("Simulation Sell Opportunity", np.count_nonzero(~np.isnan(buy_sell[1])))
    match_indicator_simulate_list.append( [id, np.count_nonzero(~np.isnan(buy_sell[0])), np.count_nonzero(~np.isnan(buy_sell[1]))] )
    print(short_term_simulation_data[short_term_simulation_data['Buy_signal_Price'].notnull()])
    print(short_term_simulation_data[short_term_simulation_data['Sell_Signal_price'].notnull()])
    print('======================================================================================================')
    if np.count_nonzero(~np.isnan(cci['CCI'])) == 0:
        print("CCI is empty, skip the plot")
    elif np.count_nonzero(~np.isnan(macd['MACD'])) == 0 or np.count_nonzero(~np.isnan(macd['MACD_DIFF'])) == 0 or np.count_nonzero(~np.isnan(macd['MACD_SIGNAL'])) == 0:
        print("MACD is empty, skip the plot")
    elif np.count_nonzero(~np.isnan(aroon['ARRON_DOWN'])) == 0 or np.count_nonzero(~np.isnan(aroon['ARRON_UP'])) == 0 or np.count_nonzero(~np.isnan(aroon['ARRON'])) == 0:
        print("AROON is empty, skip the plot")
    elif np.count_nonzero(~np.isnan(rsi['RSI7'])) == 0 or np.count_nonzero(~np.isnan(rsi['RSI14'])) == 0 :
        print("RSI is empty")
    else:
        draw_Prediction_Simulate(buy_sell,id)


api_url = 'https://api.pro.coinbase.com/'
auth = CoinbaseExchangeAuth(api_key, secret_key, passphrase)
coinbase_products = requests.get(api_url + 'products', auth=auth)

current_datetime = requests.get(api_url + 'time', auth=auth)
time.sleep(1)
start_datetime = datetime.utcfromtimestamp(current_datetime.json()['epoch']-86400*Long_Term_Indicator_days).__format__('%Y-%m-%d %H:%M:%S')
end_datetime = datetime.utcfromtimestamp(current_datetime.json()['epoch']).__format__('%Y-%m-%d %H:%M:%S')
print("Current local date time(CST): ", datetime.utcfromtimestamp(current_datetime.json()['epoch']+seconds_UTC2local).__format__('%Y-%m-%d %H:%M:%S'))
print("Start Date(UTC) : ",start_datetime,"   End Date(UTC) : ", end_datetime)
print('------------------------------------------------------------------------------------------------------')
##### min_max_list formart [id, history records number, max price date, max price, min price date, min price] #####
min_max_list = []
##### match_profit_rate_list formart [id, Match profit_rate Buy Opportunity, Match profit_rate Sell Opportunity] #####
match_profit_rate_list = []
##### match_indicator_simulate_list formart [id, Simulation Buy Opportunity, Simulation Sell Opportunity] #####
match_indicator_simulate_list = []
for item in coinbase_products.json():
    if (item['id'].endswith("-USDC")) and (item['status_message'] == ""):
        min_max_price(Long_Term_Indicator_days,item['id'])
for item in coinbase_products.json():
    if (item['id'].endswith("-BTC")) and (item['status_message'] == ""):
        min_max_price(Long_Term_Indicator_days,item['id'])
for i in range(len(min_max_list)):
    if min_max_list[i][1] >= Long_Term_Indicator_days and min_max_list[i][1] > 14:
        start_datetime = datetime.utcfromtimestamp(current_datetime.json()['epoch']-86400*Long_Term_Indicator_days).__format__('%Y-%m-%d %H:%M:%S')
        Long_Term_Indicator(Long_Term_Indicator_days, min_max_list[i][0])
        start_datetime = datetime.utcfromtimestamp(current_datetime.json()['epoch']-86400*Short_Term_Indicator_days).__format__('%Y-%m-%d %H:%M:%S')
        Short_Term_Indicator(Short_Term_Indicator_days, min_max_list[i][0])
print(match_profit_rate_list)
print(match_indicator_simulate_list)
