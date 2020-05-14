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
import logging
#um die FirstRunStatistics zu speichern
timestr = time.strftime("%Y%m%d-%H%M%S")
def step_log(message, *args, **kwargs):
    timeee = (time.time() - start_time)/60
    print("Step %d" % step_log.counter + "/%d: " % step_log.stepCount + message + " | time(m): ", "%.2f" % round(timeee, 2), *args, **kwargs)
    step_log.counter += 1
    step_log.stepCount = 9
step_log.counter = 1
step_log.stepCount = 9
start_time = time.time()

# =============================================================================
# pd.set_option('display.max_rows', 50000)
# pd.set_option('display.width', 10000)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_colwidth', None)
# =============================================================================

# =============================================================================
#Variables
show_rules = 0
kluc_range_min = 0.5
kluc_range_max = 1.0
imb_ratio_threshold = 0.0
association_rules_threshold = 0.0
min_sup_threshold = 0.00001
metric = "confidence"
choose = "PrimaryType"
# =============================================================================


# =============================================================================
 # =============================================================================
step_log("start")
df = pd.read_csv("7mioCrimes.csv", low_memory=False)
# =============================================================================
step_log("apply temporary filter")
# Mögliche Spalten: 
# ['time', 'District', 'year', 'Primary Type','IUCR','Block', 'Location Description', 'month', 'weekday', 't', 'Description']
df["time"] = df["time"].astype(str)
df["year"] = df["year"].astype(str)
df["District"] = df["District"].astype(str)

df["LocationDescription"] = df["Location Description"]
df["PrimaryType"] = df["Primary Type"]
df = df.drop(["Location Description"], axis=1)
df = df.drop(["Primary Type"], axis=1)
# =============================================================================
#drop IMMER
#df = df.drop(["time"], axis=1)
df = df.drop(["t"], axis=1)
df = df.drop(["year"], axis=1)
df = df.drop(["Block"], axis=1)
df = df.drop(["Description"], axis=1)
# =============================================================================

if(choose == "PrimaryType"):
    df = df.drop(["IUCR"], axis=1)
if(choose == "IUCR"):
    df = df.drop(["PrimaryType"], axis=1)
    df["IUCR"] = df["IUCR"].replace(to_replace=r'\,', value=' ', regex=True) 

#df = df.drop(["time"], axis=1)
print(df.columns)
# =============================================================================

df["time"] = df["time"].replace(["1","2","3","4","5", "6"], "Time: 1-6")
df["time"] = df["time"].replace(["7","8","9","10","11","12"], "Time: 7-12")
df["time"] = df["time"].replace(["13","14","15","16","17","18"], "Time: 13-18")
df["time"] = df["time"].replace(["19","20","21","22","23","24"], "Time: 19-24")
  



#extrahiert die monate! 
#df['DATE'] = df ['DATE'].str.extract("(\w*)/")
#df['DATE'] = df ['DATE'].str.replace("12", "Winter").str.replace("01", "Winter").str.replace("02", "Winter").str.replace("03", "Spring").str.replace("04", "Spring").str.replace("05", "Spring").str.replace("06", "Summer").str.replace("07", "Summer").str.replace("08", "Summer").str.replace("09", "Autumn").str.replace("10", "Autumn").str.replace("11", "Autumn")

df = df.dropna()

#Speiche die Columns, damit sie später in der Statistik auftauchen
usedColums = str(df.columns)
print(usedColums)

df_num = df.to_numpy()
#print(df)
#print(df[df['IUCR'].str.contains('8')])
# =============================================================================
step_log("create Frequent Itemsets. Min-Sup: " + str(min_sup_threshold))
te = TransactionEncoder()
te_ary = te.fit(df_num).transform(df_num)
df2 = pd.DataFrame(te_ary, columns=te.columns_)
#frequent_itemsets = apriori(df1, min_support=0.0001, use_colnames=True, low_memory=True)
frequent_itemsets = fpgrowth(df2, min_support=min_sup_threshold, use_colnames=True)
# =============================================================================
step_log("save Frequent Itemsets")
frequent_itemsets.to_json("frequent_itemsets.json", orient='records')

# =============================================================================
step_log("create Association Rules. Metrik" + metric + " Threshold:" + str(association_rules_threshold))
result = own.association_rules(frequent_itemsets, min_threshold=association_rules_threshold, metric=metric)
# =============================================================================
step_log("save Association Rules")

result[(result['kluc'] >= kluc_range_min)].to_json("association_rules.json", orient='records')

# =============================================================================
step_log("save statistics for this Run")
with io.open('StatisticsFirstRun/StatisticsFirstRun'+timestr+'.json', 'w', encoding='utf-8') as outfile:
    outfile.write("Benutzte Spalten:")
    outfile.write(usedColums)
    outfile.write("\nAnzahl Frequent Itemsets: ")
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
    outfile.write("\nmetric: ")
    outfile.write(metric)


# =============================================================================
step_log("save files for the website")
frequent_itemsets.to_json("website/src/assets/json/frequent_itemsets.json", orient='records')
result[(result['kluc'] >= kluc_range_min)].to_json("website/src/assets/json/association_rules.json", orient='records')
# =============================================================================
step_log("finish")

