# -*- coding: utf-8 -*-
"""
Created on Fri May  8 13:07:25 2020

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

def run(min_sup_threshold, association_rules_threshold, metric, choose):
    #um die FirstRunStatistics zu speichern
    timestr = time.strftime("%Y%m%d-%H%M%S")
    def step_log(message, *args, **kwargs):
        timeee = (time.time() - start_time)/60
        #print("Step %d" % step_log.counter + "/%d: " % step_log.stepCount + message + " | time(m): ", "%.2f" % round(timeee, 2), *args, **kwargs)
        step_log.counter += 1
        step_log.stepCount = 10
    step_log.counter = 1
    step_log.stepCount = 10
    start_time = time.time()
    
    # =============================================================================
    #Variables
    kulc_range_min = 0.0
    kulc_range_max = 1.0
    imb_ratio_threshold = 0.25
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
    
    # =============================================================================
    
    df["time"] = df["time"].replace(["1","2","3","4","5", "6"], "Time: 1-6")
    df["time"] = df["time"].replace(["7","8","9","10","11","12"], "Time: 7-12")
    df["time"] = df["time"].replace(["13","14","15","16","17","18"], "Time: 13-18")
    df["time"] = df["time"].replace(["19","20","21","22","23","24"], "Time: 19-24")
      
    
    df = df.dropna()
    
    #Speiche die Columns, damit sie später in der Statistik auftauchen
    usedColumns = df.columns.to_numpy()
    
    
    df = df.to_numpy()
    #print(df)
    #print(df[df['IUCR'].str.contains('8')])
    # =============================================================================
    step_log("create Frequent Itemsets. Min-Sup: " + str(min_sup_threshold))
    te = TransactionEncoder()
    te_ary = te.fit(df).transform(df)
    df2 = pd.DataFrame(te_ary, columns=te.columns_)
    #frequent_itemsets = apriori(df1, min_support=0.0001, use_colnames=True, low_memory=True)
    frequent_itemsets = fpgrowth(df2, min_support=min_sup_threshold, use_colnames=True)
    # =============================================================================
    step_log("save Frequent Itemsets")
    frequent_itemsets.to_json("frequent_itemsets.json", orient='records')
    
    # =============================================================================
    step_log("create Association Rules. Metrik" + metric + " Threshold:" + str(association_rules_threshold))
    result = own.association_rules(frequent_itemsets, min_threshold=association_rules_threshold, metric=metric)
    
    #Postprocessing
    
    # =============================================================================
    
# =============================================================================
#     step_log("save Association Rules")
#     
#     result[(result['kulc'] >= kulc_range_min) & 
#             (result['kulc'] >= kulc_range_max)].to_json("association_rules.json", orient='records')
# =============================================================================
    result.to_json(r"website\src\assets\json\association_rules.json", orient='records')

    # =============================================================================
    step_log("save statistics for this Run")
    with io.open(r"StatisticsFirstRun\Vergleiche_FQ_Metric\AR_" + timestr + "_Statistics.json", 'w', encoding='utf-8') as outfile:
        outfile.write("Benutzte Spalten:")
        outfile.write(str(usedColumns).replace("\n",""))
        outfile.write("\nAnzahl Frequent Itemsets: ")
        outfile.write(str(len(frequent_itemsets)))
        outfile.write("\nAnzahl Association Rules: ")
        outfile.write(str(len(result)))
        outfile.write("\nZeit: ")
        outfile.write(str(time.time() - start_time))
        outfile.write("\nParameter: ")
#        outfile.write("\nkulc_range_max: ")   
#        outfile.write(str(kulc_range_max))
#        outfile.write("\nkulc_range_min: ")
#        outfile.write(str(kulc_range_min))
#        outfile.write("\nimb_ratio_threshold: ")
#        outfile.write(str(imb_ratio_threshold))
        outfile.write("\nassociation_rules_threshold: ")
        outfile.write(str(association_rules_threshold))
        outfile.write("\nmin_sup_threshold: ")
        outfile.write(str(min_sup_threshold))
        outfile.write("\nmetric: ")
        outfile.write(metric)
    
    result.to_json(r'StatisticsFirstRun\Vergleiche_FQ_Metric\AR_'+ timestr +'_Rules.json', orient='records')

    # =============================================================================
    step_log("finish")
    print("-------START---------")
    print("AR:")
    print(len(result))
    print("Min-Sup:", min_sup_threshold)
    print("association_rules_threshold:", str(association_rules_threshold))
    print("metric:", metric)
    print("Column:", choose)
    timeee = (time.time() - start_time)/60
    print("finish time(m): ", "%.2f" % round(timeee, 2))
    print("-------FINISH---------")