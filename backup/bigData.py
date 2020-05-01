#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 18:17:59 2020

@author: philip & robin
""" 

import pandas as pd
from datetime import datetime, timedelta 
import time
import re

start_time = time.time()

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
    
print('(1/9) start importing the csv')
df = pd.read_csv("Crimes_-_2001_to_present_19042020.csv", low_memory=False)


#Filtere für die passenden Spalten
print('(2/9) filter Columns | Time previous Step: ', time.time() - start_time)
columns = ['Date', 'Block', 'Primary Type', 'Description', 'Location Description', 'Year']
df = pd.DataFrame(df, columns=columns)

#Teile das Datum in eigene Spalten ein
print("(3/9) split date | Time in Secounds: ", time.time() - start_time)
df[['Date','time', 't']] = df['Date'].str.split(' ',expand=True)

#Passe die Blockspalte an
print("(4/9) customize the block column | Time in Secounds: ", time.time() - start_time)
df['Block'].replace(r'^\d\d\d\w\w\s\w\s', ' ', inplace=True, regex=True)

#Passe die Datumspalte an
print("(5/9) customize the date | in Secounds: ", time.time() - start_time)
day_name= ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag','Sonntag']
month_name= ['Januar', 'Februar', 'Maerz', 'April', 'Mai','Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
df["weekday"] = df["Date"].apply(lambda x: day_name[datetime.strptime(x, '%m/%d/%Y').weekday()])
df[['month', 'day', 'year']] = df['Date'].str.split('/',expand=True)
df["month"] = df["month"].apply(lambda x: month_name[int(x)-1])

#Entferne Komma in der Location Spalte
print("(6/9) customize the location | Time in Secounds: ", time.time() - start_time)
df['Location Description'].replace(r', ', ' - ', inplace=True, regex=True)

#Passe die Zeit zu deutschem Format an
print("(7/9) some more date things | Time in Secounds: ", time.time() - start_time)
df["time"] = df.apply((lambda x: format(datetime.strptime(x.time, '%H:%M:%S') + timedelta(hours=12),'%H') if "PM" in x.t else format(datetime.strptime(x.time, '%H:%M:%S'), '%H')), axis=1)

print("--------------Adding Prefixes--------------- | Time in Secounds: ", time.time() - start_time)
df["Block"] = df["Block"].replace(to_replace=r'^\s', value='bl_', regex=True) #hier ist das \s dabei, weil es mit nem Leerzeichen noch anfängt
df["Primary Type"] = df["Primary Type"].replace(to_replace=r'^', value='pr_', regex=True)
df["Description"] = df["Description"].replace(to_replace=r'^', value='de_', regex=True)
df["Location Description"] = df["Location Description"].replace(to_replace=r'^', value='lo_', regex=True)

#Entferne Ähnlichkeiten
print("--------------Remove Similarities------------- | Time in Secounds: ", time.time() - start_time)
#df["Primary Type"] = df["Primary Type"].replace("pr_CRIM SEXUAL ASSAULT", "pr_CRIMINAL SEXUAL ASSAULT") #geprüft3004
#df["Primary Type"] = df["Primary Type"].replace(["pr_NON - CRIMINAL", "pr_NON-CRIMINAL (SUBJECT SPECIFIED)" ], "pr_NON-CRIMINAL") #geprüft3004

#Stand 3004 von 213 auf 144 bei Location Description
print("--------------Remove Similarities------------- | Time in Secounds: ", time.time() - start_time)
df["Location Description"] = df["Location Description"].replace(to_replace=r'^lo_AIRPORT.+', value='lo_AIRPORT', regex=True) #geprüft3004 von 213 auf 201 
df["Location Description"] = df["Location Description"].replace(to_replace=r'\s*/\s*', value=' ', regex=True) ##geprüft3004 von 213 auf 198  
df["Location Description"] = df["Location Description"].replace("lo_BAR OR TAVERN", "lo_TAVERN") ##geprüft3004 von 213 auf 212
df["Location Description"] = df["Location Description"].replace(to_replace=r'^lo_CHA.+', value='lo_Chicago Housing Authority', regex=True) #geprüft3004 von 213 auf 201 
df["Location Description"] = df["Location Description"].replace("lo_DRIVEWAY - RESIDENTIAL", "lo_DRIVEWAY") ##geprüft3004 von 213 auf 212
df["Location Description"] = df["Location Description"].replace(["lo_FACTORY / MANUFACTURING BUILDING","lo_FACTORY/MANUFACTURING BUILDING"], "lo_FACTORY") ##geprüft3004 von 213 auf 211
df["Location Description"] = df["Location Description"].replace("lo_GARAGE/AUTO REPAIR", "lo_GARAGE") ##geprüft3004 von 213 auf 212
df["Location Description"] = df["Location Description"].replace("lo_GARAGE/AUTO REPAIR", "lo_GARAGE") ##geprüft3004 von 213 auf 212
df["Location Description"] = df["Location Description"].replace(["lo_GOVERNMENT BUILDING / PROPERTY","lo_GOVERNMENT BUILDING/PROPERTY"], "lo_GOVERNMENT BUILDING") ##geprüft3004 von 213 auf 211
df["Location Description"] = df["Location Description"].replace(to_replace=r'^lo_OTHER.+', value='lo_OTHER', regex=True) #geprüft3004 von 213 auf 209
df["Location Description"] = df["Location Description"].replace(to_replace=r'^lo_PARKING LOT.+', value='lo_PARKING LOT', regex=True) #geprüft3004 von 213 auf 211
df["Location Description"] = df["Location Description"].replace(to_replace=r'^lo_RESIDENCE.+', value='lo_RESIDENCE', regex=True) #geprüft3004 von 213 auf 208
df["Location Description"] = df["Location Description"].replace("lo_RESIDENTIAL YARD (FRONT/BACK)", "lo_RESIDENCE") ##geprüft3004 von 213 auf 212
df["Location Description"] = df["Location Description"].replace("lo_RIVER BANK", "lo_RIVER") ##geprüft3004 von 213 auf 212
df["Location Description"] = df["Location Description"].replace("lo_POOL ROOM", "lo_POOLROOM") ##geprüft3004 von 213 auf 212
df["Location Description"] = df["Location Description"].replace(to_replace=r'^lo_SCHOOL.+', value='lo_SCHOOL', regex=True) #geprüft3004 von 213 auf 205
df["Location Description"] = df["Location Description"].replace("lo_TAXI CAB", "lo_TAXICAB") ##geprüft3004 von 213 auf 212
df["Location Description"] = df["Location Description"].replace(to_replace=r'^lo_VEHICLE.+', value='lo_VEHICLE', regex=True) #geprüft3004 von 213 auf 205
df["Location Description"] = df["Location Description"].replace(to_replace=r'^lo_CTA.+', value='lo_Chicago Transit Authority', regex=True) 
df["Location Description"] = df["Location Description"].replace("lo_BARBER SHOP BEAUTY SALON", "lo_BARBERSHOP") 
df["Location Description"] = df["Location Description"].replace(to_replace=r'^lo_CHURCH.+', value='lo_CHURCH', regex=True) 
df["Location Description"] = df["Location Description"].replace(to_replace=r'^lo_COLLEGE.+', value='lo_COLLEGE', regex=True) 
df["Location Description"] = df["Location Description"].replace("lo_FACTORY MANUFACTURING BUILDING", "lo_FACTORY") 
df["Location Description"] = df["Location Description"].replace("lo_GAS STATION DRIVE PROP.", "lo_GAS STATION") 
df["Location Description"] = df["Location Description"].replace("lo_GOVERNMENT BUILDING PROPERTY", "lo_GOVERNMENT BUILDING") 
df["Location Description"] = df["Location Description"].replace("lo_HOSPITAL BUILDING GROUNDS", "lo_HOSPITAL") 
df["Location Description"] = df["Location Description"].replace("lo_HOTEL MOTEL", "lo_HOTEL") 
df["Location Description"] = df["Location Description"].replace("lo_LAKEFRONT WATERFRONT RIVERBANK", "lo_LAKE") 
df["Location Description"] = df["Location Description"].replace(["lo_NURSING HOME RETIREMENT HOME","lo_NURSING RETIREMENT HOME"], "lo_NURSING HOME") 
df["Location Description"] = df["Location Description"].replace("lo_POLICE FACILITY VEH PARKING LOT", "lo_POLICE FACILITY VEHICLE PARKING LOT") 
df["Location Description"] = df["Location Description"].replace(["lo_PUBLIC GRAMMAR SCHOOL","lo_PUBLIC HIGH SCHOOL"], "lo_SCHOOL") 
df["Location Description"] = df["Location Description"].replace("lo_RESIDENTIAL YARD (FRONT BACK)", "lo_RESIDENCE") 
df["Location Description"] = df["Location Description"].replace("lo_TAVERN LIQUOR STORE", "lo_TAVERN") 
df["Location Description"] = df["Location Description"].replace("lo_TRUCKING TERMINAL", "lo_TRUCK") 
df["Location Description"] = df["Location Description"].replace("lo_VACANT LOT LAND", "lo_VACANT LOT LAND") 
df["Location Description"] = df["Location Description"].replace("lo_CLEANERS LAUNDROMAT", "lo_CLEANING STORE") 
print("--------------Location Description Done------------- | Time in Secounds: ", time.time() - start_time)



df["Description"] = df["Description"].replace(to_replace=r'^de_AGG\s', value='de_AGGRAVATED ', regex=True) 
df["Description"] = df["Description"].replace(to_replace=r'^de_AGG.\s', value='de_AGGRAVATED ', regex=True) 
df["Description"] = df["Description"].replace(to_replace=r'^de_AGG:\s', value='de_AGGRAVATED ', regex=True) 
df["Description"] = df["Description"].replace(to_replace=r'^de_AGG:\s', value='de_AGGRAVATED ', regex=True) 
df["Description"] = df["Description"].replace(to_replace=r'^de_AGGRAVATED\s-', value='de_AGGRAVATED', regex=True) 
df["Description"] = df["Description"].replace(to_replace=r'^de_AGGRAVATED:', value='de_AGGRAVATED ', regex=True) 
df["Description"] = df["Description"].replace(to_replace=r'P.O.', value='POLICE OFFICER', regex=True) 
df["Description"] = df["Description"].replace(to_replace=r'PO:', value='POLICE OFFICER ', regex=True) 
df["Description"] = df["Description"].replace(to_replace=r'\s*/\s*', value=' ', regex=True)  
df["Description"] = df["Description"].replace(["de_ABUSE NEGLECT - CARE FACILITY","de_ABUSE NEGLECT: CARE FACILITY"], "de_ABUSE NEGLECT CARE FACILITY") 

df["Description"] = df["Description"].replace(to_replace=r'-', value=' ', regex=True)  
df["Description"] = df["Description"].replace(to_replace=r':', value=' ', regex=True)  
df["Description"] = df["Description"].replace(to_replace=r'\.', value=' ', regex=True) 
df["Description"] = df["Description"].replace(to_replace=r'\,', value=' ', regex=True)   
df["Description"] = df["Description"].replace(to_replace=r'\s+', value=' ', regex=True)
df["Description"] = df["Description"].replace(to_replace=r'\sOF\s', value=' ', regex=True)  

df["Description"] = df["Description"].replace(to_replace=r'^de_MANU DEL\s', value='de_MANUFACTURE DELIVER ', regex=True) 
df["Description"] = df["Description"].replace(to_replace=r'^de_MANU DELIVER\s', value='de_MANUFACTURE DELIVER ', regex=True) 
df["Description"] = df["Description"].replace(to_replace=r'^de_POSS\s', value='de_POSSESSION ', regex=True) 
df["Description"] = df["Description"].replace(to_replace=r'^de_POS\s', value='de_POSSESSION ', regex=True) 
df["Description"] = df["Description"].replace(to_replace=r'^de_POSSESS\s', value='de_POSSESSION ', regex=True) 
df["Description"] = df["Description"].replace(to_replace=r'^de_UNLAWFUL POSS\s', value='de_UNLAWFUL POSSESSION ', regex=True) 
df["Description"] = df["Description"].replace("de_AGGRAVATED FINANCIAL ID THEFT", "de_AGGRAVATED FINANCIAL IDENTITY THEFT") 
df["Description"] = df["Description"].replace(to_replace=r'\sFIST\s', value=' FISTS ', regex=True) 
df["Description"] = df["Description"].replace(["de_AGGRAVATED KNIFE CUT INSTR","de_AGGRAVATED KNIFE CUTTING INSTR"], "de_AGGRAVATED KNIFE CUTTING INSTRUMENT") 
df["Description"] = df["Description"].replace(to_replace=r'\sDANG\s', value=' DANGEROUS ', regex=True)
df["Description"] = df["Description"].replace(to_replace=r'\sWEAP\s', value=' WEAPON ', regex=True)  
df["Description"] = df["Description"].replace(to_replace=r'\sCUT\sINSTR\s', value=' CUTTING INSTRUMENT ', regex=True) 
df["Description"] = df["Description"].replace(to_replace=r'\sINJ\s', value=' INJURY ', regex=True) 
df["Description"] = df["Description"].replace(to_replace=r'\sPO\s', value=' POLICE OFFICER ', regex=True) 
df["Description"] = df["Description"].replace(to_replace=r'^de_ATT\s', value='de_ATTEMPT ', regex=True) 
df["Description"] = df["Description"].replace(to_replace=r'\sAGG\s', value=' AGGRAVATED ', regex=True) 
df["Description"] = df["Description"].replace(to_replace=r'^de_CRIM\s', value='de_CRIMINAL ', regex=True) 
df["Description"] = df["Description"].replace(to_replace=r'\sCRIM\s', value=' CRIMINAL ', regex=True) 
df["Description"] = df["Description"].replace(to_replace=r'^de_DEL\s', value='de_DELIVER ', regex=True) 
df["Description"] = df["Description"].replace("de_FINAN EXPOLICE OFFICERTELDERLY DISABLED", "de_FINANCIAL EXPOLICE OFFICERTATION OF AN ELDERLY OR DISABLED PERSON")
df["Description"] = df["Description"].replace(to_replace=r'\sID\s', value=' IDENTITY ', regex=True) 
df["Description"] = df["Description"].replace(to_replace=r'\sDELIVERIVER\s', value=' DELIVER ', regex=True) 
df["Description"] = df["Description"].replace(to_replace=r'\sDRUG\s', value=' DRUGS ', regex=True) 
df["Description"] = df["Description"].replace("de_NONCONSENSUAL DISSEMINATION PRIVATE SEXUAL IMAGES", "de_NONCONSENSUAL DISSEMINATION OF PRIVATE SEXUAL IMAGES")
df["Description"] = df["Description"].replace("de_SALE DIST OBSCENE MAT TO MINOR", "de_SALE DISTRIBUTE OBSCENE MATERIAL TO MINOR")
df["Description"] = df["Description"].replace("de_SALE TOBACCO POLICE OFFICERUCTS TO MINOR", "de_SALE OF TOBACCO POLICE OFFICERUCTS TO MINOR")
df["Description"] = df["Description"].replace(to_replace=r'\sPOSSESSIONESSION\s', value='POSSESSION ', regex=True) 
df["Description"] = df["Description"].replace("de_FINANCIAL IDENTITY THEFT $300 &UNDER", "de_FINANCIAL IDENTITY THEFT $300 AND UNDER")
df["Description"] = df["Description"].replace("de_FINANCIAL IDENTITY THEFT OVER $ 300", "de_FINANCIAL IDENTITY THEFT OVER $300")
df["Description"] = df["Description"].replace(["de_MANUFACTURE DELIVER HEROIN (BLACK TAR)", "de_MANUFACTURE DELIVER HEROIN (TAN BROWN TAR)", "de_MANUFACTURE DELIVER HEROIN (WHITE)", "de_MANUFACTURE DELIVER HEROIN(BLACK TAR)", "de_MANUFACTURE DELIVER HEROIN(BRN TAN)"], "de_MANUFACTURE DELIVER HEROIN")
df["Description"] = df["Description"].replace("de_NON CONSENSUAL DISSEMINATION PRIVATE SEXUAL IMAGES", "de_NON CONSENSUAL DISSEMINATION OF PRIVATE SEXUAL IMAGES")
df["Description"] = df["Description"].replace(to_replace=r'\sHEROIN(BLACK\sTAR)', value='HEROIN', regex=True) 
df["Description"] = df["Description"].replace(to_replace=r'\sHEROIN(BRN\sTAN)', value='HEROIN', regex=True) 
df["Description"] = df["Description"].replace(to_replace=r'\sHEROIN(WHITE)', value='HEROIN', regex=True) 
df["Description"] = df["Description"].replace(to_replace=r'\sHEROIN\s(BLACK\sTAR)', value='HEROIN', regex=True) 
df["Description"] = df["Description"].replace(to_replace=r'\sHEROIN\s(BRN\sTAN)', value='HEROIN', regex=True) 
df["Description"] = df["Description"].replace(to_replace=r'\sHEROIN\s(WHITE)', value='HEROIN', regex=True) 
df["Description"] = df["Description"].replace(to_replace=r'\sHEROIN\s(TAN\sBROWN\sTAR)', value='HEROIN', regex=True) 
df["Description"] = df["Description"].replace(to_replace=r'^de_SALE DEL\s', value='de_SALE DELIVER ', regex=True) 
df["Description"] = df["Description"].replace("de_SELL GIVE DEL LIQUOR TO MINOR", "de_SELL GIVE DELIVER LIQUOR TO MINOR")
df["Description"] = df["Description"].replace(["de_SEX OFFENDER FAIL REG NEW ADD", "de_SEX OFFENDER FAIL TO REGISTER"], "de_SEX OFFENDER FAIL TO REGISTER NEW ADDRESS")
df["Description"] = df["Description"].replace(to_replace=r'^de_SOLICIT\s', value='de_SOLICITING ', regex=True) 
df["Description"] = df["Description"].replace(to_replace=r'PUBLICWAY', value='PUBLIC WAY', regex=True) 
df["Description"] = df["Description"].replace("de_THEFT BY LESSEE MOTOR VEH", "de_THEFT BY LESSEE MOTOR VEHICLE")
df["Description"] = df["Description"].replace("de_THEFT BY LESSEE NON VEH", "de_THEFT BY LESSEE NON MOTOR VEHICLE")
df["Description"] = df["Description"].replace("de_THEFT OF LOST MISLAID POLICE OFFICER", "de_THEFT OF LOST MISLAID POLICE OFFICERERTY")
df["Description"] = df["Description"].replace("de_THEFT RECOVERY TRUCK BUS MHOME", "de_THEFT RECOVERY TRUCK BUS MOBILE HOME")
df["Description"] = df["Description"].replace("de_UNLAWFUL POSSESSION HANDGUN", "de_UNLAWFUL POSSESSION OF HANDGUN")
df["Description"] = df["Description"].replace("de_UNLAWFUL USE SALE AIR RIFLE", "de_UNLAWFUL USE SALE OF AIR RIFLE")
df["Description"] = df["Description"].replace(to_replace=r'\sREG\s', value=' REGISTRATION ', regex=True) 
df["Description"] = df["Description"].replace(to_replace=r'^de_VIO\s', value='de_VIOLATION ', regex=True) 
df["Description"] = df["Description"].replace(to_replace=r'^de_VIOL\s', value='de_VIOLATION ', regex=True) 
df["Description"] = df["Description"].replace(to_replace=r'^de_VIOLATE\s', value='de_VIOLATION ', regex=True) 
df["Description"] = df["Description"].replace(["de_VIOLENT OFFENDER ANNUAL REGISTRATION", "de_VIOLENT OFFENDER DUTY TO REGISTER"], "de_VIOLENT OFFENDER FAIL TO REGISTER NEW ADDRESS")
df["Description"] = df["Description"].replace("de_AGGRAVATED CRIMINAL SEX ABUSE FAM MEMBER", "de_AGGRAVATED CRIMINAL SEXUAL ABUSE BY FAMILY MEMBER")
df["Description"] = df["Description"].replace(["de_AGGRAVATED DOMESTIC BATTERY KNIFE CUTTING INST", "de_AGGRAVATED DOMESTIC BATTERY KNIFE CUTTING INSTRUMENT"], "de_AGGRAVATED DOMESTIC BATTERY KNIFE CUTTING INSTSTRUMENT")
df["Description"] = df["Description"].replace("de_AGGRAVATED POLICE OFFICER HANDS ETC SERIOUS INJ", "de_AGGRAVATED POLICE OFFICER HANDS FISTS FEET SERIOUS INJURY")
df["Description"] = df["Description"].replace("de_AGGRAVATED POLICE OFFICER KNIFE CUT INSTR", "de_AGGRAVATED POLICE OFFICER KNIFE CUTTING INSTRUMENT")
df["Description"] = df["Description"].replace("de_AGGRAVATED POLICE OFFICER OTHER DANGEROUS WEAP", "de_AGGRAVATED POLICE OFFICER OTHER DANGEROUS WEAPON")
df["Description"] = df["Description"].replace(["de_AGGRAVATED POLICE OFFICERECTED EMPOLICE OFFICEREE HANDGUN", "de_AGGRAVATED POLICE OFFICEREMP HANDGUN"], "de_AGGRAVATED POLICE OFFICER HANDGUN")
df["Description"] = df["Description"].replace(["de_AGGRAVATED POLICE OFFICERECTED EMPOLICE OFFICEREE HANDS FISTS FEET SERIOUS INJURY", "de_AGGRAVATED POLICE OFFICEREMP HANDS SERIOUS INJ"], "de_AGGRAVATED POLICE OFFICER HANDS FISTS FEET SERIOUS INJURY")
df["Description"] = df["Description"].replace(["de_AGGRAVATED POLICE OFFICERECTED EMPOLICE OFFICEREE KNIFE CUTTING INSTRUMENT", "de_AGGRAVATED POLICE OFFICEREMP KNIFE CUTTING INST"], "de_AGGRAVATED POLICE OFFICER KNIFE CUTTING INSTRUMENT")
df["Description"] = df["Description"].replace(["de_AGGRAVATED POLICE OFFICERECTED EMPOLICE OFFICEREE OTHER DANGEROUS WEAPON", "de_AGGRAVATED POLICE OFFICEREMP OTHER DANGEROUS WEAPON"], "de_AGGRAVATED POLICE OFFICER OTHER DANGEROUS WEAPON")
df["Description"] = df["Description"].replace(["de_AGGRAVATED POLICE OFFICERECTED EMPOLICE OFFICEREE OTHER FIREARM", "de_AGGRAVATED POLICE OFFICEREMP OTHER DANGEROUS WEAPON"], "de_AGGRAVATED POLICE OFFICEREMP OTHER FIREARM")
df["Description"] = df["Description"].replace("de_AGGRAVATED SEX ASSLT CHILD FAM MBR", "de_AGGRAVATED SEXUAL ASSAULT CHILD BY FAMILY MEMBER")
df["Description"] = df["Description"].replace("de_ATTEMPT STRONGARM NO WEAPON", "de_ATTEMPT STRONG ARM NO WEAPON")
df["Description"] = df["Description"].replace("de_CONTRIBUTE TO THE CRIMINAL DELINQUENCY CHILD", "de_CONTRIBUTE TO THE DELINQUENCY CHILD")
df["Description"] = df["Description"].replace("de_CRIMINAL SEX ABUSE BY FAM MEMBER", "de_CRIMINAL SEXUAL ABUSE BY FAMILY MEMBER")
df["Description"] = df["Description"].replace("de_CYCLE SCOOTER BIKE W VIN", "de_CYCLE SCOOTER BIKE WITH VIN")
df["Description"] = df["Description"].replace("de_DEFACE IDENT MARKS FIREARM", "de_DEFACE IDENTIFICATION MARKS FIREARM")
df["Description"] = df["Description"].replace("de_FINAN EXPOLICE OFFICERT ELDERLY DISABLED", "de_FINANCIAL EXPOLICE OFFICERTATION AN ELDERLY OR DISABLED PERSON")
df["Description"] = df["Description"].replace("de_INDECENT SOLICITATION A CHILD", "de_INDECENT SOLICITATION CHILD")
df["Description"] = df["Description"].replace("de_KEEP PLACE JUV POLICE OFFICERTITUTION", "de_KEEP PLACE POLICE OFFICERTITUTION")
df["Description"] = df["Description"].replace("de_MANUFACTURE DELIVER CANNABIS 10GM OR LESS", "de_MANUFACTURE DELIVER CANNABIS 10 GRAMS OR LESS")
df["Description"] = df["Description"].replace("de_MANUFACTURE DELIVER CANNABIS OVER 10 GMS", "de_MANUFACTURE DELIVER CANNABIS OVER 10 GRAMS")
df["Description"] = df["Description"].replace("de_POLICE OFFICERECTED EMPOLICE OFFICEREE HANDS NO MIN INJURY", "de_POLICE OFFICERECTED EMPOLICE OFFICEREE HANDS FISTS FEET NO MINOR INJURY")
df["Description"] = df["Description"].replace("de_POLICE OFFICEREMP HANDS NO MIN INJURY", "de_POLICE OFFICERECTED EMPOLICE OFFICEREE HANDS FISTS FEET NO MINOR INJURY")
df["Description"] = df["Description"].replace("de_POSSESSION BARBITUATES", "de_POSSESSION BARBITURATES")
df["Description"] = df["Description"].replace("de_POSSESSION CANNABIS 30GMS OR LESS", "de_POSSESSION CANNABIS 30 GRAMS OR LESS")
df["Description"] = df["Description"].replace("de_POSSESSION CANNABIS MORE THAN 30GMS", "de_POSSESSION CANNABIS MORE THAN 30 GRAMS")
df["Description"] = df["Description"].replace("de_POSSESSION FIREARM AMMO NO FOID CARD", "de_POSSESSION FIREARM AMMUNITION NO FOID CARD")
df["Description"] = df["Description"].replace(to_replace=r'\sMETHAMPHETAMINE\s', value=' METHAMPHETAMINES ', regex=True) 
df["Description"] = df["Description"].replace("de_SEX ASSLT CHILD BY FAM MBR", "de_SEXUAL ASSAULT CHILD BY FAMILY MEMBER")
df["Description"] = df["Description"].replace("de_SEX RELATION IN FAMILY", "de_SEXUAL RELATIONS IN FAMILY")
df["Description"] = df["Description"].replace("de_SOLICITING FOR A POLICE OFFICERTITUTE", "de_SOLICITING FOR POLICE OFFICERTITUTE")
df["Description"] = df["Description"].replace("de_STOLEN POLICE OFFICER BUY RECEIVE POS", "de_STOLEN POLICE OFFICERERTY BUY RECEIVE POSSESS")
df["Description"] = df["Description"].replace("de_STRONGARM NO WEAPON", "de_STRONG ARM NO WEAPON")
df["Description"] = df["Description"].replace("de_THEFT LOST MISLAID POLICE OFFICERERTY", "de_THEFT LOST MISLAID POLICE OFFICER")
df["Description"] = df["Description"].replace("de_TO STATE SUPOLICE OFFICERTED POLICE OFFICERERTY", "de_TO STATE SUP POLICE OFFICER")
df["Description"] = df["Description"].replace("de_VIOLATION BAIL BOND DOMESTIC VIOLENCE", "de_VIOLATION BAIL BOND DOM VIOLENCE")
print("--------------Description Done------------- | Time in Secounds: ", time.time() - start_time)

#von 4208 auf -3260 mit upper allein
df["Block"] = df["Block"].str.upper()
df["Block"] = df["Block"].replace(to_replace=r'BL_\s.', value='', regex=True) 
df["Block"] = df["Block"].replace(to_replace=r'\s+', value=' ', regex=True)
df["Block"] = df["Block"].replace(to_replace=r'\dTH\s', value=' ', regex=True) 
df["Block"] = df["Block"].replace(to_replace=r'\dND\s', value=' ', regex=True) 
df["Block"] = df["Block"].replace(to_replace=r'\dRD\s', value=' ', regex=True) 
df["Block"] = df["Block"].replace(to_replace=r'\dST\s', value=' ', regex=True)
df["Block"] = df["Block"].replace(to_replace=r'\d\sTH\s', value=' ', regex=True) 
df["Block"] = df["Block"].replace(to_replace=r'\d\sND\s', value=' ', regex=True) 
df["Block"] = df["Block"].replace(to_replace=r'\d\sRD\s', value=' ', regex=True) 
df["Block"] = df["Block"].replace(to_replace=r'\d\sST\s', value=' ', regex=True)
df["Block"] = df["Block"].replace(to_replace=r'\s\bSTREET\b', value=' ST', regex=True)
df["Block"] = df["Block"].replace(to_replace=r'\s\bPLACE\b', value=' ST', regex=True) 
df["Block"] = df["Block"].replace(to_replace=r'\s\bBLVD\b', value=' BL', regex=True)
df["Block"] = df["Block"].replace(to_replace=r'\s\bAV\b', value=' AVE', regex=True) 
df["Block"] = df["Block"].replace(to_replace=r'\s\bTR\b', value=' TER', regex=True) 
df["Block"] = df["Block"].replace(to_replace=r'\s\bSTREET\b', value=' ST', regex=True)
df["Block"] = df["Block"].replace(to_replace=r'\s\bDRIVE\b', value=' DR', regex=True)
df["Block"] = df["Block"].replace(to_replace=r'\s\bAVENUE\b', value=' AVE', regex=True)
df["Block"] = df["Block"].replace(to_replace=r'\s\bPARK\b', value=' PK', regex=True)  
df["Block"] = df["Block"].replace(to_replace=r'\s\bSQUARE\b', value=' SQ', regex=True) 
df["Block"] = df["Block"].replace(to_replace=r'\s\bPLACE\b', value=' ST', regex=True) 
df["Block"] = df["Block"].replace(to_replace=r'\s\bBLVD\b', value=' BL', regex=True)
df["Block"] = df["Block"].replace(to_replace=r'\s\bAV\b', value=' AVE', regex=True) 
df["Block"] = df["Block"].replace(to_replace=r'\s\bTR\b', value=' TER', regex=True) 
df["Block"] = df["Block"].replace(to_replace=r'\s\bAVE\b\s\w.+', value=' AVE', regex=True) 
df["Block"] = df["Block"].replace(to_replace=r'\s\bST\b\s\w.+', value=' ST', regex=True)
df["Block"] = df["Block"].replace(to_replace=r'\s\bPL\b\s\w.+', value=' PL', regex=True) 
df["Block"] = df["Block"].replace(to_replace=r'\s\bRD\b\s\w.+', value=' PL', regex=True) 
df["Block"] = df["Block"].replace(to_replace=r'\s\bPW\b', value=' PKWY', regex=True)
df["Block"] = df["Block"].replace(to_replace=r'\s\bPZ\b', value=' PLZ', regex=True)

df["Block"] = df["Block"].replace(to_replace=r'\.', value='', regex=True)

print("--------------Block Done------------- | Time in Secounds: ", time.time() - start_time)




columns = ['time', 'Block', 'Primary Type', 'Description', 'Location Description', 'year', 'month', 'weekday', 't']
df = pd.DataFrame(df, columns=columns)
df.dropna()
print("(8/9) start preparing for printing | Time in Secounds: ", time.time() - start_time)
print(df)

print('(9/9) start saving as csv | Time previous Step: ', time.time() - start_time)
df.to_csv('7mioCrimes.csv', index=False)


Laufzeit = time.time() - start_time
print("Finished, Time: ", Laufzeit)