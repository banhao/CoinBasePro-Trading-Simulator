#Initial Parameters
import ctypes
import os
api_key = ''
secret_key = ''
passphrase = ''
if os.name == 'nt':
    screen_width = ctypes.windll.user32.GetSystemMetrics(0)
    screen_height = ctypes.windll.user32.GetSystemMetrics(1)
Long_Term_Indicator_days = 300
Long_Term_Indicator_days_granularity = 86400 #{60, 300, 900, 3600, 21600, 86400}
Short_Term_Indicator_days = 1
Short_Term_Indicator_days_granularity = 300 #{60, 300, 900, 3600, 21600, 86400}
seconds_UTC2local = -25200
profit_rate = 1.10
seconds_cancel_order = 60
BTC_lower_limit = 100
USDC_lower_limit = 100
first_buy_percent = 0.10
second_buy_percent = 0.20
third_buy_percent = 0.30
exclude_currency = ["XRP-BTC","DAI-USDC","WBTC-BTC"] # "exclude_currency" and "include_currency" only one can have items or both empty
include_currency = [] # "exclude_currency" and "include_currency" only one can have items or both empty
output_data_file = 'output_data.txt'
close_plot_second = 0 # "0" will not show the plot, just use for generate data
order_start_date = '2021-02-01'
