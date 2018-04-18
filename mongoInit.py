import pymongo
from bson import json_util as jsonb

'''生成设备默认数据库'''
client=pymongo.MongoClient()
db=client.hducloud
db["5a98fcb8a970a13064ccff46"].drop()

print(db.collection_names())


