#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Account class...
This object will have attributes like cash and positions and will need to allow for retrieval methods and some minor calculations of each (unless it can be done in the trade/transaction class). This object must persist throughout the trading session.

Positions must store total shares, average price, possibly VWAP
In addition, store cash amount; keep in mind that short positions do not affect cash balance.
"""

class Account:
    def __init__(self):
        self.cash_bal=1000000
        #will be a nested dictionary, the outermost key is the ticker and the value will be a dictionary of total shares, average price and possibly VWAP, realized p/l... ex: {ticker:{'notional':notaionValue,'direction':direction_string, etc...}}
        self.positions={}
        
    def getCash(self):
        print('cash balance is :'+str(self.cash_bal))
        return self.cash_bal
    
    def getPortfolio(self):
        return(self.positions)
    
    def updateTickersOwned(self):
        #could also just get the keys from the dictionary
        self.tickers=self.position.keys()
            
    def amend_cash(self,amend):
        self.cash=self.cash+amend
        
    def checkIfNew(self,dic):
        #checks whether there is a position in that stock and in the same direction
        if dic['ticker'] in self.positions.keys():
            if self.positions[dic['ticker']]['original_direction']==dic['original_tradetype']:
                return False
        else:
            #create an entry/holding in the portfolio for that stock at 0 notional and shares
            self.positions[dic['ticker']]={'shares':0,'notional':0,'original_direction':'','realized_pl':0}
            return True
        
        
    def postEquityTrade(self,dic):
        #dic will come from the tradeClass
        '''
  the dictionary will contain total number of shares and trade price... conditional statements will qualify whether the trade serves to: 
    a) open a new position - can be long or short
    b) close all or part of an existing position - long or short
    c) augment an existing position - short or long

this function will then instantiate a tradeClass object that will QA the trade (verify whether legal), then subsequently amend the current portfolio
'''
        #if the trade/position is new, create a new entry in the dictionary to not trigger errors
        isNew=self.checkIfNew(dic) #if the trade is in a new ticker, than no need to calculate realized pl
        if isNew:
            self.positions[dic['ticker']]['vwap']=dic['notional_delta']/dic['position_delta']
        else: #pre-existing position in the stock
            self.calcVWAP(dic) #function will determine whether VWAP is to be impacted, and if so, will update it
            self.calcRealizedPL(dic) #calclates realized PL if applicable
        self.positions[dic['ticker']]['shares']=dic['position_delta']+self.positions[dic['ticker']]['shares']    
        self.positions[dic['ticker']]['notional']=self.positions[dic['ticker']]['shares']*self.positions[dic['ticker']]['vwap']
        self.cash_bal=dic['cash_delta']+self.cash_bal
        
        #how to keep track of "new" trades - tracking the genesis trade
        self.positions[dic['ticker']]['original_direction']=dic['original_tradetype']
        #updat self.positions[ticker]['realized_pl'] with another application

    def calcVWAP(self,dic):
        #reconcile the new transaction to the previous portfolio stats... only applicable to position increasing transactions (buys for long positions and sales for shorts)
        #ticker will be in the dictionary... no need to check that... initial trade will not have a VWAP
        print("I'm reconciling the portfolio to this transaction dictionary:")
        #print(dic)
        if(self.positions[dic['ticker']]['original_direction']==dic['original_tradetype'] and  abs(self.positions[dic['ticker']]['shares']+dic['position_delta'])>abs(self.positions[dic['ticker']]['shares'])):
            newVWAP=(self.positions[dic['ticker']]['notional']+dic['notional_delta'])/(self.positions[dic['ticker']]['shares']+dic['position_delta'])
            self.positions[dic['ticker']]['vwap']=newVWAP
        else:
            return
        
    def calcRealizedPL(self,dic):
        #requires a calculated VWAP... realized PL = notional on transaction - VWAP * same # of shares, so price is not necessary
        if(self.positions[dic['ticker']]['original_direction']==dic['original_tradetype'] and abs(self.positions[dic['ticker']]['shares']+dic['position_delta'])<self.positions[dic['ticker']]['shares']):
            #'notional_delta' is negative for sales
            self.positions[dic['ticker']]['realized_pl']=-dic['notional_delta']+self.positions[dic['ticker']]['vwap']*dic['position_delta']+self.positions[dic['ticker']]['realized_pl']
            
    def calcUPL(self,dictOfPrices):
        #dictOfPrices = output from scrape class; format: {ticker as str:price as float}
        #calc = portfolio for >0 holdings: current market price*shares held - VWAP*shares held 
        #TODO I need to print the cash position, namely: the USD and sum of cash and notional value of all the current holdings... may need to store it all into a dataframe
        for k,v in self.positions.items():
            #retrieve price
            self.positions[k]['upl']=dictOfPrices[k]*v['shares']-v['vwap']*v['shares']
        return(self.positions)