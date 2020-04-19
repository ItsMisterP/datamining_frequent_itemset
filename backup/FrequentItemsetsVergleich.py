# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 09:04:07 2020

@author: robi & phili
"""

import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
#from mlxtend.frequent_patterns import association_rules
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import fpgrowth
import numpy as np
import csv
import re
import association_rules as own
import dataframePrint as ownPrint


#pd.set_option('display.max_rows', 50000)
#pd.set_option('display.width', 10000)
#pd.set_option('display.max_columns', None)
#pd.set_option('display.max_colwidth', None)

#Variables
show_rules = 3
kluc_threshold = 0.55
kluc_range_max = 0.6
kluc_range_min = 0.5
imb_ratio_threshold = 0.25
association_rules_threshold = 0.6
min_sup_threshold = 0.0005


print("Start")
df = pd.read_csv("7mioCrimes.csv", low_memory=False)
#print(df)

df["time"] = df["time"].astype(str)
df["year"] = df["year"].astype(str)

#extrahiert die monate! 
#df['DATE'] = df ['DATE'].str.extract("(\w*)/")
#df['DATE'] = df ['DATE'].str.replace("12", "Winter").str.replace("01", "Winter").str.replace("02", "Winter").str.replace("03", "Spring").str.replace("04", "Spring").str.replace("05", "Spring").str.replace("06", "Summer").str.replace("07", "Summer").str.replace("08", "Summer").str.replace("09", "Autumn").str.replace("10", "Autumn").str.replace("11", "Autumn")

df = df.dropna()

df = df.to_numpy()
#print(df)
#print(df[df['IUCR'].str.contains('8')])


te = TransactionEncoder()
te_ary = te.fit(df).transform(df)
df2 = pd.DataFrame(te_ary, columns=te.columns_)

#frequent_itemsets = apriori(df1, min_support=0.0001, use_colnames=True, low_memory=True)
frequent_itemsets = fpgrowth(df2, min_support=min_sup_threshold, use_colnames=True)
print("Frequent_Itemsets created")
print(len(frequent_itemsets))



print("Finished")
