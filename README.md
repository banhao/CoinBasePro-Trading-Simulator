cryptocurrency_trading_simulator.py is used to simulate the cryptocurrency trading indicators.

Currently it support 'MACD','RSI','ARRON','SMA','EMA','WMA','BOLLINGER','CCI' indicators.

You need have CoinBase Pro API first, but if you have the other data soruce I think it also can support. If you have more data source please share it with me.

Because I'm not a expert of stock trading so I'm not familiar with these indicators. And you also can define your own trading condition and use this tool to simulate.


Here I'll give you an example and explain it.

The first plot the tool will show you the max/min price by blue down/up arrow in the predefined period. And also use red/green arrows to show you all matched opportunities that predefine in parameter "profit_rate", here it's 10%.

And the tool will also output the data of the match point.

<img src="/screenshot/screenshot_01.jpg">

```
REN-BTC
                         High          MACD     MACD_DIFF   MACD_SIGNAL      RSI7      RSI14  ARRON_DOWN  ARRON_UP      ARRON  BOLLINGER_HBAND  \
Date
2021-01-15 03:15:00  0.000015  2.785402e-07  1.147812e-07  1.637591e-07  87.63128  77.310638   21.428571     100.0  78.571429         0.000013

                     BOLLINGER_HBAND_INDICATOR  BOLLINGER_LBAND  BOLLINGER_LBAND_INDICATOR  BOLLINGER_MAVG  BOLLINGER_PBAND  BOLLINGER_WBAND
Date
2021-01-15 03:15:00                        1.0         0.000011                        0.0        0.000012         1.461119        10.885924
                         Low          MACD     MACD_DIFF   MACD_SIGNAL       RSI7      RSI14  ARRON_DOWN   ARRON_UP      ARRON  BOLLINGER_HBAND  \
Date
2021-01-13 21:45:00  0.00001 -9.675435e-08 -8.245229e-08 -1.430206e-08  14.151404  28.135547       100.0  28.571429 -71.428571         0.000012

                     BOLLINGER_HBAND_INDICATOR  BOLLINGER_LBAND  BOLLINGER_LBAND_INDICATOR  BOLLINGER_MAVG  BOLLINGER_PBAND  BOLLINGER_WBAND
Date
2021-01-13 21:45:00                        0.0         0.000011                        0.0        0.000011         0.115376        11.892132
------------------------------------------------------------------------------------------------------
Match profit_rate Buy Opportunity 4
Match profit_rate Sell Opportunity 4
                          Low      High      Open     Close  Volume          MACD     MACD_DIFF   MACD_SIGNAL       RSI7      RSI14  ARRON_DOWN  \
Date
2021-01-12 04:30:00  0.000011  0.000011  0.000011  0.000011   21921           NaN           NaN           NaN        NaN        NaN         NaN
2021-01-12 14:00:00  0.000010  0.000011  0.000011  0.000010    5815 -4.599820e-08 -3.391777e-09 -4.260643e-08  26.343895  36.467209       100.0
2021-01-13 22:45:00  0.000011  0.000011  0.000011  0.000011   23689 -1.778982e-07 -8.113621e-08 -9.676197e-08  21.542520  30.235613       100.0
2021-01-14 21:00:00  0.000012  0.000012  0.000012  0.000012   35545 -5.476099e-08 -3.931264e-08 -1.544835e-08  27.923919  37.738088       100.0

                      ARRON_UP      ARRON      SMA5     SMA10     SMA60       EMA       WMA  BOLLINGER_HBAND  BOLLINGER_HBAND_INDICATOR  \
Date
2021-01-12 04:30:00        NaN        NaN       NaN       NaN       NaN       NaN       NaN              NaN                        0.0
2021-01-12 14:00:00  50.000000 -50.000000  0.000011  0.000011       NaN  0.000011  0.000011              NaN                        0.0
2021-01-13 22:45:00  21.428571 -78.571429  0.000011  0.000011  0.000011  0.000011  0.000011         0.000012                        0.0
2021-01-14 21:00:00   7.142857 -92.857143  0.000012  0.000012  0.000012  0.000012  0.000012         0.000012                        0.0

                     BOLLINGER_LBAND  BOLLINGER_LBAND_INDICATOR  BOLLINGER_MAVG  BOLLINGER_PBAND  BOLLINGER_WBAND        CCI  Min_signal_Price  \
Date
2021-01-12 04:30:00              NaN                        0.0             NaN              NaN              NaN        NaN               NaN
2021-01-12 14:00:00              NaN                        0.0             NaN              NaN              NaN        NaN               NaN
2021-01-13 22:45:00         0.000011                        0.0        0.000012         0.037007        11.197577 -26.077075               NaN
2021-01-14 21:00:00         0.000011                        0.0        0.000012         0.124860         8.305822   9.335825               NaN

                     Max_Signal_price  Buy_signal_Price  Sell_Signal_price
Date
2021-01-12 04:30:00               NaN          0.000011                NaN
2021-01-12 14:00:00               NaN          0.000010                NaN
2021-01-13 22:45:00               NaN          0.000011                NaN
2021-01-14 21:00:00               NaN          0.000012                NaN
                          Low      High      Open     Close  Volume          MACD     MACD_DIFF   MACD_SIGNAL       RSI7      RSI14  ARRON_DOWN  \
Date
2021-01-12 05:15:00  0.000011  0.000012  0.000011  0.000012   22024           NaN           NaN           NaN  95.310707        NaN         NaN
2021-01-13 14:00:00  0.000012  0.000012  0.000012  0.000012   22977  1.619489e-07  2.815063e-08  1.337982e-07  79.580668  71.743623   28.571429
2021-01-14 11:15:00  0.000012  0.000012  0.000012  0.000012   32035  8.064031e-08  3.320452e-08  4.743579e-08  82.881182  69.146365   57.142857
2021-01-15 02:45:00  0.000013  0.000013  0.000013  0.000013   45110  1.951036e-07  8.218269e-08  1.129209e-07  80.029781  70.672121   35.714286

                     ARRON_UP      ARRON      SMA5     SMA10     SMA60       EMA       WMA  BOLLINGER_HBAND  BOLLINGER_HBAND_INDICATOR  \
Date
2021-01-12 05:15:00       NaN        NaN  0.000011       NaN       NaN       NaN       NaN              NaN                        0.0
2021-01-13 14:00:00     100.0  71.428571  0.000011  0.000011  0.000011  0.000011  0.000011         0.000011                        1.0
2021-01-14 11:15:00     100.0  42.857143  0.000012  0.000012  0.000011  0.000012  0.000012         0.000012                        1.0
2021-01-15 02:45:00     100.0  64.285714  0.000013  0.000012  0.000012  0.000012  0.000012         0.000013                        1.0

                     BOLLINGER_LBAND  BOLLINGER_LBAND_INDICATOR  BOLLINGER_MAVG  BOLLINGER_PBAND  BOLLINGER_WBAND         CCI  Min_signal_Price  \
Date
2021-01-12 05:15:00              NaN                        0.0             NaN              NaN              NaN         NaN               NaN
2021-01-13 14:00:00         0.000010                        0.0        0.000011         1.151103         9.741565         NaN               NaN
2021-01-14 11:15:00         0.000011                        0.0        0.000011         1.120887         8.622493  130.782797               NaN
2021-01-15 02:45:00         0.000012                        0.0        0.000012         1.313614         8.495411  222.129176               NaN

                     Max_Signal_price  Buy_signal_Price  Sell_Signal_price
Date
2021-01-12 05:15:00               NaN               NaN           0.000012
2021-01-13 14:00:00               NaN               NaN           0.000012
2021-01-14 11:15:00               NaN               NaN           0.000012
2021-01-15 02:45:00               NaN               NaN           0.000013
------------------------------------------------------------------------------------------------------
279
Simulation Buy Opportunity 1
Simulation Sell Opportunity 1
                          Low      High      Open     Close  Volume          MACD     MACD_DIFF   MACD_SIGNAL       RSI7     RSI14  ARRON_DOWN  \
Date
2021-01-14 21:15:00  0.000012  0.000012  0.000012  0.000012    5212 -6.494159e-08 -3.909805e-08 -2.584354e-08  34.739297  39.24143   92.857143

                      ARRON_UP      ARRON      SMA5     SMA10     SMA60       EMA       WMA  BOLLINGER_HBAND  BOLLINGER_HBAND_INDICATOR  \
Date
2021-01-14 21:15:00  57.142857 -35.714286  0.000012  0.000012  0.000012  0.000012  0.000012         0.000012                        0.0

                     BOLLINGER_LBAND  BOLLINGER_LBAND_INDICATOR  BOLLINGER_MAVG  BOLLINGER_PBAND  BOLLINGER_WBAND         CCI  Buy_signal_Price  \
Date
2021-01-14 21:15:00         0.000012                        1.0        0.000012        -0.075968         4.664584 -134.755855          0.000012

                     Sell_Signal_price
Date
2021-01-14 21:15:00                NaN
                          Low      High      Open     Close  Volume          MACD     MACD_DIFF   MACD_SIGNAL       RSI7      RSI14  ARRON_DOWN  \
Date
2021-01-15 02:55:00  0.000013  0.000013  0.000013  0.000013   13875  1.717742e-07  3.410695e-08  1.376673e-07  82.091588  73.814921    7.142857

                     ARRON_UP      ARRON      SMA5     SMA10     SMA60       EMA       WMA  BOLLINGER_HBAND  BOLLINGER_HBAND_INDICATOR  \
Date
2021-01-15 02:55:00     100.0  92.857143  0.000013  0.000013  0.000012  0.000013  0.000013         0.000013                        1.0

                     BOLLINGER_LBAND  BOLLINGER_LBAND_INDICATOR  BOLLINGER_MAVG  BOLLINGER_PBAND  BOLLINGER_WBAND         CCI  Buy_signal_Price  \
Date
2021-01-15 02:55:00         0.000012                        0.0        0.000012         1.185002         8.805261  295.221026               NaN

                     Sell_Signal_price
Date
2021-01-15 02:55:00           0.000013
```

The second plot will give you all the match point that you defined condition in the tool. 

For example, my buy condition is if the candle is lower than 'BOLLINGER_LBAND' and 'CCI' is less than -100. 

My sell condition is if the candle is higher than 'BOLLINGER_HBAND' and 'CCI' is more than 100 and the profit is more than 10%.    

<img src="/screenshot/screenshot_02.jpg">

<b>Note: You can use the different period days and granularity for the first plot and second plot, but remember the number of the data return from API mush be less than 300. Here the first plot "regress_history_days = 3" and "regress_history_days_granularity = 900", the second plot "simulate_history_days = 1" and "simulate_history_days_granularity = 300".</b>

variable.py is used to load paraments/variables and I also remained some paraments/variables for automatice trading tools to share one variable file (Automatic trading tool is still in testing)

```
#Initial Parameters
api_key = ''                #input your coinbase pro api_key,secret_key and passphrase here
secret_key = ''
passphrase = ''
regress_history_days = 3    #how many days you want to get the history data.
regress_history_days_granularity = 900     #{60, 300, 900, 3600, 21600, 86400} Because of CoinBase pro API limits, you only can get 300 data from coinbase pro API. If you want to get 3 days data so the granularity must be greater or equal 900. 86400/900=96, 96*3=288 less than 300.
simulate_history_days = 1   #how many days you want to get the history data.
simulate_history_days_granularity = 300    #{60, 300, 900, 3600, 21600, 86400} 
seconds_UTC2local = -25200  #seconds between UTC and your time zone, for example if your are in UTC-7h, so this should be -25200. 
profit_rate = 1.10          #profit define, if you want have 10% profit it should be 1.10. If you want to have 20% profit it should be 1.20.
seconds_cancel_order = 60   #remained for trading tool 
days_history_data = 3       #remained for trading tool
BTC_lower_limit = 100       #remained for trading tool
USDC_lower_limit = 100      #remained for trading tool
first_buy_percent = 0.10    #remained for trading tool
second_buy_percent = 0.20   #remained for trading tool
third_buy_percent = 0.30    #remained for trading tool
low_price_percent = 0.90    #remained for trading tool
exclude_currency = []       #remained for trading tool
include_currency = []       #remained for trading tool
```

<b>
Next version I'd like to have a configure file that can define different buy and sell condition for each crypto currency.

If you have any idea want to add in the tools you can send me an email and let me know.
</b>
