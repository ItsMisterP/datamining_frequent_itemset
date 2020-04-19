#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 21:03:00 2020

@author: robin
"""

import numpy as np
import pandas as pd
import matplotlib as mlp
import matplotlib.pyplot as plt

print("Start")
df = pd.read_csv("crimes_e_columns_ficken.csv", low_memory=False)

#Damit verlieren wir die erstezeile im datensatz
df.columns = ['PRIMARY DESCRIPTION', 'LOCATION DESCRIPTION', 'BLOCK', 'DAY', 'AM/PM', 'SECONDARY DESCRIPTION', 'TIME'] 

def statisticsPrint(dataframe):

    #print("Unique Werte:")
    #print(dataframe.unique())
    #print("Anzahl unique Werte:")
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
primary_description = df['PRIMARY DESCRIPTION']
statisticsPrint(primary_description)
print("--------------SECONDARY DESCRIPTION:---------------")
secondary_description = df['SECONDARY DESCRIPTION']
statisticsPrint(secondary_description)
print("--------------BLOCK:---------------")
block = df['BLOCK']
statisticsPrint(block)
print("--------------LOCATION DESCRIPTION:---------------")
location_description = df['LOCATION DESCRIPTION']
statisticsPrint(location_description)
print("--------------DAY---------------")
day = df['DAY']
statisticsPrint(day)
print("--------------AM/PM---------------")
ampm = df['AM/PM']
statisticsPrint(ampm)
print("--------------TIME---------------")
time = df['TIME']
statisticsPrint(time)


#Diagramme START 

def printBarChart(dataframe, title, w=6.4 , h=4.8):
    plt.figure(figsize=(w,h))
    dataframe.value_counts().plot(kind = "bar")
    plt.savefig('Diagramme/_' + title + '_barChart.png', dpi=120, bbox_inches = 'tight')


#printBarChart(time, "time")
#printBarChart(primary_description, "primary_description")
#printBarChart(secondary_description, "secondary_description")
#printBarChart(ampm, "ampm")
#printBarChart(block,"block")
#printBarChart(day, "day")
#printBarChart(location_description, "location_description", 25, 10)

#plt.figure()


location_description.value_counts().sort_values(ascending=False)[:40].plot(kind="barh", rot=20, x='anzahl', y='Streets')
#plt.savefig('Diagramme/_' + 'test' + '_barChart.png', dpi=120, bbox_inches = 'tight')

x = df['PRIMARY DESCRIPTION']
y = df['DAY']
plt.scatter(x,y)
plt.show()

#df.tail(10).plot.barh()

print(location_description)
