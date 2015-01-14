# -*- coding: utf-8 -*-
"""
Created on Tue Jan 13 14:27:37 2015

@author: feiwu
"""
import re
import time
import datetime


def read_usgs_data(filename):
    Flag  = True
    TS_DB  = dict()
    for oneline in open(filename,'r'):
        if "#" == oneline[0]:
            continue
        if Flag:
            head_line = oneline
            headers = oneline.rstrip('\n').rstrip('\r').split("\t")
            Flag    = False
            continue 
        if '5s' == oneline.split("\t")[0]:
            continue
        #print head_line
        #print oneline
        
        item_set    = oneline.split('\t')
        #print item_set
        agency_id   = item_set[0]
        site_num    = item_set[1]
        sample_date = item_set[2]
        sample_hours= item_set[3]
        complete_date = sample_date + " "+ sample_hours
        try:
            timestamp   = datetime.datetime.strptime(complete_date,"%Y-%m-%d %H:%M").timetuple()
        except Exception as e:
            print e
            continue
        variable_code=item_set[12].lower()
        if item_set[14] == '':
            continue
        value       = float(item_set[14])
        #print variable_cod
        if variable_code not in TS_DB:
            TS_DB[variable_code] = list()
        TS_DB[variable_code].append((time.mktime(timestamp),value))
    return TS_DB
        
        
    
def read_hydro_data(filename):
    Flag  = True
    TS_DB = dict()
    for oneline in open(filename):
        if "\"" == oneline[0] or 'Citation' == oneline[0:8] or ',' == oneline[0]:
            continue
        if Flag:
            Flag = False
            headers = oneline.rstrip('\n').rstrip('\r').split(",")
            continue
        item_set  = oneline.split(',')
        record_id = int(item_set[0])
        loc_id    = item_set[1]
        ts_name   = item_set[2].replace("\"","").lower()
        date_str  = item_set[3]
        timestamp = datetime.datetime.strptime(date_str,"%m/%d/%Y %H:%M").timetuple() ## this is in a time object
        value     = float(item_set[4])
        if "Bobs Creek" not in loc_id:
            continue
        if ts_name not in TS_DB:
            TS_DB[ts_name] = list()
        TS_DB[ts_name].append((time.mktime(timestamp),value))
    return TS_DB
import dateutil.parser
def get_merged_ts(DB_usgs, DB_hydro, tsname):
    if tsname == 'Chloride':
        hydro_key = 'chloride total'
        USGS_key  = '00940'
    if tsname == 'Barium':
        hydro_key = 'barium total'
        USGS_key  = '01007'
        DB_usgs[USGS_key] = list()
    if tsname == 'Strontium':
        hydro_key = 'strontium total'
        USGS_key  = '01080' #01080 unfiltered
    if tsname == 'specific conductivity':
        hydro_key = 'specific conductance'
        USGS_key1  = '00095' # 90095  
        USGS_key2  = '90095'
        DB_usgs['newkey'] = list(DB_usgs[USGS_key1]) + list(DB_usgs[USGS_key2])
        USGS_key = 'newkey'
    TS1       = DB_hydro[hydro_key]
    TS2       = DB_usgs[USGS_key]
    TS_list   = TS1+TS2
    x         = [datetime.datetime.fromtimestamp(e[0]).strftime('%Y-%m-%d %H:%M:%S') for e in TS_list]
    x         = [dateutil.parser.parse(s) for s in x]
    y         = [e[1] for e in TS_list]
    return x,y

path2hydro_data = "../bobcreek_hydro.csv"
path2usgs_data  = "../USGS_bobcreek_current"

TS_DB_hydro = read_hydro_data(path2hydro_data)
TS_DB_usgs = read_usgs_data(path2usgs_data)


chloride_ts  = get_merged_ts(TS_DB_usgs,TS_DB_hydro,'Chloride')
strontium_ts = get_merged_ts(TS_DB_usgs,TS_DB_hydro,'Strontium')
Barium_ts    = get_merged_ts(TS_DB_usgs,TS_DB_hydro,'Barium')
s_conductance_ts  = get_merged_ts(TS_DB_usgs,TS_DB_hydro,'specific conductivity')

import matplotlib.pyplot as plt
import matplotlib
import matplotlib.dates as md
import math
f1 = plt.figure()
plt.xticks(rotation = 60)
ax  = plt.gca()
xfmt = md.DateFormatter('%Y-%m-%d')
ax.xaxis.set_major_formatter(xfmt)
ax.set_yscale('log')
plt.gcf().subplots_adjust(bottom=0.3)
plt.ylabel('Strontium (mg/l)')
plt.scatter(strontium_ts[0],[x/1000 for x in strontium_ts[1]])
#plt.savefig('8a-unfiltered-recoverable.pdf', format='pdf')

f2 = plt.figure()
plt.xticks(rotation = 60)
ax  = plt.gca()
xfmt = md.DateFormatter('%Y-%m-%d')
ax.xaxis.set_major_formatter(xfmt)
plt.gcf().subplots_adjust(bottom=0.3)
plt.ylabel('Barium (mg/l)')
plt.scatter(Barium_ts[0],Barium_ts[1]) 
#plt.savefig('8b.pdf', format='pdf')

f3 = plt.figure()
plt.xticks(rotation = 60)
ax  = plt.gca()
xfmt = md.DateFormatter('%Y-%m-%d')
plt.gcf().subplots_adjust(bottom=0.3)
plt.ylabel('Chloride (mg/l)')
ax.xaxis.set_major_formatter(xfmt)
plt.scatter(chloride_ts[0], chloride_ts[1])
#plt.savefig('8c.pdf', format='pdf')

f4 = plt.figure()
plt.xticks(rotation = 60)
ax  = plt.gca()
xfmt = md.DateFormatter('%Y-%m-%d')
plt.gcf().subplots_adjust(bottom=0.3)
plt.ylabel('Specific Conductivity (Microsiemens per centimeter)')
ax.xaxis.set_major_formatter(xfmt)
plt.scatter(s_conductance_ts[0], s_conductance_ts[1])
#plt.savefig('8d.pdf', format='pdf')
#plt.scatter(chloride_ts[0], chloride_ts[1])
#plt.show()
