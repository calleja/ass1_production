#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Controller class to the equity trading platform
"""

import sys
#sys.path.append('/home/lechuza/Documents/CUNY/data_607/assignment1/ass1_fromWork')
#sys.path.append('/home/tio/Documents/CUNY/advancedProgramming/ass1_fromWork')
sys.path.append('/usr/src/app/PROJECT_FOLDER')
import tradeClass as trade
import ass1_acountsClass as accts
import tradeManager as tm
import engageUser as eu
import yahoo_scraper_cleaner as scraper

def main():
    ''' building console interaction '''
    engage=eu.Dialogue()
    engage.engageUser()

if __name__ == "__main__":
    # execute only if run as a script
    main()