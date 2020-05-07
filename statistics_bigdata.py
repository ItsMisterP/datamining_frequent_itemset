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


def statistics(df):    
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
  

    df["LocationDescription"] = df["Location Description"]
    df["PrimaryType"] = df["Primary Type"]
    df = df.drop(["Location Description"], axis=1)
    df = df.drop(["Primary Type"], axis=1)

    resultObject = {}

    for column in df.columns:
        print("Generate counts of column ", column)
        columnset = df[column]
        #statisticsPrint(columnset)
        #columnset.value_counts().to_json(r'Counts_json\Counts' + column + '.json')
        #columnset.value_counts().to_json(r'website\src\assets\json\Counts' + column + '.json')
        resultObject[column] = columnset.value_counts().to_dict()
    
    print("Safe as json")
    with open(r'website\src\assets\json\CountsAll.json', "w") as outfile: 
        outfile.write(json.dumps(resultObject))

    with open(r'Counts_json\CountsAll.json', "w") as outfile: 
        outfile.write(json.dumps(resultObject))
    

