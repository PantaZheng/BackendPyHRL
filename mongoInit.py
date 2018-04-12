import pymongo
import csv
client=pymongo.MongoClient()
db=client.hducloud
account= db["5a98fcb8a970a13064ccff46"]

print((account.find_one()))


