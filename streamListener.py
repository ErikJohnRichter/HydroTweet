import tweepy
import json
import pymongo
from authKeys import keys

CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']

class HidroTwitListener(tweepy.StreamListener):
	def __init__(self):
		self.conn = pymongo.MongoClient()
		self.db = self.conn.tweets
		print "Init"
		
	def insert(self, data):
		self.db.tweets.insert(data)#inserts into db
		self.db.tweets.save(data)
		
	def on_data(self, data):
		tweets = json.loads(data)
		tweetstext = ''.join(tweets['text']).encode('utf-8')
		try:
			print(tweets['user']['location'])
			print(tweets['lang'])
			print(tweetstext)
			print(tweets['entities']['hashtags'])
			print(tweets['entities']['trends'])
			
			self.insert(tweets)
		except UnicodeEncodeError:
			print('UnicodeEncodeError')
		return True
	def on_error(self, status):
		print status

if __name__ == "__main__":
    listenBot = HidroTwitListener()
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    
    stream = tweepy.Stream(auth, listenBot)
    stream.filter(locations=[-122.75,36.8,-121.75,37.8, -74,40,-73,41, -89,41,-88,42, -119,33,-117,34.5])



