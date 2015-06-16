import json
import pymongo

#def insert_data(data, db):
#
#    # Your code here. Insert the data into a collection 'arachnid'
#    db.cleveland.insert(data)

#    pass


if __name__ == "__main__":
    
    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017")
    db = client.cities

    with open('cleveland.osm.json') as f:
        for line in f:
            db.cleveland.insert(json.loads(line))
