import pymongo
from bson import json_util as jsonb

'''生成设备默认数据库'''
client=pymongo.MongoClient()
db=client.hducloud.slaves

db.drop()
db.insert([{"name":"树莓派_1","id":1,"kind":"RaspberryPi","experiments":[{"name":"温度实验"}],"user_experiment":None, "state":"free"},
           {"name":"CC3200_1","id":2,"kind":"CC3200","experiments": [{"name": "温度实验"}], "user_experiment": None, "state": "free"},
           {"name":"Arduino_1","id":3,"kind":"CC3200","experiments":[{"name":"温度实验"}], "user_experiment": None,"state":"free"},
           {"name":"STM32_1","id":4,"kind":"STM32","experiments":[{"name":"温度实验"}], "user_experiment": None,"state":"free"}
          ])

print(jsonb.dumps(db.find()))



