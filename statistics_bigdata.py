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

print("Start")
df = pd.read_csv("7mioCrimes.csv", low_memory=False)
df["time"] = df["time"].astype(str)
df["year"] = df["year"].astype(str)

#Damit verlieren wir die erstezeile im datensatz
print(df.columns)
print(df.unique())

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

print("--------------PRIMARY DESCRIPTION:---------------")
primary_description = df['time']
statisticsPrint(primary_description)
primary_description.value_counts().to_json(r'Counts_json\DataframeValueCounts' + 'TIME'+ '.json')
print("--------------SECONDARY DESCRIPTION:---------------")
secondary_description = df['Block']
statisticsPrint(secondary_description)
secondary_description.value_counts().to_json(r'Counts_json\DataframeValueCounts' + 'BLOCK' + '.json')
print("--------------BLOCK:---------------")
block = df['Primary Type']
statisticsPrint(block)
block.value_counts().to_json(r'Counts_json\DataframeValueCounts' + 'PRIMARYTYPE' + '.json')
print("--------------LOCATION DESCRIPTION:---------------")
location_description = df['Description']
statisticsPrint(location_description)
location_description.value_counts().to_json(r'Counts_json\DataframeValueCounts' + 'DESCRIPTION' + '.json')
print("--------------DAY---------------")
day = df['Location Description']
statisticsPrint(day)
day.value_counts().to_json(r'Counts_json\DataframeValueCounts' + 'LOCATIONDESCRIPTION' + '.json')
print("--------------AM/PM---------------")
ampm = df['year']
statisticsPrint(ampm)
ampm.value_counts().to_json(r'Counts_json\DataframeValueCounts' + 'YEAR' + '.json')
print("--------------TIME---------------")
time = df['month']
statisticsPrint(time)
time.value_counts().to_json(r'Counts_json\DataframeValueCounts' + 'MONTH' + '.json')
print("--------------TIME---------------")
time2 = df['weekday']
statisticsPrint(time)
time2.value_counts().to_json(r'Counts_json\DataframeValueCounts' + 'WEEKDAY' + '.json')
print("--------------TIME---------------")
time3 = df['t']
statisticsPrint(time)
time3.value_counts().to_json(r'Counts_json\DataframeValueCounts' + 'T' + '.json')
