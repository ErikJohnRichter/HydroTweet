
from pymongo import MongoClient
import pymongo


conn = pymongo.MongoClient()
db = conn.tweets

items = db.tweets.find()


from tester import *
conn = MongoClient()
currentTime = millis()
db = conn.tweets
sevenDays = 604800000
items = db.tweets.find()
area = {}
#print items
for tweet in items:
    tweetTimeStamp = long(tweet["timestamp_ms"])
    if (currentTime - tweetTimeStamp) < sevenDays:
        loc = getArea(tweet)
        if loc != None:
            if loc not in area:
                area[loc] = {}
            for ent in tweet["entities"]["hashtags"]:
                try:
                    #area[loc][ent["text"]] 
                    print ent["text"]
                    if ent["text"] not in area[loc]:
                        area[loc][ent["text"]] = 1
                    else:
                        area[loc][ent["text"]] += 1
                except UnicodeEncodeError:
                    print("UnicodeFail")
#print area
#print area[loc]
raw_input()
print area[loc][ent]
raw_input()

"""
masterTrends = {}
items = db.byhash.find()
for area in items:i
	#print area
	for hashT in area:
        print hashT
        for hashTags in hashT:
            print hashTags
raw_input()           
            
<<<<<<< HEAD
"""
            

