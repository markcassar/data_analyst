#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
"""
Your task is to wrangle the data and transform the shape of the data
into the model we mentioned earlier. The output should be a list of dictionaries
that look like this:

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}


"""


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
colon_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
address = re.compile(r'^addr:')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

mapping = { "St": "Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "ave": "Avenue",
            "Rd.": "Road",
            "Rd": "Road",
            "Dr": "Drive",
            "E": "East",
            "E.": "East",
            "W": "West",
            "W.": "West",
            "N": "North",
            "N.": "North",
            "S": "South",
            "S.": "South",
            "NE": "Northeast",
            "NW": "Northwest",
            "SE": "Southeast",
            "Blvd.": "Boulevard",
            "Blvd" : "Boulevard",
            "SR": "State Route",
            }
            
oddities = {'Paula': 'Paula Drive', 
            'Lee': 'Lee Road', 
            'Cedar': 'Cedar Road', 
            'Lorain': 'Lorain Road', 
            'Mayfield': 'Mayfield Road', 
            'Fleet': 'Fleet Avenue', 
            '14': 'State Route 14', 
            'Rauscher': 'Rauscher Court', 
            'St. Clair': '', 
            'South Arlington': 'South Arlington Street',
            'Cleve E Liverpool Road': 'Cleveland East Liverpool Road'}
            
city = {'21010 Center Ridge Road': 'Rockport',
        '21029 Center Ridge Road': 'Rockport',
        '55 Public Square': 'Cleveland',
        '20770 Hilliard Blvd.': 'Rocky River',
        '21014 Hilliard Blvd.': 'Rocky River'}

def is_street_name(elem):
    return (elem == 'addr:street')
    
def is_postal_code(elem):
    return (elem == 'addr:postcode')
    
def is_city(elem):
    return (elem == 'addr:city')
    
def update_name(name, map=mapping, odd=oddities):
    # function to update street names based on the 'mapping' dict, which 
    # has already been created based on a previous audit of the data file

    # this section takes care of the oddities found in street names that 
    # I manually looked up for the correct street type    
    if name in odd.keys():
        new_name = odd[name]
        return new_name
    
    # this section takes care of all other abbreviations found in street names        
    name_lst = name.split()
    for i,nm in enumerate(name_lst):
        if nm in map.keys():
            name_lst[i] = map[nm]
            # the next two lines are a manual hack so that Paul E. Brown Dr SE
            # does not become Paul East Brown Drive Southeast
            if nm == 'E.' and name_lst[0] == 'Paul':
                name_lst[i] = 'E.'

    new_name = " ".join(name_lst)

    #if name != new_name:
    #    print "before ", name
    #    print "after  ", new_name
    #    print
    
    return new_name



def shape_element(element):
    node = {}
    i = 0
    if element.tag == "node" or element.tag == "way" :
        refs = []
        for tag in element.iter():
#            print tag.tag
            created = {}
            pos = []
#            refs = []
            addr = {}
            for k,v in tag.attrib.iteritems():
#                print k,v
                node['type'] = element.tag
                if problemchars.search(k):
                    break
                elif colon_colon.search(k):
                    break
                elif k in CREATED:
                    created[k] = v
                elif (k=='lat') or (k=='lon'):
                    pos.append(float(v))
                    node['pos'] = pos[::-1] #.reverse() 
                elif k == 'ref':
                    refs.append(v)
                    node['node_refs'] = refs
                elif (k=='k'): 
                    key = v
                    node[key] = ''
                elif (k=='v'):
                    value = v
                    node[key] = value
                else:
                    node[k] = v
            if created: 
                node['created'] = created
            if addr:
                node['address'] = addr
        to_remove = []
        for item in node:
            if colon_colon.search(item):
                to_remove.append(item)
        if to_remove:
            for term in to_remove:
                del node[term]
        addr_remove = []
        for item in node:
            if address.search(item):
                # fix postal codes
                # if numeric just keep first 5 digits
                # if alpha just replace with ''
                if is_postal_code(item):
                    if node[item].isalpha():
                        addr[item[5:]] = ''
                    else:    
                        addr[item[5:]] = node[item][0:5]
                # fix city names for those
                #   1. having address in city name and no city
                #   2. mispellings in city name, eg. 'heighst' instead of 'heights'
                #   3. city names including state, eg. 'Cleveland, OH' instead of 'Cleveland'
                elif is_city(item):
                    if node[item] in city.keys():
                        addr[item[5:]] = city[ node[item] ]
                        address_lst = node[item].split()
                        addr['housenumber'] = address_lst[0]
                        streetname = " ".join(address_lst[1:])
                        addr['street'] = update_name(streetname)
                    elif node[item] == 'OH':
                        addr[item[5:]] = "Newton Falls"
                    else:
                        addr[item[5:]] = node[item].replace(', Ohio', '')
                        addr[item[5:]] = node[item].replace(', OH', '')
                        addr[item[5:]] = node[item].replace(' OH', '')
                        addr[item[5:]] = node[item].replace('Hts.', 'Heights')
                        addr[item[5:]] = node[item].replace('Heighst', 'Heights')
                # fix street names based on 'mapping' and 'oddities' dicts
                elif is_street_name(item):
                    addr[item[5:]] = update_name(node[item])
                else:
                    addr[item[5:]] = node[item]
                addr_remove.append(item)
        if addr_remove:
            for term in addr_remove:
                del node[term]
        if addr:
            node['address'] = addr
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def test():
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
    filename = 'c://users//bonnie//desktop//mark_work//nanodegree//data_wrangling//project_2//cleveland.osm'
    data = process_map(filename, False)
    #pprint.pprint(data)
    
#test()

if __name__ == "__main__":
    test()