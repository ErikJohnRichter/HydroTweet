import pymongo
from Rect import *
from Point import *
import time as time_ #make sure we don't override time

def millis():
    return int(round(time_.time() * 1000))
	
conn = pymongo.MongoClient()
db = conn.tweets
items = db.tweets.find()

def getArea(tweet):
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

def tweetCount():
	db.tweets.count()
	
def countByWord():
	area = {}
	for item in items:
		text = item['text']
		place = getArea(item)
		if place != None:
			if place in area:
				a = area[place]
				for word in text.split(" "):
					word = word.replace('.', '').lower()
					if len(word) >= 3 and not word.startswith('\\') and not word.startswith('$'):
						if word in a:
							a[word] += 1
						else:
							a[word] = 1
			else:
				area[place] = {}
				a = area[place]
				for word in text.split(" "):
					word = word.replace('.', '').lower()
					if len(word) >= 3 and not word.startswith('\\') and not word.startswith('$'):
						if word in a:
							a[word] += 1
						else:
							a[word] = 1
	return area
	
def countByName():
	area = {}
	for item in items:
		user = item['user']['screen_name']
		place = getArea(item)
		if place != None:
			if place in area:
				a = area[place]
				if user in a:
					a[user] += 1
				else:
					a[user] = 1
			else:
				area[place] = {user : 1}			
	return area
	
def countByHash():
	area = {}
	for item in items:
		for hashs in item['entities']['hashtags']:
			#print hashs['text']
			place = getArea(item)
			if place != None:
				if place in area:
					a = area[place]
					if hashs['text'] in a:
						a[hashs['text']] += 1
					else:
						a[hashs['text']] = 1
				else:
					area[place] = {hashs['text'] : 1}			
	return area
	
def countByArea():
	area = {}
	for item in items:
		delta = getArea(item)
		print item[text]
	#loop through all posts, get city from post- if city doesn't exist in dictionary, add it
		#loop through words in post

	if(word in area[city][words]):
		area[city][words] += 1
	else:
		area[city][words]=1
#each area key is a city, value being a new dictionary
#the dictionary contains word as the key, and count as the value





	for item in items:
		place = getArea(item)
		if place != None:
			print place
			if place in area:
				area[place] += 1
			else:
				area[place] = 1	
	return area
	
startTime = millis()
print tweetCount()


def saveHash():
	conn = pymongo.MongoClient()
	db = conn.tweets
	items = db.tweets.find()
	areas = countByHash()
	db.byhash.save(areas)		

def saveName():
	conn = pymongo.MongoClient()
	db = conn.tweets
	items = db.tweets.find()
	areas = countByName()
	db.byname.save(areas)

def saveArea():
	conn = pymongo.MongoClient()
	db = conn.tweets
	items = db.tweets.find()
	areas = countByArea()
	db.byarea.save(areas)
	

def saveWord():
	conn = pymongo.MongoClient()
	db = conn.tweets
	items = db.tweets.find()
	areas = countByWord()
	db.byword.save(areas)

saveHash()
#saveName()
#saveArea()
#saveWord()

endTime = millis()

print "Start: ", startTime, " End: ", endTime, " time: ", (endTime - startTime)
		
