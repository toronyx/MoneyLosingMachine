"""
Created 25/07/2021  Python 3.9.6

Main code.

@author: Tom Ronayne
"""

import bots
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf
import datetime
import time
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData

API_key = open('C:/Users/Tom/github/MoneyLosingMachine/key.txt').read()

ts = TimeSeries(key=API_key, output_format='pandas')
print('Key accepted')

ticker = 'EXC'

""" Read in data """

#user_input = input('Request new data? (y/n)')
user_input = 'y'
if user_input == 'y':
    print('Requesting Alpha Vantage data...')
    t0 = time.time()

    data, metadata = ts.get_daily(ticker, outputsize='full')
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

"""my_colors = mpf.make_marketcolors(up='lime',down='r',inherit=True)
my_style  = mpf.make_mpf_style(base_mpf_style='nightclouds',marketcolors=my_colors)
mpf.plot(data[data['TradeDate']>datetime.date(2021, 1, 1)],
         type='candle', style=my_style, mav=(7,21,50), volume=True, show_nontrading=True,
         title='{0} candle plot'.format(ticker))"""



""" Let the bots do their thing """

plt.style.use('dark_background')
fig, ax = plt.subplots(nrows=1, ncols=1)
ax.plot(data[data['TradeDate']>datetime.date(2021, 1, 1)]['close'])
ax.set_title('Close price for {0} ticker'.format(ticker))
ax.set_ylabel('Close price /\$')

current_bot = bots.marvin(balance=100) #simple_jack()

#for date in pd.date_range(start="2020-01-01",end="2020-07-01"):
action_info = np.empty((0,3))
moving_average = np.empty(0)
moving_average_period = 10
trading_dates = []
for date in pd.date_range(start="2021-01-01", end=data['TradeDate'].max()):
    if not data[data['TradeDate']==date].empty:
        action = current_bot.execute_strategy(data[data['TradeDate']<=date], date)
        action_info = np.vstack((action_info, np.array([date, action[0], action[1]])))
        trading_dates.append(date)

        # Note: keep in mind we are skipping days with no trades
        moving_average = np.append(moving_average, np.mean(data[data['TradeDate']<=date]['close'][0:moving_average_period]))

final_info = ('Cash balance: $ {0:.2f}, Stocks owned: {1:.0f} \n'
              +'Balance (inc. stocks): $ {2:.2f}').format(current_bot.balance, current_bot.shares,
                                                 current_bot.balance+current_bot.shares*data['close'][0])
print(final_info)

buy_dates = action_info[:,0][np.where(action_info[:,1]=='buy')[0]]
sell_dates = action_info[:,0][np.where(action_info[:,1]=='sell')[0]]

ax.scatter(buy_dates, data.loc[buy_dates]['close'], marker='^', color='g', label='buy')
ax.scatter(sell_dates, data.loc[sell_dates]['close'], marker='v', color='r', label='sell')
#ax.plot(pd.date_range(start="2021-01-01", end=data['TradeDate'].max()), moving_average, label='moving average')
ax.plot(trading_dates, moving_average, label='moving average')
ax.legend(title=final_info)

plt.show()
