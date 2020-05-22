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
import io

#in FirstRUn integrieren

df = pd.read_csv("7mioCrimes.csv", low_memory=False)
  
df["LocationDescription"] = df["Location Description"]
df["PrimaryType"] = df["Primary Type"]
df = df.drop(["Location Description"], axis=1)
df = df.drop(["Primary Type"], axis=1)

resultObject = {}


for district in df['District'].unique():
    districtDf = df.loc[df['District'] == district]
    districtDf = districtDf.drop(['District'], axis=1)
    tmp= {}
    for column in districtDf.columns:
        print("Generate counts of column:", column)
        columnset = districtDf[column]
        tmp[column] = columnset.value_counts().to_dict()
    resultObject[district] = tmp
        
with open('website/src/assets/json/dashboard/CountsPerDistrikt.json', "w") as outfile: 
    outfile.write(json.dumps(resultObject))
    
    



