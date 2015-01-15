import time
import datetime
import dateutil.parser


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
        
   

class Site_TS_DB:
    def __init__(self, SiteDB=None):
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
            self.SiteDB[site_no][variable_code].append((time.mktime(timestamp), value, complete_date))
            print 'appended'
        except Exception as e:
            print e

    def get_raw_TS(self,site_num, var_code):
        if site_num not in self.SiteDB:
            return []
        if var_code not in self.SiteDB[site_num]:
            return []
        return self.SiteDB[site_num][var_code]
        
 
