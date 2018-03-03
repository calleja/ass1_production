#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 13:54:27 2018

@author: tio
"""
import sys
sys.path.append('/home/tio/Documents/CUNY/advancedProgramming/production/ass1_production')
import yahoo_scraper_cleaner as scraper
import imp
imp.reload(scraper)

s=scraper.Scrapy()
ahora=s.rtYhoDats()
print(act.calcUPL(ahora))