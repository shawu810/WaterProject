# -*- coding: utf-8 -*-
"""
Created on Tue Jan 13 14:27:37 2015

@author: feiwu
"""
import re
import time
import datetime
import cPickle as pickle
class Record:
    def __init__(self, line ):
        item_set    = line.split('\t')
        self.agency_id   = item_set[0]
        self.site_num    = item_set[1]
        self.sample_date = item_set[2]
        self.sample_hours= item_set[3]
        self.complete_date= item_set[2]+item_set[3]
        
        
        


class ob_Site:
    def __init__(self, site_name = '', site_no = ''):
        self.site_no   = site_no
        self.site_name = site_name
    def get_site_name(self):
        return self.site_name
    def get_site_no(self):
        return self.site_no
        
def get_site_no_mapping(filename):
    Flag  = True
    all_sites = list()
    for oneline in open(filename,'r'):
        if 'agency_cd' in oneline and not Flag:
            break
        if 'Data for the following sites are included:' not in oneline and Flag:
            continue
        if Flag:
            Flag = False
            continue
        line_set = oneline.rstrip('\r\n').split(' ')
        try:
            site_no  = line_set[3]
            site_name= ' '.join(line_set[4:])
            one_site = ob_Site(site_name,site_no)
            all_sites.append(one_site)
        except Exception as e:
            print e
    return all_sites
    
def search_target_names(names, all_sites_list):
    sites_ids = list()    
    for one_site in all_sites_list:
        if names in one_site.get_site_name():
            sites_ids.append(one_site.get_site_no())
    return sites_ids
    

class Site_TS_DB:
    SiteDB = dict()
    def __intit__(self):
        self.SiteDB = dict()
    def add_site(self, site_no):
        if site_no not in self.SiteDB:
            self.SiteDB[site_no] = dict()
    def add_ts_v(self, site_no, var_name):
        if var_name not in self.SiteDB[site_no]:
            self.SiteDB[site_no][var_name] = list()            
    def add_record(self, site_no, var_name, sample_date, sample_hours, value) :
        self.add_site(site_no)
        self.add_ts_v(site_no, var_name)
        complete_date = sample_date+ " " + sample_hours
        try:
            timestamp = datetime.datetime.strptime(complete_date,"%Y-%m-%d %H:%M").timetuple()       
            variable_code=var_name.lower()
            value       = float(value)
        #print variable_cod
            self.SiteDB[site_no][variable_code].append((time.mktime(timestamp), value))
        except Exception as e:
            print e

def get_raw_TS(self,site_num, var_code):
     return self.SiteDB[site_num][var_code]
        
        
def read_usgs_data(filename):
    DB = Site_TS_DB()
    Flag  = True
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
        variable_code=item_set[12].lower()
        value       = item_set[14]
        try:
            DB.add_record( site_num,  variable_code, sample_date, sample_hours, value )
        except Exception as e:
            print e 
    return DB   


path2usgs_data  = "../data/qwdata"
all_sites_list  = get_site_no_mapping(path2usgs_data)

DB = read_usgs_data(path2usgs_data)

path2_structured_data = "../data/data.pickle"
pickle.dump(DB, open(path2_structured_data, 'wb'))


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
