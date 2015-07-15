import pymongo

conn = pymongo.MongoClient()
db = conn.tweets

for area in db.byhash.find():
	for item in area:
		if item != '_id':
			print area[item]
	
for area in db.byname.find():
	for item in area:
		if item != '_id':
			print area[item]

for area in db.byword.find():
	for item in area:
		if item != '_id':
			print area[item]
	
for area in db.byarea.find():
	for item in area:
		if item != '_id':
			print area[item]
	
def drop():
	db.drop_collection('byhash')
	db.drop_collection('byword')
	db.drop_collection('byarea')
	db.drop_collection('byname')

def dropMain():
	db.drop_collection('tweets')
	
#dropMain()
#drop()