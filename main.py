"""
Created 25/07/2021

Main code.

@author: Tom Ronayne
"""

import bots
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import time
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData

API_key = open('C:/Users/Tom/github/MoneyLosingMachine/key.txt').read()

ts = TimeSeries(key=API_key, output_format='pandas')
print('Key accepted')

user_input = input('Request new data? (y/n)')
#user_input = 'n'
if user_input == 'y':
    print('Requesting Alpha Vantage data...')
    t0 = time.time()

    data, metadata = ts.get_daily('CNCR', outputsize='full')
    #print(metadata)
    data.to_pickle('data.pkl')

    t1 = time.time()
    print('Data acquired, length: {0}, Time taken: {1:.2f} s'.format(len(data), t1-t0))
else:
    data = pd.read_pickle('C:/Users/Tom/github/MoneyLosingMachine/data.pkl')
    print('Data unpickled')

"""print('Acquiring data...')
#t0 = time.time()
dataframe = ts.get_daily('CNCR', outputsize='full')
dataframe.to_pickle('dataframe')
dataframe = pd.read_pickle('dataframe')
data, meta_data = dataframe
#t1 = time.time()
print('Data acquired, length:', len(data))#, 'Time taken:', t0 - t1, 's')"""

data.columns = ['open', 'high', 'low', 'close', 'volume']
data['TradeDate'] = data.index.date
data['time'] = data.index.time

plt.plot(data[data['TradeDate']>datetime.date(2020, 1, 1)]['close'])

simple_jack = bots.simple_jack()
#for date in pd.date_range(start="2020-01-01",end="2020-07-01"):
for date in pd.date_range(start="2021-01-01", end=data['TradeDate'].max()):
    if not data[data['TradeDate']==date].empty:
        price = data[data['TradeDate']==date]['close'][-1]
        #print(date.date())#, ' $', price)
        simple_jack.execute_strategy(data, date)

print('Total profit: $ {0:.2f}'.format(simple_jack.balance))


plt.show()
