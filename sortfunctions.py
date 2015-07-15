import pymongo
import pygal
from Rect import *
from Point import *
import time as time_ #make sure we don't override time

def millis():
    return int(round(time_.time() * 1000))
	
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
	
def countByWord(items):
	area = {}
	filter = {"the", "and", "i'm", "that", "for", "you", "have", "with", "just", "this", "like", "your", "not", "but", "was", "are", "get", "out", "&amp;", "all", "when", "from", "about", "don't", "it's", "what"}
	for item in items:
		text = item['text']
		place = getArea(item)
		if place != None:
			if place in area:
				a = area[place]
				for word in text.split(" "):
					word = word.replace('.', '').lower()
					if len(word) > 3 and not word.startswith('\\') and not word.startswith('$') and not word in filter:
						if word in a:
							a[word] += 1
						else:
							a[word] = 1
			else:
				area[place] = {}
				a = area[place]
				for word in text.split(" "):
					word = word.replace('.', '').lower()
					if len(word) > 3 and not word.startswith('\\') and not word.startswith('$') and not word in filter:
						if word in a:
							a[word] += 1
						else:
							a[word] = 1
	return area
	
def countByName(items):
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
	
def countByHash(items):
	area = {}
	for item in items:
		for hashs in item['entities']['hashtags']:
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
	
def countByArea(items):
	area = {}
	for item in items:
		place = getArea(item)
		if place != None:
			if place in area:
				area[place] += 1
			else:
				area[place] = 1	
	return area
	

def saveHash():
	conn = pymongo.MongoClient()
	db = conn.tweets
	items = db.tweets.find()
	areas = countByHash(items)
	db.byhash.save(areas)	
	print "Hash data saved."

def saveName():
	conn = pymongo.MongoClient()
	db = conn.tweets
	items = db.tweets.find()
	areas = countByName(items)
	db.byname.save(areas)
	print "Name data saved."

def saveArea():
	conn = pymongo.MongoClient()
	db = conn.tweets
	items = db.tweets.find()
	areas = countByArea(items)
	db.byarea.save(areas)
	print "Area data saved."
	

def saveWord():
	conn = pymongo.MongoClient()
	db = conn.tweets
	items = db.tweets.find()
	areas = countByWord(items)
	db.byword.save(areas)
	print "Word data saved."
	
def drop():
	conn = pymongo.MongoClient()
	db = conn.tweets
	db.drop_collection('byhash')
	db.drop_collection('byword')
	db.drop_collection('byarea')
	db.drop_collection('byname')
	print "Databases dropped."
	

def sortCountArea(base):
	for area in base.find():
		return sorted(area.iteritems(), key=lambda (k,v): (v,k), reverse = True)
	
def sort(base):
	new = {}
	for area in base.find():
		for item in area:
			if item != '_id':
				for i in area[item]:
					if i in new:
						new[i] += area[item][i]
					else:
						new[i] = area[item][i]
	return sorted(new.iteritems(), key=lambda (k,v): (v,k), reverse = True)
def sortArea(base):
	new = {}
	for area in base.find():
		for item in area:
			if item != '_id':
				new[item] = sorted(area[item].iteritems(), key=lambda (k,v): (v,k), reverse = True)
	return new
	
def allHashGraph():
	conn = pymongo.MongoClient()
	db = conn.tweets
	s = sort(db.byhash)
	pie_chart = pygal.Pie()
	pie_chart.title = 'Top 10 Hash Tags Overall'
	count = 0
	for hash in s:
		pie_chart.add(hash[0] + " - " + str(hash[1]), hash[1])
		count += 1
		if count == 10:
			break
	pie_chart.render_to_file('total_hash_pie_chart.svg')  
	
def allWordGraph():
	conn = pymongo.MongoClient()
	db = conn.tweets
	s = sort(db.byword)
	pie_chart = pygal.Pie()
	pie_chart.title = 'Top 10 Words Overall'
	count = 0
	for hash in s:
		pie_chart.add(hash[0] + " - " + str(hash[1]), hash[1])
		count += 1
		if count == 10:
			break
	pie_chart.render_to_file('total_word_pie_chart.svg')  
	
def allNameGraph():
	conn = pymongo.MongoClient()
	db = conn.tweets
	s = sort(db.byname)
	pie_chart = pygal.Pie()
	pie_chart.title = 'Top 10 Tweeters Overall'
	count = 0
	for hash in s:
		pie_chart.add(hash[0] + " - " + str(hash[1]), hash[1])
		count += 1
		if count == 10:
			break
	pie_chart.render_to_file('total_name_pie_chart.svg')  
	
def hashGraph():
	conn = pymongo.MongoClient()
	db = conn.tweets
	s = sortArea(db.byhash)
	for area in s:
		pie_chart = pygal.Pie()
		pie_chart.title = 'Top 10 Hash Tags in ' + area
		count = 0
		for hash in s[area]:
			pie_chart.add(hash[0] + " - " + str(hash[1]), hash[1])
			count += 1
			if count == 10:
				break
		pie_chart.render_to_file(area + '_hash_pie_chart.svg')  
		
def nameGraph():
	conn = pymongo.MongoClient()
	db = conn.tweets
	s = sortArea(db.byname)
	for area in s:
		pie_chart = pygal.Pie()
		pie_chart.title = 'Top 10 Tweeters in ' + area
		count = 0
		for name in s[area]:
			pie_chart.add(name[0] + " - " + str(name[1]), name[1])
			count += 1
			if count == 10:
				break
		pie_chart.render_to_file(area + '_name_pie_chart.svg')  
		
def areaGraph():
	conn = pymongo.MongoClient()
	db = conn.tweets
	s = sortCountArea(db.byarea)
	pie_chart = pygal.Pie()
	pie_chart.title = 'Tweet Count By Area'
	for area in s:
		if (area[0] != '_id'):
			pie_chart.add(area[0] + " - " + str(area[1]), area[1])
	pie_chart.render_to_file('count_area_pie_chart.svg')  	
	
def wordGraph():
	conn = pymongo.MongoClient()
	db = conn.tweets
	s = sortArea(db.byword)
	for area in s:
		pie_chart = pygal.Pie()
		pie_chart.title = 'Top 10 Words Used in ' + area
		count = 0
		for word in s[area]:
			pie_chart.add(word[0] + " - " + str(word[1]), word[1])
			count += 1
			if count == 10:
				break
		pie_chart.render_to_file(area + '_word_pie_chart.svg')  
		
type = int(raw_input("- Calculate Counts - \n1. Name\n2. Area\n3. Hash\n4. Word\n5. Drop\n6. Drop Save All\n\n- Sort Data -\n7. Sort Hash\n8. Sort Name\n9. Sort Area\n10. Sort Words\n11. Sort All\n> "))

if type == 1:
	saveName()
elif type == 2:
	saveArea()
elif type == 3:
	saveHash()
elif type == 4:
	saveWord()
elif type == 5:
	drop()
elif type == 6:
	drop()
	saveName()
	saveArea()
	saveHash()
	saveWord()
elif type == 7:	
	hashGraph()
elif type == 8:
	nameGraph()	
elif type == 9:
	areaGraph()
elif type == 10:
	wordGraph()
elif type == 11:
	hashGraph()
	nameGraph()
	areaGraph()
	wordGraph()
elif type == 12:
	conn = pymongo.MongoClient()
	db = conn.tweets
	allHashGraph()
	allNameGraph()
	allWordGraph()