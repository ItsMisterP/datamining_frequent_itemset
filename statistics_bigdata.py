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
uniqueTime = time.unique()
uniqueTimeList = uniqueTime.tolist()
with open(r'Unique_json\UniqueValuesTIME.json', 'w', encoding='utf-8') as f:
    json.dump(uniqueTimeList, f, ensure_ascii=False, indent=4)

print("--------------Block:---------------")
block = df['Block']
statisticsPrint(block)
valueCountsBlock = block.value_counts().to_json(r'Counts_json\DataframeValueCounts' + 'BLOCK' + '.json')
uniqueBlock = block.unique()
uniqueBlockList = uniqueBlock.tolist()
with open(r'Unique_json\UniqueValuesBLOCK.json', 'w', encoding='utf-8') as f:
    json.dump(uniqueBlockList, f, ensure_ascii=False, indent=4)


print("--------------Primary Type:---------------")
primary_type = df['Primary Type']
statisticsPrint(primary_type)
valueCountsPrimary_type = primary_type.value_counts().to_json(r'Counts_json\DataframeValueCounts' + 'PRIMARYTYPE' + '.json')
uniquePrimary_type  = primary_type.unique()
uniquePrimary_typeList = uniquePrimary_type.tolist()
with open(r'Unique_json\UniqueValuesPRIMARYTYPE.json', 'w', encoding='utf-8') as f:
    json.dump(uniquePrimary_typeList, f, ensure_ascii=False, indent=4)

print("--------------Description:---------------")
description = df['Description']
statisticsPrint(description)
valueCountsDescription = description.value_counts().to_json(r'Counts_json\DataframeValueCounts' + 'DESCRIPTION' + '.json')
uniqueDescription = description.unique()
uniqueDescriptionList = uniqueDescription.tolist()
with open(r'Unique_json\UniqueValuesDESCRIPTION.json', 'w', encoding='utf-8') as f:
    json.dump(uniqueDescriptionList, f, ensure_ascii=False, indent=4)
    
print("--------------Location Description---------------")
location_description = df['Location Description']
statisticsPrint(location_description)
valueCountsLocation_description = location_description.value_counts().to_json(r'Counts_json\DataframeValueCounts' + 'LOCATIONDESCRIPTION' + '.json')
uniqueLocation_description = location_description.unique()
uniqueLocation_descriptionList = uniqueLocation_description.tolist()
with open(r'Unique_json\UniqueValuesLOCATIONDESCRIPTION.json', 'w', encoding='utf-8') as f:
    json.dump(uniqueLocation_descriptionList, f, ensure_ascii=False, indent=4)

print("--------------year---------------")
year = df['year']
statisticsPrint(year)
valueCountsYear = year.value_counts().to_json(r'Counts_json\DataframeValueCounts' + 'YEAR' + '.json')
uniqueYear = year.unique()
uniqueYearList = uniqueYear.tolist()
with open(r'Unique_json\UniqueValuesYEAR.json', 'w', encoding='utf-8') as f:
    json.dump(uniqueYearList, f, ensure_ascii=False, indent=4)
    
print("--------------month---------------")
month = df['month']
statisticsPrint(month)
valueCountsMonth = month.value_counts().to_json(r'Counts_json\DataframeValueCounts' + 'MONTH' + '.json')
uniqueMonth = month.unique()
uniqueMonthList = uniqueMonth.tolist()
with open(r'Unique_json\UniqueValuesMONTH.json', 'w', encoding='utf-8') as f:
    json.dump(uniqueMonthList, f, ensure_ascii=False, indent=4)

print("--------------weekday---------------")
weekday = df['weekday']
statisticsPrint(weekday)
valueCountsWeekday = weekday.value_counts().to_json(r'Counts_json\DataframeValueCounts' + 'WEEKDAY' + '.json')
uniqueWeekday = weekday.unique()
uniqueWeekdayList = uniqueWeekday.tolist()
with open(r'Unique_json\UniqueValuesWEEKDAY.json', 'w', encoding='utf-8') as f:
    json.dump(uniqueWeekdayList, f, ensure_ascii=False, indent=4)

print("--------------t---------------")
t = df['t']
statisticsPrint(t)
valueCountsT = t.value_counts().to_json(r'Counts_json\DataframeValueCounts' + 'T' + '.json')
uniqueT = t.unique()
uniqueTList = uniqueT.tolist()
with open(r'Unique_json\UniqueValuesT.json', 'w', encoding='utf-8') as f:
    json.dump(uniqueTList, f, ensure_ascii=False, indent=4)

print("--------------Gesamt---------------")
UniqueWerteGESAMT = uniqueTimeList + uniqueBlockList + uniquePrimary_typeList + uniqueDescriptionList + uniqueLocation_descriptionList + uniqueYearList + uniqueMonthList + uniqueWeekdayList + uniqueTList
with open(r'Unique_json\UniqueValuesGESAMT.json', 'w', encoding='utf-8') as f:
    json.dump(UniqueWerteGESAMT, f, ensure_ascii=False, indent=4)