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
import parsing as parser    
from NewClass import Site_TS_DB, ob_Site
## plotting stuff ##
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.dates as md
import math
import Image

def plot_one_ts(x,y,ylabel = 'ylabel', path2save=None):
    f= plt.figure()
    ax   = plt.gca()
    xfmt = md.DateFormatter('%Y-%m-%d')
    ax.xaxis.set_major_formatter(xfmt)
    plt.gcf().subplots_adjust(bottom = 0.3)
    plt.ylabel(ylabel)
    plt.scatter(x,y)
    if path2save != None:
        plt.savefig(path2save, format = 'pdf')
    plt.show(block = False)


def plot_by_site(site_list, var_code,  DB, label_name= '', show_flag = True, save_path = None, datemap = dict(), name = '' ):
    f            = plt.figure()
    ax           = plt.gca()
    ax.set_color_cycle(['c','m','y','k','b','r','g'])
    xfmt = md.DateFormatter('%Y-%m-%d')
    ax.xaxis.set_major_formatter(xfmt)
    plt.gcf().subplots_adjust(bottom = 0.3)
    plt.xticks(rotation = 60)
    plt.ylabel(label_name)
    i_counter    = 0
    line_list    = []
    count = 0
    max_value = 0
    for site_no in site_list:
        raw_ts= DB.get_raw_TS(site_no, var_code)
        if len(raw_ts) == 0:
            continue
        count += len(raw_ts)
        x,y   = parser.raw_ts2xy(raw_ts)
        if max(y) > max_value:
            max_value = max(y)
        l     = ax.plot(x,y,'o', label= site_no)
    if name in datemap:
        date_x = [datetime.datetime.strptime(x,'%m/%d/%Y').timetuple() for x in datemap[name]]
        #date_x     = dateutil.parser.parse(spill_date)
        date_x = [datetime.datetime.fromtimestamp(time.mktime(x)).strftime('%m/%d/%Y') for x in date_x]
        date_x = [dateutil.parser.parse(x) for x in date_x]
        for x in date_x:
            ax.stem([x], [max_value+1], markerfmt = '')
    plt.legend(loc='upper left')
    if count != 0 and show_flag:
        f.show()
    if count != 0 and save_path != None:
        f.savefig(save_path, format='png')
        Image.open(save_path).save(save_path+'.jpg','JPEG')

def plot_by_site_subs(site_list, var_code,  DB):
    number_of_plots = len(site_list)+1
    f, axarr        = plt.subplots(number_of_plots, sharex = True, sharey= True)
    aggregated_x = list()
    aggregated_y = list()
    i_counter    = 0
    for site_no in site_list:
        raw_ts = DB.get_raw_TS(site_no, var_code)
        x,y   = parser.raw_ts2xy(raw_ts)
        axarr[i_counter].scatter(x,y)  
        aggregated_x += x
        aggregated_y += y
        i_counter += 1
    axarr[i_counter].scatter(aggregated_x,aggregated_y)
    plt.show()


global DB,all_sites_list

path2usgs_data  = "../data/qwdata"
PROCESS_RAW_DATA_FLAG = True#False
PROCESS_RAW_MAPPING   = True#False
path2_structured_data = "../data/data.pickle"
path2_site_no_mapping = "../data/mapping.pickle"
################### loading data or processing data from file ####################################
if PROCESS_RAW_DATA_FLAG:
    DB = parser.read_usgs_data(path2usgs_data)
    pickle.dump(DB, open(path2_structured_data, 'wb'))
else:
    DB = pickle.load(open(path2_structured_data))


if PROCESS_RAW_MAPPING:
    all_sites_list  = parser.get_site_no_mapping(path2usgs_data)
    pickle.dump(all_sites_list, open(path2_site_no_mapping, 'wb'))
else:
    all_sites_list  = pickle.load(open(path2_site_no_mapping))
#test_ts = DB.get_raw_TS('01559795', '00940')
#test_x,test_y = parser.raw_ts2xy(test_ts)
##################################################################################################


# an example of getting series from bobs creek
bobscreek_sites, site_names = parser.search_target_names('Bobs', all_sites_list)
def plot_by_query(oneplace,code):
    sites, site_names = parser.search_target_names(oneplace, all_sites_list)
    plot_by_site(sites, code, DB)


#TS_DB_usgs = read_usgs_data(path2usgs_data)

#################################################################################################
# Var_code mapping
# 
#  00940  - Chloride, water, filtered, milligrams per liter
#  91001  - Chloride, water, filtered, micrograms per liter
#  99220  - Chloride, water, unfiltered, milligrams per liter
#  71870  - Bromide, water, filtered, milligrams per liter
#  91000  - Bromide, water, filtered, micrograms per liter
#  91053  - Sodium, water, filtered, micrograms per liter  
#  00929  - Sodium, water, unfiltered, recoverable, milligrams per liter
#  00930  - Sodium, water, filtered, milligrams per liter
#  00935  - Potassium, water, filtered, milligrams per liter
#  00937  - Potassium, water, unfiltered, recoverable, milligrams per liter#  
#  00910  - Calcium, water, unfiltered, milligrams per liter as calcium carbonate
#  00915  - Calcium, water, filtered, milligrams per liter
#  00916  - Calcium, water, unfiltered, recoverable, milligrams per liter
#  00920  - Magnesium, water, unfiltered, milligrams per liter as calcium carbonate
#  00921  - Magnesium, water, unfiltered, recoverable, milligrams per liter
#  01005  - Barium, water, filtered, micrograms per liter
#  01006  - Barium, suspended sediment, recoverable, micrograms per liter
#  01007  - Barium, water, unfiltered, recoverable, micrograms per liter
#  01008  - Barium, bed sediment, recoverable, dry weight, milligrams per kilogram
#  01009  - Barium, water, unfiltered, recoverable, micrograms per liter
#  71885  - Iron, water, unfiltered, micrograms per liter
#  74010  - Iron, water, unfiltered, milligrams per liter
#  71883  - Manganese, water, unfiltered, micrograms per liter
#  00094  - Specific conductance, water, unfiltered, field, microsiemens per centimeter at 25 degrees Celsius
#  00095  - Specific conductance, water, unfiltered, microsiemens per centimeter at 25 degrees Celsius
#  00400  - pH, water, unfiltered, field, standard units
#  00403  - pH, water, unfiltered, laboratory, standard units
#  39036  - Alkalinity, water, filtered, fixed endpoint (pH 4.5) titration, field, milligrams per liter as calcium carbonate
#  39086  - Alkalinity, water, filtered, inflection-point titration method (incremental titration method), field, milligrams per liter as calcium carbonate
#  39087  - Alkalinity, water, filtered, inflection-point titration method (incremental titration method), laboratory, milligrams per liter as calcium carbonate
#  00945  - Sulfate, water, filtered, milligrams per liter
#  00946  - Sulfate, water, unfiltered, milligrams per liter
##############################################################################
var_map = {'cl':['00940','91001','99220'], 
           'br':['71870','91000'],
           'na':['91053','00929','00930'],
           'k' :['00935','00937'],
           'ca':['00910','00915','00916'],
           'mg':['00920','00921'],
           'ba':['01005','01006','01007','01008','01009'],
           'fe':['71885','74010'],
           'mn':['71883'],
           'conductivity':['00094','00095'],
           'ph':['00400', '00403'],
           'alkalinity':['39036','39086','39087'],
           's':['00945','00946']}
testlist = ['Cross Creek']
key_words_list = ['Cross Creek','Brush Run','Bobs', 'Laurel Run', 'Jacobs Creek', 'Dunkle Run', 
                  'Pine Creek', 'Sugar Creek','Sugar Run', 'Tenmile Creek', 'Towanda Creek',
                  ]
key_words_date = {'Tenmile Creek': ['07/05/2011'],
                  'Bobs': ['05/24/2010'],
                  'Pine Creek': ['03/13/2010','03/14/2010','01/06/2012','01/15/2012']}
path2save_figure = '../jpg_figure/'
STOP_FLAG = True
#if STOP_FLAG:
#    import sys
#    sys.exit()
for oneplace in key_words_list:
    sites, site_names = parser.search_target_names(oneplace, all_sites_list)
    for one_var in var_map:
        for one_code in var_map[one_var]:
            path2save = path2save_figure+oneplace.replace(" ","_")+'_'+one_var+'_'+one_code
            plot_by_site(sites, one_code,DB, one_var+':'+one_code+ ' (milligrams/L)',False,path2save, key_words_date, oneplace)
        





