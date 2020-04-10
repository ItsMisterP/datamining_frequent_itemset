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




print("Hier sind alle Spalten:")
print(df.columns)
#print(df.isnull())

print()
print()
print()

print("--------------PRIMARY DESCRIPTION:---------------")
primary_description = df['PRIMARY DESCRIPTION']
#print("Unique Werte:")
#print(primary_description.unique())
#print("Anzahl unique Werte:")
print(len(primary_description.unique()))
print("Häufigkeit der Werte:")
print(primary_description.value_counts())

print()
print("--------------SECONDARY DESCRIPTION:---------------")
secondary_description = df['SECONDARY DESCRIPTION']
#print("Unique Werte:")
#print(secondary_description.unique())
print("Anzahl unique Werte:")
print(len(secondary_description.unique()))
print("Häufigkeit der Werte:")
print(secondary_description.value_counts())

print()
print("--------------BLOCK:---------------")
block = df['BLOCK']
#print("Unique Werte:")
#print(block.unique())
print("Anzahl unique Werte:")
print(len(block.unique()))
print("Häufigkeit der Werte:")
print(block.value_counts())

print()
print("--------------LOCATION DESCRIPTION:---------------")
location_description = df['LOCATION DESCRIPTION']
#print("Unique Werte:")
#print(location_description.unique())
print("Anzahl unique Werte:")
print(len(location_description.unique()))
print("Häufigkeit der Werte:")
print(location_description.value_counts())

print()
print("--------------DAY---------------")
day = df['DAY']
#print("Unique Werte:")
#print(day.unique())
print("Anzahl unique Werte:")
print(len(day.unique()))
print("Häufigkeit der Werte:")
print(day.value_counts())

print()
print("--------------AM/PM---------------")
ampm = df['AM/PM']
#print("Unique Werte:")
#print(ampm.unique())
print("Anzahl unique Werte:")
print(len(ampm.unique()))
print("Häufigkeit der Werte:")
print(ampm.value_counts())

print()
print("--------------TIME---------------")
time = df['TIME']
#print("Unique Werte:")
#print(ampm.unique())
print("Anzahl unique Werte:")
print(len(time.unique()))
print("Häufigkeit der Werte:")
print(time.value_counts())


#Diagramme START 

def diagrammedrucken():
    #Balkendiagramm
    plt.figure()
    primary_description.value_counts().plot(kind = "bar")
    plt.savefig('Diagramme/primary_description.value_counts.png', dpi=1200, bbox_inches = "tight")
    #ax.set_xticks([])       # Alternatively, you can manually adjust the ticks
    #x.set_xticklabels([])   # or their labels
    #plt.axis([0, 6, 0, 20])
    #plt.locator_params(axis='x', nbins=100)
    
    plt.figure()
    secondary_description.value_counts().plot(kind = "bar")
    plt.savefig('Diagramme/secondary_description.value_counts.png', dpi=1200, bbox_inches = "tight")
    
    
    plt.figure()
    block.value_counts().plot(kind = "bar")
    plt.savefig('Diagramme/block.value_counts.png', dpi=1200, bbox_inches = "tight")
        
    plt.figure()
    location_description.value_counts().plot(kind = "bar")
    plt.savefig('Diagramme/location_description.value_counts.png', dpi=1200, bbox_inches = "tight")

    plt.figure()
    day.value_counts().plot(kind = "bar")
    plt.savefig('Diagramme/day.value_counts.png', dpi=1200, bbox_inches = "tight")
    
    plt.figure()
    ampm.value_counts().plot(kind = "bar")
    plt.savefig('Diagramme/ampm.value_counts.png', dpi=1200, bbox_inches = "tight")

    plt.figure()
    time.value_counts().plot(kind = "bar")
    plt.savefig('Diagramme/time.value_counts.png', dpi=1200, bbox_inches = "tight")

diagrammedrucken()


# iterating over rows using iterrows() function 

'''
for i, j in df.iterrows():
    print(i, j)
    print()
'''    
'''
# creating a list of dataframe columns
columns = list(df)
 
for i in columns:
    # printing the third element of the column
    print (df[i][0])
#print(df)
'''