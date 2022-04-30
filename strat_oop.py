#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 23:19:30 2022

@author: pranav.atulya
"""

import pandas as pd

import smtplib, ssl
from email.mime.text import MIMEText
from getData import getOHLC
from OLS import OLS_max, regression_channel
from time import time, sleep
from datetime import datetime
from getIndicators import *
from tabulate import tabulate
from tqdm import tqdm
from backtest_oop import backtest






#-------------------------------------------------------------------------------------------#

def run():
    pd.set_option('display.max_rows', 1000)
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.width', 1000)
    
    names_us = pd.read_csv(r"constituents.csv")
    names_ind = pd.read_csv(r"futuresList.csv")
    mylist = names_us['Symbol'].tolist()
    
    
    
    
    suff = ''
    
    
     #SMA50>UpperBoll BUY; SMA50<LowerBoll SELL
    Speriod = '1mo'
    Sinterval = '15m'
    target_pct = 0.01      
    amount = 10000
    
    resLong = pd.DataFrame(columns = ['Stock', '%Chg', 'Qty', 'Target Price', 'Expected return%'])
    resShort = pd.DataFrame(columns = ['Stock', '%Chg','Qty', 'Target Price', 'Expected return%'])
    for i in tqdm(mylist[:]):    
        # print(i)
        price = getOHLC(i, period = Speriod, interval = Sinterval, suffix = suff)
        # price = price[0:len(price)-8]
        price = getBollingerBands(price)
        price = getMACD(price)
        price['50SMA'] = price['Close'].rolling(window = 50).mean()
        
        macd_mean = price['signal_line'].mean()
        macd_dev = price['signal_line'].std()
        if(price['50SMA'][-1] > price['Upper Band'][-1] and price['signal_line'][-1] < macd_mean-1*macd_dev):
            price_d = getOHLC(i, period = Speriod, interval = '1d', suffix = suff)
            price_s = getOHLC(i, period = Speriod, interval = '5m', suffix = suff)
            flag_5m = price_s['Close'].rolling(window = 50).mean()[-1] < price_s['Close'][-1]
            ols_m = round(OLS_max(price), 2)
            price = regression_channel(price)
            backtest_ret = backtest(i)
            
            resLong = resLong.append({'Stock':i, '%Chg': round((price_d['Close'][-1]/price_d['Close'][-2]-1)*100,2), 'Qty': int(amount/price['Close'][-1]), 'Target Price': round((1-target_pct)*price['Close'][-1], 2), 'Expected return%': backtest_ret}, ignore_index=True)
            
        if(price['50SMA'][-1] < price['Lower Band'][-1] and price['signal_line'][-1] > macd_mean+1*macd_dev): 
            price_d = getOHLC(i, period = Speriod, interval = '1d', suffix = suff)
            price_s = getOHLC(i, period = Speriod, interval = '5m', suffix = suff)
            flag_5m = price_s['Close'].rolling(window = 50).mean()[-1] > price_s['Close'][-1]
            ols_m = round(OLS_max(price), 2)
            price = regression_channel(price)
            backtest_ret = backtest(i)
            
            resShort = resShort.append({'Stock':i, '%Chg': round((price_d['Close'][-1]/price_d['Close'][-2]-1)*100,2), 'Qty': int(amount/price['Close'][-1]), 'Target Price': round((1-target_pct)*price['Close'][-1], 2), 'Expected return%': backtest_ret}, ignore_index=True)
            
    print('\n', "Go Long", '\n',tabulate(resLong.sort_values("Expected return%", ascending=False)[:10], headers='keys', tablefmt='psql'), '\n')  
    print("Go Short",'\n',tabulate(resShort.sort_values("Expected return%", ascending=False)[:10], headers='keys', tablefmt='psql'), '\n')  
    
    
    