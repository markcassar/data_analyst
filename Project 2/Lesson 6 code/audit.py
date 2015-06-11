"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "example.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

# a list of non-abbreviated street types that we would expect to see 
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

# a dict of abbreviated street types found in our data audit and the 
# non-abbreviated street type that we would like to replace it with 
mapping = { "St": "Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Rd.": "Road"
            }


def audit_street_type(street_types, street_name):
    # function that uses a regular expression to check if 'street_name' is 
    # in the 'expected' list of street types; if it is not, 'street_name' is
    # added to the 'street_types' dict
    # for example, if 'street_name = John St.', this function will check if 'St.'
    # is in the list 'expected'. If it is not, then it will create a new entry
    # in the 'street_types' dict, with the key being 'St.' and the value being
    # 'John St.'
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    # function to check if the 'k' attribute of the xml tag
    # is identified as the street address
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    # function to run through all the 'node' and 'way' tags of an open street map xml file
    # and generate a dict of all the street types that are not expected (as defined by 
    # the list 'expected')
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    return street_types


def update_name(name, mapping):
    # function to update street names based on the 'mapping' dict, which 
    # has already been created based on a previous audit of the data file
    i = 0
    for k,v in mapping.iteritems():
        if k in name and (i==0): 
            name = name.replace(k, v)
            i += 1

    return name


def test():
    st_types = audit(OSMFILE)
    assert len(st_types) == 3
    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name
            if name == "West Lexington St.":
                assert better_name == "West Lexington Street"
            if name == "Baldwin Rd.":
                assert better_name == "Baldwin Road"


if __name__ == '__main__':
    test()