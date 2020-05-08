# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 09:04:07 2020

@author: robi & phili
"""

import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import fpgrowth
import numpy as np
import csv
import time

start_time = time.time()

method = "fpgrowth"
min_support = 0.6
min_support_str =  str(min_support)
print("Start")
print("Min_Sup = " + min_support_str)
print("Method = " + method) 
df = pd.read_csv(r"..\7mioCrimes.csv", low_memory=False)

te = TransactionEncoder()
te_ary = te.fit(df).transform(df)
df2 = pd.DataFrame(te_ary, columns=te.columns_)

Vorbereitungszeit = time.time() - start_time
print("Vorbereitungszeit in Sekunden  = "+ str(Vorbereitungszeit) )

#frequent_itemsets = apriori(df1, min_support=0.0001, use_colnames=True, low_memory=True)
frequent_itemsets = fpgrowth(df2, min_support=min_support, use_colnames=True)
#fpmax(df, min_support=0.6, use_colnames=True)
print("Frequent_Itemsets created")


Laufzeit = time.time() - start_time
print("---  Laufzeit in Sekunden ---" + str(Laufzeit))

print("Save everything")


min_support_str_final = min_support_str.replace('.', '_')
csvFileName = "Frequent_Itemsets" + method + "TH_" + min_support_str_final + ".csv"
frequent_itemsets.to_csv(csvFileName, index=False)
print("Frequent Itemsets saved as csv") 
jsonFileName = "Frequent_Itemsets" + method + "TH_" + min_support_str_final +".json"
frequent_itemsets.to_json(jsonFileName, orient='records')
print("Frequent Itemsets saved as json") 
txtFileName = "Frequent_Itemsets" + method + "TH_" + min_support_str_final +".txt"
file = open(txtFileName,"w") 
 
file.write("MinSup: " + min_support_str) 
file.write("Method: " + method) 
file.write("Vorbereitungszeit: "+ str(Vorbereitungszeit) ) 
file.write("Laufzeit: " + str(Laufzeit)) 
 
file.close() 

##Anzahl der unique werde und die unique werte

print("Finished")