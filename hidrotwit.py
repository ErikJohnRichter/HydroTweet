import tweepy # Import tweepy to use for the streamer
import json # Import json to use json.loads
import pymongo #Import pymongo for database connection
from authKeys import keys # import keys for auths

CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']

'''
HidroTwitListener extends tweepy.StreamListener
Used to receive tweets from twitter to the on_data function
'''
class HidroTwitListener(tweepy.StreamListener):
	# Initializes our mongodb connection and database
	def __init__(self):
		self.conn = pymongo.MongoClient()
		self.db = self.conn.tweets
		print "Init"
		
	# Inserts tweets into the mongodb
	def insert(self, data):
		self.db.tweets.insert(data)#inserts into db
		self.db.tweets.save(data)
	
	#Recieves tweets via twitter stream and inserts them into the database
	def on_data(self, data):
		tweets = json.loads(data)
		tweetstext = ''.join(tweets['text']).encode('utf-8')
		try:
			print "Location:", tweets['user']['location'], "Tweet:", tweetstext
			
			self.insert(tweets)
		except UnicodeEncodeError:
			print('UnicodeEncodeError')
		return True
		
	#Prints errors from tweets
	def on_error(self, status):
		print status

#main function
if __name__ == "__main__":
    listenBot = HidroTwitListener() #Creates a new instance of the HidroTwitListener
	
	#Tweepy auth setup
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    
	#Creates the tweepy stream utilizing our auth keys and our HidroTwitListener
    stream = tweepy.Stream(auth, listenBot)
	#Creating the stream filter based on location
    stream.filter(locations=[-122.75,36.8,-121.75,37.8, -74,40,-73,41, -89,41,-88,42, -119,33,-117,34.5])



