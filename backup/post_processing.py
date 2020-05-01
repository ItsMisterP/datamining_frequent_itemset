"""
Created on 20.04.2020

@author: phili & robi
"""
import pandas as pd
import numpy as np
import csv
import re

print("Start post processing")
dataframe_fi = pd.read_json("frequent_itemsets.json")
dataframe_ar = pd.read_json("association_rules.json")

print("Do some Stuff")
dataframe_ar["imbratio"] = dataframe_ar["imb ratio"]
dataframe_ar.drop('imb ratio', axis=1, inplace=True)

print("Save stuff")
dataframe_fi.to_json(r"website\src\assets\json\frequent_itemsets.json", orient='records')
dataframe_ar.to_json(r"website\src\assets\json\association_rules.json", orient='records')

