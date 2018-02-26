#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exract price and time for the stock

Which stock would you like to trade?\n a - Camden Property Trust / CPT\n b - Delta Airlines / DAL\n c- Apache / APC\n d - Con Edison / ED\n e - Citigroup / C\n
"""

from bs4 import BeautifulSoup as bs
import requests
import re

#stock1 CPT
class Scrapy(object):
    
    def __init__(self):
        
        self.uni_dic={'CPT':'https://finance.yahoo.com/quote/CPT?p=CPT','ED':'https://finance.yahoo.com/quote/ED?p=ED','DAL':'https://finance.yahoo.com/quote/DAL?p=DAL','APC':'https://finance.yahoo.com/quote/APC?p=APC','C':'https://finance.yahoo.com/quote/C?p=C'}
        #universe of stocks for our purposes
        
    def rtYhoDats(self,stocks=None):
    #retrieve Yahoo data; function should work with a dictionary... yahoo_dict is a dictionary of dictionaries... stocks is a ticker, I'll use that to index the dictionary
        if stocks is None:
            #facilitate a dictionary if something else is passed
            stocks=self.uni_dic
            
        else: #make a dictionary with a singleton
            stocks={stocks:self.uni_dic[stocks]}
            
        #call the next function            
        return(self.topLineScrape(stocks))
        
    def topLineScrape(self,stocks):
        #entire dictionary, regardless of # of elements, is passed this argument
        yahoo_dict={}
        keys_len=len(stocks.keys())
        
        if keys_len>1: #the parsing function is different depending whether we need to retrieve prices for p&l or single trades
            for k,v in stocks.items():
                yahoo_pg=requests.get(v)
                stock_html=yahoo_pg.text
                stock_soup =bs(stock_html,'html.parser')
                #set the key to a single element: a float
                yahoo_dict[k]=self.wholePortfolio(k,stock_soup)
        else:
            for k,v in stocks.items():
                yahoo_pg=requests.get(v)
                stock_html=yahoo_pg.text
                stock_soup =bs(stock_html,'html.parser')
                #below returns a dictionary w/bid & ask
                yahoo_dict=self.singleton(k,stock_soup)
        
        return yahoo_dict
    
    def singleton(self,k,stock_soup):
            #remember that dictionaries do not maintain
        yh_dict={}
        quote=stock_soup.find_all('div',{'id':'quote-header'})
        yh_dict.setdefault(k,{})
                #k is a ticker
                #call the parser, which returns a dictionary of bid and ask for the stock
        yh_dict[k]=self.parseText(quote)
        return(yh_dict)
    
    def wholePortfolio(self,k,stock_soup):
        quote=stock_soup.find_all('div',{'id':'quote-header-info'})
        #a single price as a float
        return(self.parseTextForPortfolio(quote))
            
    def parseText(self,extract):
            #parse the price text and return a dictionary of the bid and ask... this dictionary will be nested into the ticker dictionary
        mini_dict={}
        for i in extract:
            mini_dict['ASK']=self.lowerParse(i.find('td',{'data-test':'ASK-value'}).get_text())
            mini_dict['BID']=self.lowerParse(i.find('td',{'data-test':'BID-value'}).get_text())
        return(mini_dict)
        
    def lowerParse(self,price_text):
        price=re.search(r'.*?(?: )',price_text)
        price_float=float(price.group(0))
        return(price_float)
        
    def parseTextForPortfolio(self,extract):
        #extract last market price... for portfolio-wide scrapes
        stats=[]
        for i in extract:
    #print(i)
            contents=i.find_all({'div':{'class':'smartphone_Mt'}})
            for c in contents:
                for g in c.find_all({'div':{'class':'D(ib'}}):
                    for h in g.find_all({'span':{'class':'Trsdu'}}):
                        stats.append(h.text)
        try:
            return(float(stats[3]))
        except IndexError:
            #TODO handle the error... nothing is at times returned from the scrape
            print("we are running the scrape again")
            self.rtYhoDats()
            
