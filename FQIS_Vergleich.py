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
from mlxtend.frequent_patterns import fpmax
import numpy as np
import csv
import re
import association_rules as own
import io
import time
import statistics_bigdata as statistics
import logging


def run(min_sup_threshold, choose):
    #um die FirstRunStatistics zu speichern
    timestr = time.strftime("%Y%m%d-%H%M%S")
    def step_log(message, *args, **kwargs):
        timeee = (time.time() - start_time)
        #print("Step %d" % step_log.counter + "/%d: " % step_log.stepCount + message + " | time(m): ", "%.2f" % round(timeee, 2), *args, **kwargs)
        step_log.counter += 1
        step_log.stepCount = 6
    step_log.counter = 1
    step_log.stepCount = 6
    start_time = time.time()

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
      
    
    #df['IUCR'] = df['IUCR'].astype(str)
    
    #extrahiert die monate! 
    #df['DATE'] = df ['DATE'].str.extract("(\w*)/")
    #df['DATE'] = df ['DATE'].str.replace("12", "Winter").str.replace("01", "Winter").str.replace("02", "Winter").str.replace("03", "Spring").str.replace("04", "Spring").str.replace("05", "Spring").str.replace("06", "Summer").str.replace("07", "Summer").str.replace("08", "Summer").str.replace("09", "Autumn").str.replace("10", "Autumn").str.replace("11", "Autumn")
    
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
    #frequent_itemsets = apriori(df2, min_support=min_sup_threshold, use_colnames=True, low_memory=True)
    frequent_itemsets = apriori(df2, min_support=min_sup_threshold, use_colnames=True)
    #frequent_itemsets = fpgrowth(df2, min_support=min_sup_threshold, use_colnames=True)
    #frequent_itemsets = fpmax(df2, min_support=min_sup_threshold, use_colnames=True)
    # =============================================================================
    step_log("save Frequent Itemsets")
    frequent_itemsets.to_json("frequent_itemsets.json", orient='records')
    
    
    
    # =============================================================================
    step_log("save statistics for this Run")
    with io.open(r"StatisticsFirstRun\Vergleiche_FQ_Metric\FQIS_" + timestr + "_Statistics.json", 'w', encoding='utf-8') as outfile:
        outfile.write("Benutzte Spalten:")
        outfile.write(str(usedColumns).replace("\n",""))
        outfile.write("\nAnzahl Frequent Itemsets: ")
        outfile.write(str(len(frequent_itemsets)))
        outfile.write("\nZeit: ")
        outfile.write(str(time.time() - start_time))
        outfile.write("\nmin_sup_threshold: ")
        outfile.write(str(min_sup_threshold))
        
    frequent_itemsets.to_json(r'StatisticsFirstRun\Vergleiche_FQ_Metric\FQIS_'+ timestr +'_Itemsets.json', orient='records')
    
    print("FQIS:")
    print("Min-Sup:", min_sup_threshold)
    print("Column:", choose)
    print(len(frequent_itemsets))
    timeee = (time.time() - start_time)
    print("finish time(s): ", "%.2f" % round(timeee, 2))
