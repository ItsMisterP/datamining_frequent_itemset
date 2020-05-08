# -*- coding: utf-8 -*-
"""
Created on Fri May  8 13:16:55 2020

@author: robi & phili
"""


import AR_Vergleich as own


print("Start Skript")
min_sup = [0.05,0.01,0.001,0.0001]
min_conf = [1.0,1.25,1.5,2.0,5.0]
choose = ["PrimaryType","IUCR"]

for c in choose:
    for sup in min_sup:
        for conf in min_conf:
            own.run(sup, conf, "lift", c)
        
print("Finish Skript")