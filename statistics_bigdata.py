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
      

def statisticsPrint(dataframe):

    print("Unique Werte:")
    print(dataframe.unique())
    print("Anzahl unique Werte:")
    print(len(dataframe.unique()))
    print("Häufigkeit der Werte:")
    print(dataframe.value_counts())
    print()
    #print(dataframe.value_counts().to_json())
    dataframe.value_counts().to_json(r'Counts_json\DataframeValueCounts' + dataframe[0] + '.json')

print("Hier sind alle Spalten:")
print(df.columns)
#print(df.isnull())

print()
print()
print()

print("--------------PRIMARY DESCRIPTION:---------------")
primary_description = df['time']
statisticsPrint(primary_description)
print("--------------SECONDARY DESCRIPTION:---------------")
secondary_description = df['Block']
statisticsPrint(secondary_description)
print("--------------BLOCK:---------------")
block = df['Primary Type']
statisticsPrint(block)
print("--------------LOCATION DESCRIPTION:---------------")
location_description = df['Description']
statisticsPrint(location_description)
print("--------------DAY---------------")
day = df['Location Description']
statisticsPrint(day)
print("--------------AM/PM---------------")
ampm = df['year']
statisticsPrint(ampm)
print("--------------TIME---------------")
time = df['month']
statisticsPrint(time)
print("--------------TIME---------------")
time = df['weekday']
statisticsPrint(time)
print("--------------TIME---------------")
time = df['t']
statisticsPrint(time)
 