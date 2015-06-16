# -*- coding: utf-8 -*-
import pymongo

"""
Your task is to sucessfully run the exercise to see how pymongo works
and how easy it is to start using it.
You don't actually have to change anything in this exercise,
but you can change the city name in the add_city function if you like.

Your code will be run against a MongoDB instance that we have provided.
If you want to run this code locally on your machine,
you have to install MongoDB (see Instructor comments for link to installation information)
and uncomment the get_db function.
"""


def get_db():
    # For local use
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    # 'examples' here is the database name. It will be created if it does not exist.
    db = client.cities
    return db

if __name__ == "__main__":
    # For local use
    db = get_db() # uncomment this line if you want to run this locally

    # all queries below are good
    #print db.cleveland.find_one()
    #print db.cleveland.find_one({"created.user":"skorasaurus"})
    print db.cleveland.find().count()
    print db.cleveland.find( {"type":"node"} ).count()
    print db.cleveland.find( {"type":"way"} ).count()
    print len(db.cleveland.distinct( "created.user" ) )
    print db.cleveland.aggregate([{"$match": {"amenity":{"$exists":1}, "amenity":"hospital"}}, {"$group":{"_id":"$amenity", "count":{"$sum":1}}}])
    print db.cleveland.aggregate([{"$match": {"amenity":{"$exists":1}, "amenity":"hospital", "emergency":"yes"}}, {"$group":{"_id":"$amenity", "count":{"$sum":1}}}])

    # percent contributions of top 10 users
    top_10 = db.cleveland.aggregate([{"$group":{"_id":"$created.user", "count":{"$sum":1}}}, {"$sort":{"count":-1}}, {"$limit":10}])
    total = 0
    for item in top_10['result']:
        total += item['count']
        print float(total)/db.cleveland.find().count()

    #counts of amenities
    print db.cleveland.aggregate([{"$match": {"amenity":{"$exists":1}}}, {"$group":{"_id":"$amenity", "count":{"$sum":1}}}])
    
    
    #print db.cleveland.aggregate([{"$match":{"amenity":{"$exists":1}}}, {"$group":{"_id":"$amenity","count":{"$sum":1}}}, {"$sort":{"count":-1}}, {"$limit":10} ])# , {"$sort":{"count":­-1}} ]) #, {"$limit":10}])
    #print db.cleveland.aggregate([{"$group":{"_id":"$created.user", "count":{"$sum":1}}}, {"$sort":{"count":-1}}, {"$limit":10} ]) # {"$sort":{"count":­1}}, {"$limit":1}])
    #print db.cleveland.aggregate([{"$match": {"amenity":{"$exists":1}, "amenity":"restaurant"}}])
        
    