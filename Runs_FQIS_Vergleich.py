# -*- coding: utf-8 -*-
"""
Created on Fri May  8 11:04:19 2020

@author: robi & phili
"""


import FQIS_Vergleich as own

print("Start Skript")
# =============================================================================
# laufzeiten = [0.6,0.5,0.25,0.1,0.05,0.01,0.005,0.001,0.0005,0.0001]
# choose = ["PrimaryType","IUCR"]
# 
# 
# for c in choose:
#     for lz in laufzeiten:
#         own.run(lz, c)
# 
# =============================================================================
own.run(0.001,"PrimaryType")

print("Finish Skript")