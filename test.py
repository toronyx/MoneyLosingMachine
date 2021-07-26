# Python 3.9.6
"""
Created 14/07/2021

What am I doing.

@author: Tom Ronayne
"""

import pandas as pd
import matplotlib.pyplot as plt
import datetime
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData

API_key = open('C:/Users/Tom/github/MoneyLosingMachine/key.txt').read()

ts = TimeSeries(key=API_key, output_format='pandas')
#fd = FundamentalData(key=API_key, output_format='pandas')

#data = ts.get_monthly_adjusted('MSFT')
#data = fd.get_income_statement_annual('MSFT')
#ts.get_daily('CNCR', outputsize='full')

#data, meta_data = ts.get_intraday(symbold='MSFT', interval='1min', outputsize='full')
data, meta_data = ts.get_daily('CNCR', outputsize='full')
data.columns = ['open', 'high', 'low', 'close', 'volume']
data['TradeDate'] = data.index.date
data['time'] = data.index.time

print(data.head())
#plt.plot(data[data['TradeDate']>datetime.date(2019, 1, 1)]['close'])



""" Let's get some fake money involved """

bank_balance = 100.00
number_of_shares = 0

def buy(daily_data, date, shares):
    global bank_balance, number_of_shares
    price = daily_data[daily_data['TradeDate']==date]['close'][-1]
    bank_balance -= price*shares
    number_of_shares += shares
    print("Bought {0} shares for $ {1} total on {2}".format(shares, shares*price, date))

def sell(daily_data, date, shares):
    global bank_balance, number_of_shares
    price = daily_data[daily_data['TradeDate']==date]['close'][-1]
    bank_balance += price*shares
    number_of_shares -= shares
    print("Sold {0} shares for $ {1} total on {2}".format(shares, shares*price, date))

print('Balance = $', bank_balance)
buy(data, datetime.date(2020, 4, 1), 3)
print('Balance = $', bank_balance)
sell(data, datetime.date(2020, 7, 13), 3)
print('Balance = $', bank_balance)



#plt.show()
