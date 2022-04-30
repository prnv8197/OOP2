#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 21:40:10 2022

@authors: Pranav Atulya, Akshay Joshi, 
"""

import requests
from backtest_oop import backtest
from strat_oop import run

import os

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'clear'
    os.system(command)

myuser = ['rootuser', 'pranav', 'akshay', 'aditi']
mypass = ['rootpass']

# Class for hitting a dummy broker api and authenticating user
class BrokerConnection:
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
    def validation(self, username, password):
        return ((self.username in myuser and self.password in mypass))
            

    # Instance method
    def createconnection(self):
        query = {'Username': self.username, 'Password': self.password}
        response = requests.get('http://api.open-notify.org/astros.json', query)
        if(response.status_code == 200):
            return f"Broker connection successful for username: {self.username}"
        else:
            return f"Some error occured, try again."


class RunStrat:
    def run(self):
        return run()
        
        
print("Starting System")  
print("Please enter username")
username = input()
print("Please enter password")
password = input()

# Creating object for establishing connection

StartConnection = BrokerConnection(username, password)
if(StartConnection.validation(username,password)):
    print(StartConnection.createconnection())
    clearConsole()
    print("Running analysis on S&P500 stocks")
    print("Please be patient, the analysis will take 4-5mins based on API response rate")
    RunAnalysis = RunStrat()
    RunAnalysis.run()
else:
    print("\n","Invalid credentials, please try again")



