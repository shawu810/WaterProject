from NewClass import Point
import parsing as parser
import cPickle as pickle
PROCESS_RAW = False

def construct_google_map_point(lat, lon):
    return "new google.maps.LatLng({0},{1})".format(str(lat), str(lon))
    

#def construct_point_var(target_site):
#    site   = DB[target_site][0]
#    lat    = site.lat
#    lon    = site.lon
#    name   = site.site_name
#    var_out= """var chicago = {0};  
#                var ouput   =' {1} <br> site number = {2}';""".format(construct_google_map_point(lat, lon), name, target_site)
#    return var_out

def construct_location_variable(target_sites):
    center_string = ""
    for site in target_sites:
        site = DB[site][0]
        lat  = site.lat
        lon  = site.lon
        name = site.site_name
        s    = site.site_no
        center_string += """["{}<br> id: USGS {} ",{},{}],""".format(name,s,str(lat),str(lon))
    center_string = center_string.rstrip(',')
    return "var locations = [{}];".format(center_string)

def construct_point_var(target_sites):
    site   = target_sites[0]
    site   = DB[site][0]
    lat    = site.lat
    lon    = site.lon
    var_out= """var point   = {0}; """.format(construct_google_map_point(lat, lon))
    return var_out


def load_template(path):
    return ''.join(open(path,'r').readlines())




def plot_sites(list_of_sites, path = '../visualization/test'):
    html        = load_template(path2template).replace('####', construct_point_var(list_of_sites)+ construct_location_variable(list_of_sites))
    f           = open(path+'.html','w')
    f.write(html)
    f.close()



global DB
path2template  = '../visualization/template2.html'
site_file_name = '../data/inventory'
pickle_file    = '../data/inventory.pickle'
if PROCESS_RAW:
    DB = parser.read_site_infor(site_file_name)
    pickle.dump(DB, open(pickle_file,'w'))
else:
    DB = pickle.load(open(pickle_file,'r'))


#plot_site(target_site)


muncy  =  ['01552500','01552800','01553005','01552975']
bobs   =  ['01559795', '01559800', '01559920', '0155979602']
tenmile=  ['03072813', '03072815', '03072817', '03072840', '03072850', '03073000', '03073535', '03073540', '03073600']
pine   =  ['01548500', '01549600', '01549700', '01548235', '03036240', '01471805']

plot_sites(muncy, '../visualization/muncy')
plot_sites(bobs, '../visualization/bobs')
plot_sites(tenmile, '../visualization/tenmile')
plot_sites(pine, '../visualization/pine')




