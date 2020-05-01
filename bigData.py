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
columns = ['Date', 'Block', 'IUCR', 'Primary Type', 'Location Description', 'Year']
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

print("--------------Adding Prefixes--------------- | Time in Secounds: ", time.time() - start_time)
df["Block"] = df["Block"].replace(to_replace=r'^\s', value='bl_', regex=True) #hier ist das \s dabei, weil es mit nem Leerzeichen noch anfängt
df["Location Description"] = df["Location Description"].replace(to_replace=r'^', value='lo_', regex=True)
#df["IUCR"] = df["IUCR"].replace(to_replace=r'^', value='IUCR_', regex=True)

print("--------------Encode IUCR--------------- | Time in Secounds: ", time.time() - start_time)
df['IUCR'] = df['IUCR'].astype(str)
df_iucr['IUCR'] = df_iucr['IUCR'].astype(str)
df_iucr = pd.read_csv(r'IUCR\IUCR_CODES.csv', low_memory=False)
df_iucr["IUCR_ENCODED"] = df_iucr['PRIMARY DESCRIPTION'] + " " + df_iucr['SECONDARY DESCRIPTION']
df_iucr = df_iucr.drop(columns=['PRIMARY DESCRIPTION', 'SECONDARY DESCRIPTION','INDEX CODE'])
df_iucr["IUCR"] = df_iucr["IUCR"].replace(to_replace=r'^0', value='', regex=True)
df["IUCR"] = df["IUCR"].replace(to_replace=r'^0', value='', regex=True) 



def encodeIUCR(x):
    test = df_iucr.loc[df_iucr["IUCR"] == x]
    return test.iloc[0]["IUCR_ENCODED"]


df["IUCR"] = df["IUCR"].apply(lambda x: encodeIUCR(x))


#df.loc[df["IUCR"] == "5013"]

#Entferne Ähnlichkeiten
#Stand 3004 von 213 auf 144 bei Location Description
print("--------------Remove Similarities------------- | Time in Secounds: ", time.time() - start_time)
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
df["Location Description"] = df["Location Description"].replace(to_replace=r'^lo_CTA.+', value='lo_Chicago Transit Authority', regex=True) 
df["Location Description"] = df["Location Description"].replace("lo_BARBER SHOP BEAUTY SALON", "lo_BARBERSHOP") 
df["Location Description"] = df["Location Description"].replace(to_replace=r'^lo_CHURCH.+', value='lo_CHURCH', regex=True) 
df["Location Description"] = df["Location Description"].replace(to_replace=r'^lo_COLLEGE.+', value='lo_COLLEGE', regex=True) 
df["Location Description"] = df["Location Description"].replace("lo_FACTORY MANUFACTURING BUILDING", "lo_FACTORY") 
df["Location Description"] = df["Location Description"].replace("lo_GAS STATION DRIVE PROP.", "lo_GAS STATION") 
df["Location Description"] = df["Location Description"].replace("lo_GOVERNMENT BUILDING PROPERTY", "lo_GOVERNMENT BUILDING") 
df["Location Description"] = df["Location Description"].replace("lo_HOSPITAL BUILDING GROUNDS", "lo_HOSPITAL") 
df["Location Description"] = df["Location Description"].replace("lo_HOTEL MOTEL", "lo_HOTEL") 
df["Location Description"] = df["Location Description"].replace("lo_LAKEFRONT WATERFRONT RIVERBANK", "lo_LAKE") 
df["Location Description"] = df["Location Description"].replace(["lo_NURSING HOME RETIREMENT HOME","lo_NURSING RETIREMENT HOME"], "lo_NURSING HOME") 
df["Location Description"] = df["Location Description"].replace("lo_POLICE FACILITY VEH PARKING LOT", "lo_POLICE FACILITY VEHICLE PARKING LOT") 
df["Location Description"] = df["Location Description"].replace(["lo_PUBLIC GRAMMAR SCHOOL","lo_PUBLIC HIGH SCHOOL"], "lo_SCHOOL") 
df["Location Description"] = df["Location Description"].replace("lo_RESIDENTIAL YARD (FRONT BACK)", "lo_RESIDENCE") 
df["Location Description"] = df["Location Description"].replace("lo_TAVERN LIQUOR STORE", "lo_TAVERN") 
df["Location Description"] = df["Location Description"].replace("lo_TRUCKING TERMINAL", "lo_TRUCK") 
df["Location Description"] = df["Location Description"].replace("lo_VACANT LOT LAND", "lo_VACANT LOT LAND") 
df["Location Description"] = df["Location Description"].replace("lo_CLEANERS LAUNDROMAT", "lo_CLEANING STORE") 
print("--------------Location Description Done------------- | Time in Secounds: ", time.time() - start_time)

#von 4208 auf -3260 mit upper allein
df["Block"] = df["Block"].str.upper()
df["Block"] = df["Block"].replace(to_replace=r'BL_\s.', value='', regex=True) 
df["Block"] = df["Block"].replace(to_replace=r'\s+', value=' ', regex=True)
df["Block"] = df["Block"].replace(to_replace=r'\dTH\s', value=' ', regex=True) 
df["Block"] = df["Block"].replace(to_replace=r'\dND\s', value=' ', regex=True) 
df["Block"] = df["Block"].replace(to_replace=r'\dRD\s', value=' ', regex=True) 
df["Block"] = df["Block"].replace(to_replace=r'\dST\s', value=' ', regex=True)
df["Block"] = df["Block"].replace(to_replace=r'\d\sTH\s', value=' ', regex=True) 
df["Block"] = df["Block"].replace(to_replace=r'\d\sND\s', value=' ', regex=True) 
df["Block"] = df["Block"].replace(to_replace=r'\d\sRD\s', value=' ', regex=True) 
df["Block"] = df["Block"].replace(to_replace=r'\d\sST\s', value=' ', regex=True)
df["Block"] = df["Block"].replace(to_replace=r'\s\bSTREET\b', value=' ST', regex=True)
df["Block"] = df["Block"].replace(to_replace=r'\s\bPLACE\b', value=' ST', regex=True) 
df["Block"] = df["Block"].replace(to_replace=r'\s\bBLVD\b', value=' BL', regex=True)
df["Block"] = df["Block"].replace(to_replace=r'\s\bAV\b', value=' AVE', regex=True) 
df["Block"] = df["Block"].replace(to_replace=r'\s\bTR\b', value=' TER', regex=True) 
df["Block"] = df["Block"].replace(to_replace=r'\s\bSTREET\b', value=' ST', regex=True)
df["Block"] = df["Block"].replace(to_replace=r'\s\bDRIVE\b', value=' DR', regex=True)
df["Block"] = df["Block"].replace(to_replace=r'\s\bAVENUE\b', value=' AVE', regex=True)
df["Block"] = df["Block"].replace(to_replace=r'\s\bPARK\b', value=' PK', regex=True)  
df["Block"] = df["Block"].replace(to_replace=r'\s\bSQUARE\b', value=' SQ', regex=True) 
df["Block"] = df["Block"].replace(to_replace=r'\s\bPLACE\b', value=' ST', regex=True) 
df["Block"] = df["Block"].replace(to_replace=r'\s\bBLVD\b', value=' BL', regex=True)
df["Block"] = df["Block"].replace(to_replace=r'\s\bAV\b', value=' AVE', regex=True) 
df["Block"] = df["Block"].replace(to_replace=r'\s\bTR\b', value=' TER', regex=True) 
df["Block"] = df["Block"].replace(to_replace=r'\s\bAVE\b\s\w.+', value=' AVE', regex=True) 
df["Block"] = df["Block"].replace(to_replace=r'\s\bST\b\s\w.+', value=' ST', regex=True)
df["Block"] = df["Block"].replace(to_replace=r'\s\bPL\b\s\w.+', value=' PL', regex=True) 
df["Block"] = df["Block"].replace(to_replace=r'\s\bRD\b\s\w.+', value=' PL', regex=True) 
df["Block"] = df["Block"].replace(to_replace=r'\s\bPW\b', value=' PKWY', regex=True)
df["Block"] = df["Block"].replace(to_replace=r'\s\bPZ\b', value=' PLZ', regex=True)

df["Block"] = df["Block"].replace(to_replace=r'\.', value='', regex=True)

print("--------------Block Done------------- | Time in Secounds: ", time.time() - start_time)


columns = ['time', 'Block', 'IUCR', 'Location Description', 'year', 'month', 'weekday', 't']
df = pd.DataFrame(df, columns=columns)
df = df.dropna()
print("(8/9) start preparing for printing | Time in Secounds: ", time.time() - start_time)
print(df)

print('(9/9) start saving as csv | Time previous Step: ', time.time() - start_time)
df.to_csv('7mioCrimes.csv', index=False)


Laufzeit = time.time() - start_time
print("Finished, Time: ", Laufzeit)