# -*- coding: utf-8 -*-
"""
Created on Tue Jan 13 14:27:37 2015

@author: feiwu
"""
import re
import time
import datetime
import cPickle as pickle
import dateutil.parser
       
## plotting stuff ##
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.dates as md
import math
def plotting_one_ts(x,y,ylabel = 'ylabel', path2save=None):
    f= figure()
    plt.xticks(rotation = 60)
    ax   = plt.gca()
    xfmt = md.DateFormatter('%Y-%m-%d')
    ax.xaxis.set_major_formatter(xfmt)
    plt.gcf().subplots_adjust(bottom = 0.3)
    plt.ylabel(ylabel)
    plt.scatter(x,y)
    if path2save != None:
        plt.savefig(path2save, format='pdf')

def plot_by_site(list_of_ts):
    pass

path2usgs_data  = "../data/qwdata"
PROCESS_RAW_DATA_FLAG = False
PROCESS_RAW_MAPPING   = False
path2_structured_data = "../data/data.pickle"
path2_site_no_mapping = "../data/mapping.pickle"
################### loading data or processing data from file ####################################
if PROCESS_RAW_DATA_FLAG:
    DB = read_usgs_data(path2usgs_data)
    pickle.dump(DB, open(path2_structured_data, 'wb'))
else:
    DB = pickle.load(open(path2_structured_data))


if PROCESS_RAW_MAPPING:
    all_sites_list  = get_site_no_mapping(path2usgs_data)
    pickle.dump(all_sites_list, open(path2_site_no_mapping, 'wb'))
else:
    all_sites_list  = pickle.load(open(path2_site_no_mapping))
test_ts = DB.get_raw_TS('01559795', '00940')

##################################################################################################


# an example of getting series from bobs creek
bobscreek_sites = search_target_names('Bobs', all_sites_list)

#TS_DB_usgs = read_usgs_data(path2usgs_data)
"""
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

"""
