"""
Created 25/07/2021

Main code.

@author: Tom Ronayne
"""

import bots
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import time
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData

API_key = open('C:/Users/Tom/github/MoneyLosingMachine/key.txt').read()

ts = TimeSeries(key=API_key, output_format='pandas')
print('Key accepted')

#user_input = input('Request new data? (y/n)')
user_input = 'n'
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

data.columns = ['open', 'high', 'low', 'close', 'volume']
data['TradeDate'] = data.index.date
data['time'] = data.index.time

fig, ax = plt.subplots(nrows=1, ncols=1)
ax.plot(data[data['TradeDate']>datetime.date(2021, 1, 1)]['close'])


simple_jack = bots.simple_jack()
#for date in pd.date_range(start="2020-01-01",end="2020-07-01"):
action_info = np.empty((0,3))
for date in pd.date_range(start="2021-01-01", end=data['TradeDate'].max()):
    if not data[data['TradeDate']==date].empty:
        action = simple_jack.execute_strategy(data[data['TradeDate']<=date], date)
        #price = daily_data[daily_data['TradeDate']==date]['close'][-1]
        action_info = np.vstack((action_info, np.array([date, action[0], action[1]])))

print('Total profit: $ {0:.2f}'.format(simple_jack.balance))

buy_dates = action_info[:,0][np.where(action_info[:,1]=='buy')[0]]
sell_dates = action_info[:,0][np.where(action_info[:,1]=='sell')[0]]

ax.scatter(buy_dates, data.loc[buy_dates]['close'], marker='^', color='g')
ax.scatter(sell_dates, data.loc[sell_dates]['close'], marker='v', color='r')

plt.show()
