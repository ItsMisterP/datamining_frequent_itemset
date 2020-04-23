#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 21:03:00 2020

@author: robi & phili
"""

import numpy as np
import pandas as pd
import matplotlib as mlp
import matplotlib.pyplot as plt
import json
from  jsonmerge import merge
import io


print("Start")
df = pd.read_csv("7mioCrimes.csv", low_memory=False)


#Damit verlieren wir die erstezeile im datensatz
print(df.columns)

def statisticsPrint(dataframe):

    print("Unique Werte:")
    print(dataframe.unique())
    print("Anzahl unique Werte:")
    print(len(dataframe.unique()))
    print("Häufigkeit der Werte:")
    print(dataframe.value_counts())
    print()
    #print(dataframe.value_counts().to_json())
    #dataframe.value_counts().to_json(r'Counts_json\DataframeValueCounts' + dataframe[0] + '.json')

print("Hier sind alle Spalten:")
print(df.columns)
#print(df.isnull())

print()
print()
print()

print("--------------time:---------------")
time = df['time']
statisticsPrint(time)
valueCountsTime = time.value_counts().to_json(r'Counts_json\DataframeValueCounts' + 'TIME'+ '.json')
uniqueTime = pd.DataFrame(time.unique())
uniqueTime.columns = ["id"]
uniqueTime.to_json(r'Unique_json\UniqueValuesTIME.json', orient='records', lines=True)
timeJSON = uniqueTime.to_json(orient='records', lines=True)

print("--------------Block:---------------")
block = df['Block']
statisticsPrint(block)
valueCountsBlock = block.value_counts().to_json(r'Counts_json\DataframeValueCounts' + 'BLOCK' + '.json')
uniqueBlock = pd.DataFrame(block.unique())
uniqueBlock.columns = ["id"]
uniqueBlock.to_json(r'Unique_json\UniqueValuesBLOCK.json', orient='records', lines=True)
blockJSON = uniqueBlock.to_json(orient='records', lines=True)

print("--------------Primary Type:---------------")
primary_type = df['Primary Type']
statisticsPrint(primary_type)
valueCountsPrimary_type = primary_type.value_counts().to_json(r'Counts_json\DataframeValueCounts' + 'PRIMARYTYPE' + '.json')
uniquePrimary_type  = pd.DataFrame(primary_type.unique())
uniquePrimary_type.columns = ["id"]
uniquePrimary_type.to_json(r'Unique_json\UniqueValuesPRIMARYTYPE.json', orient='records', lines=True)
primary_typeJSON = uniquePrimary_type.to_json(orient='records', lines=True)

print("--------------Description:---------------")
description = df['Description']
statisticsPrint(description)
valueCountsDescription = description.value_counts().to_json(r'Counts_json\DataframeValueCounts' + 'DESCRIPTION' + '.json')
uniqueDescription = pd.DataFrame(description.unique())
uniqueDescription.columns = ["id"]
uniqueDescription.to_json(r'Unique_json\UniqueValuesDESCRIPTION.json', orient='records', lines=True)
descriptionJSON = uniqueDescription.to_json(orient='records', lines=True)
    
print("--------------Location Description---------------")
location_description = df['Location Description']
statisticsPrint(location_description)
valueCountsLocation_description = location_description.value_counts().to_json(r'Counts_json\DataframeValueCounts' + 'LOCATIONDESCRIPTION' + '.json')
uniqueLocation_description = pd.DataFrame(location_description.unique())
uniqueLocation_description.columns = ["id"]
uniqueLocation_description.to_json(r'Unique_json\UniqueValuesLOCATIONDESCRIPTION.json', orient='records', lines=True)
locationJSON = uniqueLocation_description.to_json(orient='records', lines=True)

print("--------------year---------------")
year = df['year']
statisticsPrint(year)
valueCountsYear = year.value_counts().to_json(r'Counts_json\DataframeValueCounts' + 'YEAR' + '.json')
uniqueYear = pd.DataFrame(year.unique())
uniqueYear.columns = ["id"]
uniqueYear.to_json(r'Unique_json\UniqueValuesYEAR.json', orient='records', lines=True)
yearJSON = uniqueYear.to_json(orient='records', lines=True)
  
print("--------------month---------------")
month = df['month']
statisticsPrint(month)
valueCountsMonth = month.value_counts().to_json(r'Counts_json\DataframeValueCounts' + 'MONTH' + '.json')
uniqueMonth = pd.DataFrame(month.unique())
uniqueMonth.columns = ["id"]
uniqueMonth.to_json(r'Unique_json\UniqueValuesMONTH.json', orient='records', lines=True)
monthJSON = uniqueMonth.to_json(orient='records', lines=True)

print("--------------weekday---------------")
weekday = df['weekday']
statisticsPrint(weekday)
valueCountsWeekday = weekday.value_counts().to_json(r'Counts_json\DataframeValueCounts' + 'WEEKDAY' + '.json')
uniqueWeekday = pd.DataFrame(weekday.unique())
uniqueWeekday.columns = ["id"]
uniqueWeekday.to_json(r'Unique_json\UniqueValuesWEEKDAY.json', orient='records', lines=True)
weekdayJSON = uniqueWeekday.to_json(orient='records', lines=True)

print("--------------t---------------")
t = df['t']
statisticsPrint(t)
valueCountsT = t.value_counts().to_json(r'Counts_json\DataframeValueCounts' + 'T' + '.json')
uniqueT = pd.DataFrame(t.unique())
uniqueT.columns = ["id"]
uniqueT.to_json(r'Unique_json\UniqueValuesT.json', orient='records', lines=True)
tJSON = uniqueT.to_json(orient='records', lines=True)


print("--------------Gesamt---------------")

result = timeJSON + "\r" + blockJSON + "\r" + primary_typeJSON + "\r" + descriptionJSON + "\r" + locationJSON +"\r" + yearJSON + "\r"+ monthJSON + "\r" + weekdayJSON + "\r"+ tJSON
resultTmp = result.replace("}", "},")
resultFormatted = "[" + resultTmp + "]"
resultFormatted2 = resultFormatted.replace(",]", "]")
with io.open(r'Unique_json\UniqueValuesGESAMT.json', 'w', encoding='utf-8') as outfile:
    outfile.write(resultFormatted2)
    
print("--------------Finished---------------")
