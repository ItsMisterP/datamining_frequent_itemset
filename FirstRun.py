# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 13:54:13 2020

@author: robi & pili
"""


import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import association_rules
from mlxtend.frequent_patterns import apriori
import numpy as np
import csv
import re

print("Start")
df = pd.read_csv("crimes_e_columns_ficken.csv", low_memory=False)
#print(df)


#extrahiert die monate! 
#df['DATE'] = df ['DATE'].str.extract("(\w*)/")
#df['DATE'] = df ['DATE'].str.replace("12", "Winter").str.replace("01", "Winter").str.replace("02", "Winter").str.replace("03", "Spring").str.replace("04", "Spring").str.replace("05", "Spring").str.replace("06", "Summer").str.replace("07", "Summer").str.replace("08", "Summer").str.replace("09", "Autumn").str.replace("10", "Autumn").str.replace("11", "Autumn")

df = df.dropna()

df2 = df.to_numpy()
#print(df)
#print(df[df['IUCR'].str.contains('8')])


te = TransactionEncoder()
te_ary = te.fit(df2).transform(df2)
df1 = pd.DataFrame(te_ary, columns=te.columns_)

frequent_itemsets = apriori(df1, min_support=0.0001, use_colnames=True, low_memory=True)
print("Frequent_Itemsets created")
#print(frequent_itemsets)

result = association_rules(frequent_itemsets, min_threshold=0.2)
#print(result['lift'])
#result = association_rules(frequent_itemsets, min_threshold=0.5)6g vbrdf e

print("Association Rules")
#print(result)
result.to_csv('out.csv', index=False) 
df2 = result
#Füge eine neue Spalte mit der Länge dem Dataframe hinzu
df2["antecedent_len"] = df2["antecedents"].apply(lambda x: len(x))
print(df2[ (df2['antecedent_len'] >= 3) ])
#hier ist ein Dataframe, welches frozensets enthält -> deswegen inhalt zu string convertieren und dann contains prüfen können
#print(df2[df2['antecedents'].astype(str).str.contains(',')]) 
#print(df2)
print("Finished")
