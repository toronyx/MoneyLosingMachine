# Python 3.9.6
"""
Created 25/07/2021

This file will hold the various trading bots.

@author: Tom Ronayne
"""

class daily_trading_bot:
    """
    I've decided to give the traders (children of this class) names, as it would
    be challenging to give each different bot a name that adequately describes
    their strategy.
    """

    def __init__(self):
        self.balance = 0
        self.shares = 0

    def buy(self, daily_data, date, number_of_shares):
        price = daily_data[daily_data['TradeDate']==date]['close'][-1]
        self.balance -= price*number_of_shares
        self.shares += number_of_shares
        print("Bought {0} shares for $ {1} total on {2}".format(number_of_shares, price*number_of_shares, date.date()))

    def sell(self, daily_data, date, number_of_shares):
        price = daily_data[daily_data['TradeDate']==date]['close'][-1]
        self.balance += price*number_of_shares
        self.shares -= number_of_shares
        print("Sold {0} shares for $ {1} total on {2}".format(number_of_shares, price*number_of_shares, date.date()))



class simple_jack(daily_trading_bot):
    """
    Simple jack is a type of day trader that will use a very simple strategy.
    """

    def execute_strategy(self, daily_data, date):
        price = daily_data[daily_data['TradeDate']==date]['close'][-1]
        if price < 29:
            self.buy(daily_data, date, 1)
        if (price > 31) and (self.shares >= 1):
            self.sell(daily_data, date, 1)
