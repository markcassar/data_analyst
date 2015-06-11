#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.
"""
import xml.etree.cElementTree as ET
import pprint
import json
import codecs

filename = 'c://users//bonnie//desktop//mark_work//nanodegree//data_wrangling//project_2//Cleveland_sample.osm'


def count_tags_keys(filename):
    # This function counts the frequency of tags and keys in osm file
    # returns both tag and key counts as dictionaries
    tags = {}
    keys ={}
    tag_keys = {}
    for event, elem in ET.iterparse(filename):
        tags[elem.tag] = tags.get(elem.tag,0) + 1
        for k, v in elem.attrib.iteritems():
            keys[k] = keys.get(k,0) + 1
    
    # now count the frequency of keys (attributes) per tag
    tag_keys = { k:{} for k in tags.keys()} 
    for event, elem in ET.iterparse(filename):
        for k, v in elem.attrib.iteritems():
            tag_keys[elem.tag][k] = tag_keys[elem.tag].get(k,0) + 1
    
    return tags, keys, tag_keys  
    
def explore_tags(filename):
    nested_tags = {}
    nested_keys = []
    xml_levels = []
    level = 0
    for event, elem in ET.iterparse(filename, events=('start', 'end')):
        if elem.tag != 'osm':
            if event == 'start':
                level += 1
                nested_keys.append(elem.tag)
            elif event == 'end':
                level -= 1
                if elem.tag == nested_keys[0]:
                    nested_tags[elem.tag] = set(nested_keys[1:])
#                    nested_tags[elem.tag].append(set(nested_keys[1:]))
                    nested_keys = []
                #if len(nested_keys) == 1:
                #    nested_keys.pop()
        xml_levels.append(level) 
    return nested_tags, set(xml_levels)
    
tags, keys, tag_keys = count_tags_keys(filename)
print " Tags found in file"
print
pprint.pprint(tags)
print 
print
print "Keys found within tags in file"
print
pprint.pprint(keys)
print
print
print "Keys associated with specific tags"
print
pprint.pprint(tag_keys)

nested_tags, xml_levels = explore_tags(filename)

for k,v in nested_tags.iteritems():
    nested_tags[k] = list(v)

print 
print
print "Tag structure of file"
print
pprint.pprint(nested_tags)

print
print "xml levels in file"
print list(xml_levels)

file_out = "{0}.json".format(filename)

with codecs.open(file_out, 'w') as fo: 
    fo.write("Tags found in "+filename+"\n")
    fo.write(json.dumps(tags, indent=2)+"\n") 
    fo.write("Keys found inside the tags in "+filename+"\n")
    fo.write(json.dumps(keys, indent=2)+"\n") 
    fo.write("Keys associated with the tags found in "+filename+"\n")
    fo.write(json.dumps(tag_keys, indent=2)+"\n")
    fo.write("Tag structure found in "+filename+"\n")
    fo.write(json.dumps(nested_tags, indent=2)+"\n") 
 



#
#if __name__ == "__main__":
#    test()