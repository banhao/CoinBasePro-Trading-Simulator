#Initial Parameters
import ctypes
api_key = ''
secret_key = ''
passphrase = ''
screen_width = ctypes.windll.user32.GetSystemMetrics(0)
screen_height = ctypes.windll.user32.GetSystemMetrics(1)
regress_history_days = 300
regress_history_days_granularity = 86400 #{60, 300, 900, 3600, 21600, 86400}
simulate_history_days = 1
simulate_history_days_granularity = 300 #{60, 300, 900, 3600, 21600, 86400}
seconds_UTC2local = -25200
profit_rate = 1.10
seconds_cancel_order = 60
BTC_lower_limit = 100
USDC_lower_limit = 100
first_buy_percent = 0.10
second_buy_percent = 0.20
third_buy_percent = 0.30
low_price_percent = 0.90
exclude_currency = [] # "exclude_currency" and "include_currency" only one can have items or both empty
include_currency = [] # "exclude_currency" and "include_currency" only one can have items or both empty
output_data_file = 'output_data.txt'
close_plot_second = 5
