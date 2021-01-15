#Initial Parameters
api_key = ''
secret_key = ''
passphrase = ''
regress_history_days = 3 # Because of CoinBase pro API limits, if the days too far away or the granularity too small will cause no data return from the API.
simulate_history_days = 1 # Because of CoinBase pro API limits, if the days too far away or the granularity too small will cause no data return from the API.
seconds_cancel_order = 60
days_history_data = 3
seconds_UTC2local = -21600
BTC_lower_limit = 100 # If BTC balance value less than 100 USD stop trade
USDC_lower_limit = 100 # If USDC balance value less than 100 USD stop trade
first_buy_percent = 0.10
second_buy_percent = 0.20
third_buy_percent = 0.30
low_price_percent = 0.90
profit_rate = 1.10
plot1_granularity = 900 #{60, 300, 900, 3600, 21600, 86400} Because of CoinBase pro API limits, if the days too far away or the granularity too small will cause no data return from the API.
plot2_granularity = 300 #{60, 300, 900, 3600, 21600, 86400} Because of CoinBase pro API limits, if the days too far away or the granularity too small will cause no data return from the API.
exclude_currency = [] # "exclude_currency" and "include_currency" only one can have items or both empty
include_currency = [] # "exclude_currency" and "include_currency" only one can have items or both empty

