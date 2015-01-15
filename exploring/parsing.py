# -*- coding: utf-8 -*-
"""
Created on Tue Jan 13 14:27:37 2015

@author: feiwu
"""
from NewClass import Site_TS_DB, ob_Site
import time
import datetime
import dateutil.parser
########################################################################################
# Method 
#######################################################################################
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
    sites_ids    = list() 
    sites_names  = list()
    for one_site in all_sites_list:
        if names in one_site.get_site_name():
            sites_ids.append(one_site.get_site_no())
            sites_names.append(one_site.get_site_name())
    return sites_ids,sites_names
 
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
       # try:
        DB.add_record( site_num,  variable_code, sample_date, sample_hours, value )
       # except Exception as e:
       #     print e 
    return DB   

def raw_ts2xy(TS_list):
    x         = [datetime.datetime.fromtimestamp(e[0]).strftime('%Y-%m-%d %H:%M:%S') for e in TS_list]
    x         = [dateutil.parser.parse(s) for s in x]
    y         = [e[1] for e in TS_list]
    return x,y



