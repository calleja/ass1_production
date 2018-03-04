#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Client dialogue
"""
import sys
sys.path.append('/usr/src/app/PROJECT_FOLDER')
sys.path.append('/home/lechuza/Documents/CUNY/data_607/assignment1/ass1_fromWork')
sys.path.append('/home/tio/Documents/CUNY/advancedProgramming/ass1_fromWork')
import tradeClass as trade
import ass1_acountsClass as accts
import datetime as datetime
import tradeManager as tm
import yahoo_scraper_cleaner as scraper

class Dialogue(object):
    def __init__(self):
        self.todayTrading=tm.TradingDay()
        #create a new account/portfolio
        self.act=accts.Account()
    
    def engageUser(self):
        menuSelection=input('Please select from the list of options below.\n a -Trade\n b - Show Blotter\n c- Show P/L\n d - Quit\n > ')
        if menuSelection=='a':
            self.prepareTrade()
        elif menuSelection=='b':
            #call the blotter from the tradeManager class - may need rendering in this class, and the return value from either this function or another in this class can be handled at the controller level
            # TODO print('call blotter function')
            #the blotter function will return a list of dictionaries, or perhaps a pandas dataframe, that I'll then print... if extensive formating is required, I'll do it in this class
            print(self.todayTrading.prettyPrintTradeLog())
            return(self.engageUser())
        elif menuSelection=='c':
            
            print('your current portfolio is below... p&l calc is pending')
            self.calcPL()
            
            return self.engageUser()
        elif menuSelection=='d':
            return
        else:
            print('please select an option')
            self.engageUser()
    
    
    def prepareTrade(self):
            agg_dic={}            
            #dictionary of trade stats to send over to the tradeClass
            stockTrade=input('Which stock would you like to trade?\n a - Apple / AAPL\n b - Amazon / AMZN\n c- Microsoft / MSFT\n d - Snap Chat / SNAP\n e - Intel Corp / INTC\n > ')
            stock_dic={'a':'AAPL','b':'AMZN','c':'MSFT','d':'SNAP','e':'INTC'}
            try:
                #store ticker symbol in the final dictionary
                agg_dic['ticker']=stock_dic[stockTrade]
            except KeyError:
                print('incorrect selection')
                #start over
                self.engageUser()
            
            tradeDirection=input('Would you like to\n a- buy\n b- sell to close\n c -short\n d- buy to close?\n > ') #drives whether we calculate using bid or ask
            
            #a lookup dictionary
            options={'a':'buy','b':'sell to close','c':'short','d':'buy to close'}
            
            try:
                #store tradetype entry in the final dictionary
                agg_dic['tradetype']=options[tradeDirection]
            except KeyError:
                print('incorrect selection')
                self.engageUser()
                
            qty=float(input('How many shares would you like to trade?\n > '))
            agg_dic['shares']=qty    
            agg_dic['timestamp']=datetime.datetime.now()
            #call the yahoo scraper... then call TradeManager which calls TradeClass... actually - have the option to call the yahoo scraper from the TradeManager object.
            s=scraper.Scrapy()
            price_dict=s.rtYhoDats(stock_dic[stockTrade])
            
            #select the appropriate price according to the trade type: buy on ask and sell on the bid
            map_bid_ask={'a':'ASK','b':'BID','c':'BID','d':'ASK'}
            agg_dic['price']=price_dict[stock_dic[stockTrade]][map_bid_ask[tradeDirection]]
            
            #The user is then asked to confirm the trade at the market ask price scraped from Yahoo.
            cont=input('You can transact at {}. Would you like to continue y/n?\n > '.format(agg_dic['price']))
            
            if cont=='y':
                #send over this data to the tradeClass or can return a dictionary
                print('Your trade is being processed')
                #acount object has now been updated at the highest scope
                #trade.EquityTrade(agg_dic,self.act)
                print(agg_dic)
                
                #TODO discover the error below, an invalid trade is being sent to act.CheckIfNew, but should die at the tradeClass... ensure that the call to makeTrade() encounters the invalid trade error... enforce that the thrown error reaches this object
                
                try:
                    single_trade_dic=self.todayTrading.makeTrade(agg_dic,self.act)
                    #makeTrade() calls tradeClass.tradeType() which QAs the trade, determines the original tradetype (long/short) and calculates the delta on position size and imapct to cash
                    print(single_trade_dic) #TODO printing None
                
                #TODO this is the portion that is explicitly throwing the error... error states that single_trade_dic is empty
                    self.act.postEquityTrade(single_trade_dic)
                #keep the session going until the user quits
                    self.engageUser()
                except ValueError:
                    print('try a valid trade')
                    self.engageUser()
            else:
                self.engageUser()
            
    def calcPL(self):
        #call scraper, pass dictionary of current prices to the account object and print the current status of the portfolio dictionary, equipped with both realized and unrealized p+l
        s=scraper.Scrapy()
        ahora=s.rtYhoDats()
        sorted_list=self.todayTrading.sortTrades()
        return(print(self.act.calcUPL(ahora,sorted_list)))
            
