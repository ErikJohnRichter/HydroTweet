#### this is my closest to getting words per area so far!!!
import pymongo
from Rect import *
from Point import *

try:
	conn=pymongo.MongoClient()
	print "Established Connection"
except pymongo.errors.ConnectionFailure:
	print "Connection Failed, Womp Womp..."

db = conn.tweets #ok
items = db.tweets.find() #ok

def getArea(tweet):# just gets all the areas
	sf = Rect(Point(-122.75,36.8), Point(-121.75,37.8))
	ny = Rect(Point(-74,40), Point(-73,41))
	ch = Rect(Point(-89,41), Point(-88,42))
	la = Rect(Point(-119,33), Point(-117,34.5))
	 
	if tweet['place'] != None:
		box = tweet['place']['bounding_box']
		coord = box['coordinates']
		loc = Rect(Point(coord[0][0][0], coord[0][0][1]), Point(coord[0][2][0], coord[0][2][1]))
		if sf.overlaps(loc):
			return "San Fran"
		if ny.overlaps(loc):
			return "New York"
		if ch.overlaps(loc):
			return "Chicago"
		if la.overlaps(loc):
			return "Los Angeles"
	return None

def wordsByArea(items):
	areas = {} # dictionary where areas go
	wordlist = {} #dictionary where words go
	for item in items: #Do you mean items? YES pulls and iterates through each tweet
		gamma = getArea(item)
		if gamma != None:
			try:
				if gamma in areas:#########around here is where im lost
					theta = areas[gamma]
					words = item["text"]#come back to this
					for word in words.split(" "):
						if len(word) >= 3 and not word.startswith('\\') and not word.startswith('$'):
							if word in theta:
	                            theta[word] += 1
	                        else:
	                            theta[word] = 1
                else:
                	areas[gamma] = {}
                	theta = areas[gamma]
					words = item["text"]#come back to this
					for word in words.split(" "):
						if len(word) >= 3 and not word.startswith('\\') and not word.startswith('$'):
							if word in theta:
	                            theta[word] += 1
	                        else:
	                            theta[word] = 1
            except:
            	print "Something biffed, try again"
    return areas #returns areas to dictionary


#### maybe this will loop through everything?
for areas in items:
	print areas, items[areas]

#loop though all items and then find where text is stored in dictionary 
