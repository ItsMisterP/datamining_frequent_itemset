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
  
    df["LocationDescription"] = df["Location Description"]
    df["PrimaryType"] = df["Primary Type"]
    df = df.drop(["Location Description"], axis=1)
    df = df.drop(["Primary Type"], axis=1)

    resultObject = {}

    for column in df.columns:
        print("Generate counts of column:", column)
        columnset = df[column]
        resultObject[column] = columnset.value_counts().to_dict()
    
    print("Safe as json")
    with open('website/src/assets/json/CountsAll.json', "w") as outfile: 
        outfile.write(json.dumps(resultObject))

