#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Controller class for the trading application
"""

import sys
sys.path.append('/home/lechuza/Documents/CUNY/data_607/assignment1/ass1_fromWork')
sys.path.append('/home/tio/Documents/CUNY/advancedProgramming/ass1_fromWork')
import tradeClass as trade
import ass1_acountsClass as accts
import datetime as datetime
import tradeManager as tm
import engageUser as eu
import yahoo_scraper_cleaner as scraper
import pandas as pd
import pprint
from imp import reload

reload(trade)
reload(accts)
reload(eu)
reload(scraper)

act=accts.Account()



#4 pieces of information needed: ticker, timestamp, price, trade type and original trade type
buy_trade={'ticker':'CPT','price':98.108,'shares':1000,'timestamp':datetime.datetime.today(),'tradetype':'buy','original_tradetype':'long'}

buy_trade_2={'ticker':'HD','price':78.108,'shares':1000000,'timestamp':datetime.datetime.today(),'tradetype':'buy','original_tradetype':'long'}
sell_trade_dic={'ticker':'HD','price':102.108,'shares':1000,'timestamp':datetime.datetime.today(),'tradetype':'sell to close','original_tradetype':'long'}

short_trade_dic={'ticker':'RLS','price':67.108,'shares':1000,'timestamp':datetime.datetime.today(),'tradetype':'short','original_tradetype':'short'}
btc_trade_dic={'ticker':'RLS','price':69.108,'shares':1000,'timestamp':datetime.datetime.today(),'tradetype':'buy to close','original_tradetype':'short'}

tup=short_trade_dic,
tup=tup+(btc_trade_dic,)

#initiate trading day object and pass all trades through the object in order to log it
todayTrading=tm.TradingDay()

#using the new tradeManager framework
buy_test_today=todayTrading.makeTrade(buy_trade,act)

#following along the tradeClass object... instantiation does not affect the portfolio
buy_test=trade.EquityTrade(buy_trade,act)
buy_test_2=trade.EquityTrade(buy_trade_2,act)
sell_test=trade.EquityTrade(sell_trade_dic,act)
short_test=trade.EquityTrade(short_trade_dic,act)
short_test.tradetype

#testing only the tradeClass class and circumventing tradeManager class
buy_test_dict=buy_test.tradeType()
buy_test_dict2=buy_test_2.tradeType()
sell_test_dict=sell_test.tradeType()
#nothing is being returned here
short_test_dict=short_test.tradeType()

#update the portfolio
act.postEquityTrade(buy_test_dict)
act.postEquityTrade(short_test_dict)
act.getPortfolio()
act.cash_bal

buy_dict=buy_test_today.tradeType()
buy_dict2=buy_test_2.tradeType()
sell_dict=sell_test.tradeType()
short_dict=short_test.tradeType()

act.postEquityTrade(buy_dict)
act.postEquityTrade(buy_dict2)
act.postEquityTrade(short_dict)

act.getPortfolio()
act.cash_bal
cashAfterPurchase=act.getCash()

''' building console interaction '''
engage=eu.Dialogue()
engage.engageUser()

#trade has been logged into the account object successfuly
engage.act.getPortfolio()
engage.act.cash_bal
''' test the scraper function '''
s=scraper.Scrapy()
amzn=s.rtYhoDats('AMZN')
todo=s.rtYhoDats()

one_dic={'side':'buy','ticker':'APC','quantity':1000,'executed price':67.89,'execution timestamp':datetime.datetime.strptime('2016-01-01',"%Y-%m-%d"),'original_tradetype':'long','position_delta':1000}
one_dic.keys()
''' test the p&l class '''
#version with no short positions... is qty neg or positive?
fakeTrades1=(
{'side':'buy','ticker':'INTC','quantity':1000,'executed price':67.89,'execution timestamp':datetime.datetime.strptime('2016-01-01',"%Y-%m-%d"),'original_tradetype':'long','position_delta':1000},
{'side':'buy','ticker':'DAL','quantity':400,'executed price':89.23,'execution timestamp':datetime.datetime.strptime('2016-01-01',"%Y-%m-%d"),'original_tradetype':'long','position_delta':400},
{'side':'sell to close','ticker':'AAPL','quantity':500,'executed price':69.8,'execution timestamp':datetime.datetime.strptime('2017-01-01',"%Y-%m-%d"),'original_tradetype':'long','position_delta':-500},
{'side':'buy','ticker':'AAPL','quantity':200,'executed price':65,'execution timestamp':datetime.datetime.now(),'original_tradetype':'long','position_delta':200},
{'side':'sell to close','ticker':'APC','quantity':500,'executed price':62.45,'execution timestamp':datetime.datetime.strptime('2018-01-01',"%Y-%m-%d"),'original_tradetype':'long','position_delta':-500})

df=pd.DataFrame(list(fakeTrades1))
df.reindex([0,1,2,3,4,])
df
new_order=[2,0,1,4,3]
df.reindex(new_order)
df



def sortTrades(df):
        #place tickers of trades in a pandas df of ticker and timestamp; groupBy ticker and select for the latest timestamp, then sort by timestamp

        g=df.groupby('ticker').apply(lambda x: x['execution timestamp'].max())

        g.sort_values(ascending=False,inplace=True)
        traded_ticks=g.index.tolist()
        universe=['AMZN','AAPL','SNAP','INTC','MSFT']
        [traded_ticks.append(x) for x in universe if x not in traded_ticks]
        return(traded_ticks)
    
sortTrades(df)

a.groups
for name, group in a:
    print(name)
    print(group)
    
#selecting a particular group... the key of the group is a tuple... call the group by its key... this returns a dataframe!
df_test=a.get_group(('APC','long'))    


positions={'AAPL':{'shares':0,'vwap':0,'realized_pl':0,'notional':0,'original_direction':'','upl':0},
                        'INTC':{'shares':0,'vwap':0,'realized_pl':0,'notional':0,'original_direction':'','upl':0},
                        'MSFT':{'shares':0,'vwap':0,'realized_pl':0,'notional':0,'original_direction':'','upl':0},
                        'SNAP':{'shares':0,'vwap':0,'realized_pl':0,'notional':0,'original_direction':'','upl':0},
                        'AMZN':{'shares':0,'vwap':0,'realized_pl':0,'notional':0,'original_direction':'','upl':0}}

pd.DataFrame.from_dict(positions,orient='index')
