#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 18:17:59 2020

@author: philip & robin
""" 

import pandas as pd
from datetime import datetime, timedelta 


pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
    
print('(1/9) start importing the csv')
df = pd.read_csv("~/Downloads/Crimes_-_2001_to_present.csv", low_memory=False)
df = df.dropna()

#Filtere für die passenden Spalten
print('(2/9) filter Columns')
columns = ['Date', 'Block', 'Primary Type', 'Description', 'Location Description', 'Year']
df = pd.DataFrame(df, columns=columns)

#Teile das Datum in eigene Spalten ein
print("(3/9) split date")
df[['Date','time', 't']] = df['Date'].str.split(' ',expand=True)

#Passe die Blockspalte an
print("(4/9) customize the block column")
df['Block'].replace(r'^\d\d\d\w\w\s\w\s', ' ', inplace=True, regex=True)

#Passe die Datumspalte an
print("(5/9) customize the date")
day_name= ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag','Sonntag']
month_name= ['Januar', 'Februar', 'März', 'April', 'Mai','Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
df["weekday"] = df["Date"].apply(lambda x: day_name[datetime.strptime(x, '%m/%d/%Y').weekday()])
df[['month', 'day', 'year']] = df['Date'].str.split('/',expand=True)
df["month"] = df["month"].apply(lambda x: month_name[int(x)-1])

#Entferne Komma in der Location Spalte
print("(6/9) customize the location")
df['Location Description'].replace(r', ', ' - ', inplace=True, regex=True)

#Passe die Zeit zu deutschem Format an
print("(7/9) some more date things")
df["time"] = df.apply((lambda x: format(datetime.strptime(x.time, '%H:%M:%S') + timedelta(hours=12),'%H') if "PM" in x.t else format(datetime.strptime(x.time, '%H:%M:%S'), '%H')), axis=1)

columns = ['time', 'Block', 'Primary Type', 'Description', 'Location Description', 'Year', 'month', 'weekday', 't']
df = pd.DataFrame(df, columns=columns)
print("(8/9) start preparing for printing")
print(df)

print('(9/9) start saving as csv')
df.to_csv('7mioCrimes.csv', index=False)

print("Finished")