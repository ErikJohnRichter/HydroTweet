#### this is my closest to getting words per area so far!!!
import pymongo

try:
	conn=pymongo.MongoClient()
	print "Established Connection"
except pymongo.errors.ConnectionFailure:
	print "Connection Failed, Womp Womp..."

db = conn.tweets #ok
items = db.tweets.find() #ok
words = items.text.split(' ') #? what is tweet in this case #should be items.text.split(' ')


def wordsByArea(items):

	areas={} # dictionary where words and crap go
	for words in items(): #Do you mean items? YES pulls and iterates through each tweet
		try:
			if len(words) <= 3: #you are looping through each word already no need to check if in item
				continue
			location = words["here"]["name of here"]
			if location in areas:
				areas[location]+=1 #increases word cound
			else:
				areas[location]=1
		except:
			pass
	return areas #returns areas to dictionary
	#### everything above should work right	
		
			#item.remove(word) #why remove word?
			#print "Item Removed"
		#else:
		#	words.append(word) and words.count(word) #not sure if this works o.o

print words
print words.count
		
###this stuff is a maybe/example

def tweetsPerArea(tweets):
	areas={}
	for tweet in tweets.find():					#pulls tweets and iterates through each tweet
		try:
			location = tweet["place"]['name']	#gets location from tweet dict
			if location in areas:
				areas[location]+=1				#increases location count
			else:
				areas[location]=1				#adds location key
		except:
			pass
	return areas

#below lines are to test if the function does what it is supposed to	
#areas = tweetsPerArea(tweets)	
#for location in areas:
#	print areas[location],location