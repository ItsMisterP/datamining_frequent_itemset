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
kluc_threshold = 0.55
kluc_range_max = 0.6
kluc_range_min = 0.5
imb_ratio_threshold = 0.25
association_rules_threshold = 0.6
min_sup_threshold = 0.001

start_time = time.time()
print("Start", time.time() - start_time)
df = pd.read_csv("7mioCrimes.csv", low_memory=False)
#print(df)
print("Eingelesen", time.time() - start_time)

df["time"] = df["time"].astype(str)
df["year"] = df["year"].astype(str)
#df['IUCR'] = df['IUCR'].astype(str)

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
print("Frequent_Itemsets created", time.time() - start_time)
frequent_itemsets.to_json("frequent_itemsets.json", orient='records')
print(len(frequent_itemsets))

result = own.association_rules(frequent_itemsets, min_threshold=association_rules_threshold)
print("Association Rules created")
print(len(result))

result.to_csv('out.csv', index=False)
print("Association Rules saved as csv") 
result[result['kluc'] >= kluc_threshold].to_json("association_rules.json", orient='records')

print("Filter Rules", time.time() - start_time)
df = result
#Füge eine neue Spalte mit der Länge dem Dataframe hinzu
print("Interesiting Kluc created")
df["antecedent_len"] = df["antecedents"].apply(lambda x: len(x))
kluc = df[ (df['antecedent_len'] >= show_rules) &
            (df['kluc'] >= kluc_threshold )& 
            (df['imbratio'] >= imb_ratio_threshold)]
kluc.to_csv('kluc.csv', index=False)
#print(kluc)
#Hier ist ein Dataframe, welches frozensets enthält -> deswegen Inhalt zu string konvertieren und dann contains prüfen können
#print(df2[df2['antecedents'].astype(str).str.contains(',')]) 
#print(df2)
print("interisting imb_ratio created", time.time() - start_time)
imb = df[ (df['antecedent_len'] >= show_rules)  & 
            ( (df['kluc'] < kluc_range_max) & (df['kluc'] >= kluc_range_min) )  & 
            (df['imbratio'] >= imb_ratio_threshold)]
imb.to_csv('imb.csv', index=False)
#print(imb)
#ownPrint.print_full(imb)
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
    outfile.write("\nkluc_threshold: ")
    outfile.write(str(kluc_threshold))
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

print("Save to Website", time.time() - start_time)
frequent_itemsets.to_json(r"website\src\assets\json\frequent_itemsets.json", orient='records')
result.to_json(r"website\src\assets\json\association_rules.json", orient='records')

print("Calculate Statistics", time.time() - start_time)
statistics.statistics()

print("Finished", time.time() - start_time)
