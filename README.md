cryptocurrency_trading_simulator.py is used to simulate the cryptocurrency trading indicators.

Currently it support 'MACD','RSI','ARRON','SMA','EMA','WMA','BOLLINGER','CCI' indicators.

You need have CoinBase Pro API first, but if you have the other data soruce I think it also can support. If you have more data source please share it with me.

Because I'm not a expert of stock trading so I'm not familiar with these indicators. And you also can define your own trading condition and use this tool to simulate.

<img src="/screenshot/screenshot_01.jpg">

<img src="/screenshot/screenshot_02.jpg">


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
