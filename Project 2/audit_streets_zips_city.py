import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import json
import pandas as pd

filename = 'c://users//bonnie//desktop//mark_work//nanodegree//data_wrangling//project_2//cleveland.osm'
osm_file = open(filename, 'r')

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

street_types = defaultdict(set)
postcodes = []
cities = []

# Cleveland zipcode data from http://www.zip-codes.com/city/OH-CLEVELAND.asp
# commented code was used to determine that bounding box of metro extract for 
# Cleveland included neighboring cities
#zips = pd.read_clipboard()
#zips['zip'] = zips['ZIP Code'].str.extract( r'(\d{5})' )
#cleveland_zips = zips['zip'].tolist()

expected = [ ] #'Avenue', 'Street', 'Road', 'Boulevard', 'Circle', 'Center', 'Court', 'Drive', 'Parkway', 'Square', 'Way']
ignore = ['Northeast',  'NE', 'Southeast', 'SE', 'East', 'Northwest', 'NW', 'West', 'North']

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            if street_type in ignore:
                street_type = street_name.split()[-2]
            street_types[street_type].add(street_name)
    
    #for k in keys:
    #    v = d[k]
    #    print "%s: %d" % (k, v)
    
def audit_postcode(postcodes, code):
#    if code not in cleveland_zips:
    postcodes.append(code)
        
def audit_city(cities, city):
    cities.append(city)
    
            
def is_street_name(elem):
    return (elem.attrib['k'] == 'addr:street')
    
def is_postal_code(elem):
    return (elem.attrib['k'] == 'addr:postcode')
    
def is_city(elem):
    return (elem.attrib['k'] == 'addr:city')
    
def audit():
    for event, elem in ET.iterparse(osm_file, events=('start',)):
        if elem.tag == "node" or elem.tag == "way" or elem.tag == "relation":
            for tag in elem.iter('tag'):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
                if is_postal_code(tag):
                    audit_postcode(postcodes, tag.attrib['v'])
                if is_city(tag):
                    audit_city(cities, tag.attrib['v'])
    return dict(street_types), set(postcodes), set(cities)

         
streets, codes, cities = audit()

#pprint.pprint(streets)
#pprint.pprint(codes)
#pprint.pprint(cities)

# need to convert sets to lists as sets are not JSON serializable
for k,v in streets.iteritems():
    streets[k] = list(v)
    
codes = list(codes)

cities = list(cities)

#output = json.dumps(streets)

with open('Cleveland_streets_data.json', 'w') as f: 
    f.write(json.dumps(streets, indent=2)+"\n")

with open('Cleveland_zipcodes_data.json', 'w') as f: 
    f.write(json.dumps(codes, indent=2)+"\n")

with open('Cleveland_city_data.json', 'w') as f: 
    f.write(json.dumps(cities, indent=2)+"\n")

