# Python 3.9.6
"""
Created 25/07/2021

This file will hold the various trading bots.

@author: Tom Ronayne
"""

import numpy as np

class daily_trading_bot:
    """
    I've decided to give the traders (children of this class) human names, as it
    would be challenging to give each different bot a name that adequately describes
    their strategy.
    """

    def __init__(self, balance=0):
        self.balance = balance
        self.shares = 0

    def buy(self, daily_data, date, number_of_shares):
        price = daily_data[daily_data['TradeDate']==date]['close'][-1]
        self.balance -= price*number_of_shares
        self.shares += number_of_shares
        #print("Bought {0} shares for $ {1} total on {2}".format(number_of_shares, price*number_of_shares, date.date()))

    def sell(self, daily_data, date, number_of_shares):
        price = daily_data[daily_data['TradeDate']==date]['close'][-1]
        self.balance += price*number_of_shares
        self.shares -= number_of_shares
        #print("Sold {0} shares for $ {1} total on {2}".format(number_of_shares, price*number_of_shares, date.date()))



class simple_jack(daily_trading_bot):
    """
    Simple jack is a type of day trader that will use a very simple strategy.
    """

    def execute_strategy(self, daily_data, date):
        price = daily_data[daily_data['TradeDate']==date]['close'][-1]
        if price < 29:
            self.buy(daily_data, date, 1)
            # giving this function a return code gives us a way to see what the
            # bot is doing without relying on print statements
            return 'buy', 1
        elif (price > 31) and (self.shares >= 1):
            self.sell(daily_data, date, 1)
            return 'sell', 1
        else:
            return '', 0

class marvin(daily_trading_bot):
    """
    Marvin will use a moving average (mav) to determine what to do.
    """

    def execute_strategy(self, daily_data, date):
        price = daily_data['close'][0]
        # expect errors if we don't give this bot a 10 day head start on data
        # in our implementation, the moving average lags behind the market
        moving_average_period = 10
        moving_average = np.mean(daily_data['close'][0:moving_average_period])
        if (price-moving_average < -1) and (self.balance > price):
            # giving this function a return code gives us a way to see what the
            # bot is doing without relying on print statements
            self.buy(daily_data, date, self.balance//price)
            return 'buy', 1
        elif (price-moving_average > 1) and (self.shares >= 1):
            self.sell(daily_data, date, self.shares)
            return 'sell', 1
        else:
            return '', 0
