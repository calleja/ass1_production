#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Account class...
This object will have attributes like cash and positions and will need to allow for retrieval methods and some minor calculations of each (unless it can be done in the trade/transaction class). This object must persist throughout the trading session.

Positions must store total shares, average price, possibly VWAP
In addition, store cash amount; keep in mind that short positions do not affect cash balance.
"""
import pandas as pd

class Account:
    def __init__(self):
        self.cash_bal=1000000
        #will be a nested dictionary, the outermost key is the ticker and the value will be a dictionary of total shares, average price and possibly VWAP, realized p/l... ex: {ticker:{'notional':notaionValue,'direction':direction_string, etc...}}
        self.positions={'AAPL':{'shares':0,'vwap':0,'realized_pl':0,'notional':0,'original_direction':'','upl':0},
                        'INTC':{'shares':0,'vwap':0,'realized_pl':0,'notional':0,'original_direction':'','upl':0},
                        'MSFT':{'shares':0,'vwap':0,'realized_pl':0,'notional':0,'original_direction':'','upl':0},
                        'SNAP':{'shares':0,'vwap':0,'realized_pl':0,'notional':0,'original_direction':'','upl':0},
                        'AMZN':{'shares':0,'vwap':0,'realized_pl':0,'notional':0,'original_direction':'','upl':0}}
        
        
    def getCash(self):
        print('cash balance is :'+str(self.cash_bal))
        return self.cash_bal
    
    def getPortfolio(self):
        return(self.positions)
    
    def updateTickersOwned(self):
        #could also just get the keys from the dictionary
        self.tickers=self.position.keys()
        
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
            #calculate the number of shares in portfolio
        self.positions[dic['ticker']]['shares']=dic['position_delta']+self.positions[dic['ticker']]['shares']    
        #calculate notional of shares held
        self.positions[dic['ticker']]['notional']=self.positions[dic['ticker']]['shares']*self.positions[dic['ticker']]['vwap']
        #calculate the cash position after the trade
        self.cash_bal=dic['cash_delta']+self.cash_bal
        
        #tracking the original_tradetype
        
        #clean up the portfolio if there are no positions
        if self.positions[dic['ticker']]['shares']==0:
            self.positions[dic['ticker']]['original_direction']=''
            self.positions[dic['ticker']]['vwap']=0
        else:
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
        elif (self.positions[dic['ticker']]['vwap']==0 and  abs(self.positions[dic['ticker']]['shares']+dic['position_delta'])>=abs(self.positions[dic['ticker']]['shares'])):
            newVWAP=(self.positions[dic['ticker']]['notional']+dic['notional_delta'])/(self.positions[dic['ticker']]['shares']+dic['position_delta'])
            self.positions[dic['ticker']]['vwap']=newVWAP    
        else:
            return
        
    def calcRealizedPL(self,dic):
        #requires a calculated VWAP... realized PL = notional on transaction - VWAP * same # of shares, so price is not necessary
        if(self.positions[dic['ticker']]['original_direction']==dic['original_tradetype'] and abs(self.positions[dic['ticker']]['shares']+dic['position_delta'])<self.positions[dic['ticker']]['shares']):
            #'notional_delta' is negative for sales
            self.positions[dic['ticker']]['realized_pl']=-dic['notional_delta']+self.positions[dic['ticker']]['vwap']*dic['position_delta']+self.positions[dic['ticker']]['realized_pl']
            
    def calcUPL(self,dictOfPrices,sortedList):
        #dictOfPrices = output from scrape class; format: {ticker as str:price as float}
        #calc = portfolio for >0 holdings: current market price*shares held - VWAP*shares held  
        total_notional=0
        
        for k,v in self.positions.items():
            #retrieve price
            self.positions[k]['upl']=dictOfPrices[k]*v['shares']-v['vwap']*v['shares']
            g=dictOfPrices[k]*v['shares']
            self.positions[k]['notional']=g
            total_notional+=g 
         
         #calculate the total size of portfolio: cash + notional
        self.portfolio_value=self.cash_bal+total_notional
        cash_line=('cash',self.cash_bal,self.portfolio_value)
        sorted_df=self.sortPositions(sortedList) 
        print(sorted_df)
        #TODO cash_line will need to conform to the table structure: with index "cash" and blank values for WAP, UPL and RPL... ensure that RPL persists after the position in the stock was liquidated
        print(cash_line)
        
    
    def sortPositions(self,sortedList):
        df=pd.DataFrame.from_dict(self.positions,orient='index')
        #sort the dataframe by its index
        return(df.reindex(sortedList))
        
        
