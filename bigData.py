#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 18:17:59 2020

@author: philip & robin
""" 

import pandas as pd
from datetime import datetime, timedelta 
import time
import re

start_time = time.time()

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
    
print('(1/9) start importing the csv')
df = pd.read_csv("Crimes_-_2001_to_present_19042020.csv", low_memory=False)


#Filtere für die passenden Spalten
print('(2/9) filter Columns | Time previous Step: ', time.time() - start_time)
columns = ['Date', 'Block', 'Primary Type', 'Description', 'Location Description', 'Year']
df = pd.DataFrame(df, columns=columns)

#Teile das Datum in eigene Spalten ein
print("(3/9) split date | Time in Secounds: ", time.time() - start_time)
df[['Date','time', 't']] = df['Date'].str.split(' ',expand=True)

#Passe die Blockspalte an
print("(4/9) customize the block column | Time in Secounds: ", time.time() - start_time)
df['Block'].replace(r'^\d\d\d\w\w\s\w\s', ' ', inplace=True, regex=True)

#Passe die Datumspalte an
print("(5/9) customize the date | in Secounds: ", time.time() - start_time)
day_name= ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag','Sonntag']
month_name= ['Januar', 'Februar', 'Maerz', 'April', 'Mai','Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
df["weekday"] = df["Date"].apply(lambda x: day_name[datetime.strptime(x, '%m/%d/%Y').weekday()])
df[['month', 'day', 'year']] = df['Date'].str.split('/',expand=True)
df["month"] = df["month"].apply(lambda x: month_name[int(x)-1])

#Entferne Komma in der Location Spalte
print("(6/9) customize the location | Time in Secounds: ", time.time() - start_time)
df['Location Description'].replace(r', ', ' - ', inplace=True, regex=True)

#Passe die Zeit zu deutschem Format an
print("(7/9) some more date things | Time in Secounds: ", time.time() - start_time)
df["time"] = df.apply((lambda x: format(datetime.strptime(x.time, '%H:%M:%S') + timedelta(hours=12),'%H') if "PM" in x.t else format(datetime.strptime(x.time, '%H:%M:%S'), '%H')), axis=1)

print("--------------Adding Prefixes--------------- | Time previous Step: ", time.time() - start_time)
df["Block"] = df["Block"].replace(to_replace=r'^\s', value='bl_', regex=True) #hier ist das \s dabei, weil es mit nem Leerzeichen noch anfängt
df["Primary Type"] = df["Primary Type"].replace(to_replace=r'^', value='pr_', regex=True)
df["Description"] = df["Description"].replace(to_replace=r'^', value='de_', regex=True)
df["Location Description"] = df["Location Description"].replace(to_replace=r'^', value='lo_', regex=True)

#Entferne Ähnlichkeiten
print("--------------Remove Similarities------------- | Time previous Step: ", time.time() - start_time)
#df["Primary Type"] = df["Primary Type"].replace("pr_CRIM SEXUAL ASSAULT", "pr_CRIMINAL SEXUAL ASSAULT") #geprüft3004
#df["Primary Type"] = df["Primary Type"].replace(["pr_NON - CRIMINAL", "pr_NON-CRIMINAL (SUBJECT SPECIFIED)" ], "pr_NON-CRIMINAL") #geprüft3004

#Stand 3004 von 213 auf 144 bei Location Description
df["Location Description"] = df["Location Description"].replace(to_replace=r'^lo_AIRPORT.+', value='lo_AIRPORT', regex=True) #geprüft3004 von 213 auf 201 
df["Location Description"] = df["Location Description"].replace(to_replace=r'\s*/\s*', value=' ', regex=True) ##geprüft3004 von 213 auf 198  
df["Location Description"] = df["Location Description"].replace("lo_BAR OR TAVERN", "lo_TAVERN") ##geprüft3004 von 213 auf 212
df["Location Description"] = df["Location Description"].replace(to_replace=r'^lo_CHA.+', value='lo_Chicago Housing Authority', regex=True) #geprüft3004 von 213 auf 201 

df["Location Description"] = df["Location Description"].replace("lo_DRIVEWAY - RESIDENTIAL", "lo_DRIVEWAY") ##geprüft3004 von 213 auf 212
df["Location Description"] = df["Location Description"].replace(["lo_FACTORY / MANUFACTURING BUILDING","lo_FACTORY/MANUFACTURING BUILDING"], "lo_FACTORY") ##geprüft3004 von 213 auf 211
df["Location Description"] = df["Location Description"].replace("lo_GARAGE/AUTO REPAIR", "lo_GARAGE") ##geprüft3004 von 213 auf 212
df["Location Description"] = df["Location Description"].replace("lo_GARAGE/AUTO REPAIR", "lo_GARAGE") ##geprüft3004 von 213 auf 212
df["Location Description"] = df["Location Description"].replace(["lo_GOVERNMENT BUILDING / PROPERTY","lo_GOVERNMENT BUILDING/PROPERTY"], "lo_GOVERNMENT BUILDING") ##geprüft3004 von 213 auf 211
df["Location Description"] = df["Location Description"].replace(to_replace=r'^lo_OTHER.+', value='lo_OTHER', regex=True) #geprüft3004 von 213 auf 209
df["Location Description"] = df["Location Description"].replace(to_replace=r'^lo_PARKING LOT.+', value='lo_PARKING LOT', regex=True) #geprüft3004 von 213 auf 211
df["Location Description"] = df["Location Description"].replace(to_replace=r'^lo_RESIDENCE.+', value='lo_RESIDENCE', regex=True) #geprüft3004 von 213 auf 208
df["Location Description"] = df["Location Description"].replace("lo_RESIDENTIAL YARD (FRONT/BACK)", "lo_RESIDENCE") ##geprüft3004 von 213 auf 212
df["Location Description"] = df["Location Description"].replace("lo_RIVER BANK", "lo_RIVER") ##geprüft3004 von 213 auf 212
df["Location Description"] = df["Location Description"].replace("lo_POOL ROOM", "lo_POOLROOM") ##geprüft3004 von 213 auf 212
df["Location Description"] = df["Location Description"].replace(to_replace=r'^lo_SCHOOL.+', value='lo_SCHOOL', regex=True) #geprüft3004 von 213 auf 205
df["Location Description"] = df["Location Description"].replace("lo_TAXI CAB", "lo_TAXICAB") ##geprüft3004 von 213 auf 212
df["Location Description"] = df["Location Description"].replace(to_replace=r'^lo_VEHICLE.+', value='lo_VEHICLE', regex=True) #geprüft3004 von 213 auf 205

df["Description"] = df["Description"].replace(to_replace=r'^de_AGG\s', value='AGGRAVATED ', regex=True) 
df["Description"] = df["Description"].replace(to_replace=r'^de_AGG.\s', value='AGGRAVATED ', regex=True) 
df["Description"] = df["Description"].replace(to_replace=r'^de_AGG:\s', value='AGGRAVATED ', regex=True) 
df["Description"] = df["Description"].replace(to_replace=r'^de_AGG:\s', value='AGGRAVATED ', regex=True) 
df["Description"] = df["Description"].replace(to_replace=r'^de_AGGRAVATED\s-', value='AGGRAVATED ', regex=True) 
df["Description"] = df["Description"].replace(to_replace=r'^de_AGGRAVATED:', value='AGGRAVATED ', regex=True) 
df["Description"] = df["Description"].replace(to_replace=r'P.O.', value='POLICE OFFICER', regex=True) 
df["Description"] = df["Description"].replace(to_replace=r'PO:', value='POLICE OFFICER ', regex=True) 
df["Description"] = df["Description"].replace(to_replace=r'\s*/\s*', value=' ', regex=True) ##geprüft3004 von 213 auf 198  






columns = ['time', 'Block', 'Primary Type', 'Description', 'Location Description', 'year', 'month', 'weekday', 't']
df = pd.DataFrame(df, columns=columns)
df.dropna()
print("(8/9) start preparing for printing | Time in Secounds: ", time.time() - start_time)
print(df)

print('(9/9) start saving as csv | Time previous Step: ', time.time() - start_time)
df.to_csv('7mioCrimes.csv', index=False)


Laufzeit = time.time() - start_time
print("Finished, Time: ", Laufzeit)