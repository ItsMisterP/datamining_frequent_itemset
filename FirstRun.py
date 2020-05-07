# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 13:54:13 2020

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
import io
import time
import statistics_bigdata as statistics


#pd.set_option('display.max_rows', 50000)
#pd.set_option('display.width', 10000)
#pd.set_option('display.max_columns', None)
#pd.set_option('display.max_colwidth', None)

#Variables
show_rules = 3
kluc_range_min = 0.0
kluc_range_max = 1.0
imb_ratio_threshold = 0.25
association_rules_threshold = 0.6
min_sup_threshold = 0.001
metric = "confidence"

start_time = time.time()
print("Start", time.time() - start_time)
df = pd.read_csv("7mioCrimes.csv", low_memory=False)
#print(df)
print()
print("#################################################")
print("Datensatz eingelesen", time.time() - start_time)

print()
print("#################################################")
print("Statisitken erstellen", time.time() - start_time)
statistics.statistics(df)

print()
print("#################################################")
print("Tempoären Filter anwenden")
# Mögliche Spalten: 
# ['time', 'District', 'year', 'Primary Type','IUCR','Block', 'Location Description', 'month', 'weekday', 't', 'Description']
df["time"] = df["time"].astype(str)
df["year"] = df["year"].astype(str)
df["District"] = df["District"].astype(str)
#df = df.drop(["Primary Type"], axis=1)
df = df.drop(["t"], axis=1)
#df = df.drop(["time"], axis=1)
df = df.drop(["year"], axis=1)
df = df.drop(["Block"], axis=1)

df = df.drop(["IUCR"], axis=1)
#df["IUCR"] = df["IUCR"].replace(to_replace=r'\,', value=' ', regex=True) 

df = df.drop(["Description"], axis=1)

df["time"] = df["time"].replace(["1","2","3","4","5", "6"], "Time: 1-6")
df["time"] = df["time"].replace(["7","8","9","10","11","12"], "Time: 7-12")
df["time"] = df["time"].replace(["13","14","15","16","17","18"], "Time: 13-18")
df["time"] = df["time"].replace(["19","20","21","22","23","24"], "Time: 19-24")
  

#df['IUCR'] = df['IUCR'].astype(str)

#extrahiert die monate! 
#df['DATE'] = df ['DATE'].str.extract("(\w*)/")
#df['DATE'] = df ['DATE'].str.replace("12", "Winter").str.replace("01", "Winter").str.replace("02", "Winter").str.replace("03", "Spring").str.replace("04", "Spring").str.replace("05", "Spring").str.replace("06", "Summer").str.replace("07", "Summer").str.replace("08", "Summer").str.replace("09", "Autumn").str.replace("10", "Autumn").str.replace("11", "Autumn")

df = df.dropna()

df = df.to_numpy()
#print(df)
#print(df[df['IUCR'].str.contains('8')])
print()
print("#################################################")
print("Frequent Itemsets erstellen. Min-Sup: ", min_sup_threshold)
te = TransactionEncoder()
te_ary = te.fit(df).transform(df)
df2 = pd.DataFrame(te_ary, columns=te.columns_)

#frequent_itemsets = apriori(df1, min_support=0.0001, use_colnames=True, low_memory=True)
frequent_itemsets = fpgrowth(df2, min_support=min_sup_threshold, use_colnames=True)
print("Frequent_Itemsets erstelle. Speichere...", time.time() - start_time)
frequent_itemsets.to_json("frequent_itemsets.json", orient='records')

print()
print("#################################################")
print("Assoziationsregeln erstellen. Metrik:", metric, " Threshold:", association_rules_threshold)
result = own.association_rules(frequent_itemsets, min_threshold=association_rules_threshold, metric=metric)
print("Assoziationsregeln erstellt. Speichere...")

result.to_csv('out.csv', index=False)
result[(result['kluc'] >= kluc_range_min) & 
        (result['kluc'] >= kluc_range_max)].to_json("association_rules.json", orient='records')

print()
print("#################################################")
print("Statistik zum Run abspeichern...")
with io.open(r'StatisticsFirstRun.json', 'w', encoding='utf-8') as outfile:
    outfile.write("Anzahl Frequent Itemsets: ")
    outfile.write(str(len(frequent_itemsets)))
    outfile.write("\nAnzahl Association Rules: ")
    outfile.write(str(len(result)))
    outfile.write("\nZeit: ")
    outfile.write(str(time.time() - start_time))
    outfile.write("\nParameter: ")
    outfile.write("\nshow_rules: ")
    outfile.write(str(show_rules))
    outfile.write("\nkluc_range_max: ")   
    outfile.write(str(kluc_range_max))
    outfile.write("\nkluc_range_min: ")
    outfile.write(str(kluc_range_min))
    outfile.write("\nimb_ratio_threshold: ")
    outfile.write(str(imb_ratio_threshold))
    outfile.write("\nassociation_rules_threshold: ")
    outfile.write(str(association_rules_threshold))
    outfile.write("\nmin_sup_threshold: ")
    outfile.write(str(min_sup_threshold))

print()
print("#################################################")
print("Für die Webseite abspeichern...", time.time() - start_time)
frequent_itemsets.to_json(r"website\src\assets\json\frequent_itemsets.json", orient='records')
result.to_json(r"website\src\assets\json\association_rules.json", orient='records')

print()
print("#################################################")
print("Finished", time.time() - start_time)
