import pymongo
from bson import json_util as jsonb

'''生成设备默认数据库'''
client=pymongo.MongoClient()
db=client.hducloud

db.slaves.drop()

db.slaves.insert([{"id":1,"kind":"RaspberryPi","name":"树莓派_1","experiments":[{"name":"temperature.py"},{"name":"distance.py"},{"name":"helloworld.py"},{"name":"hc-sr04_ultrasonic_sensor.py"}],"state":"free"},
                  {"id":2,"kind":"CC3200","name":"CC3200_1","experiments":[{"name":"temperature.py"},{"name":"distance.py"}],"state":"free"},
                  {"id":3,"kind":"STM32","name":"STM32_1","experiments":[{"name":"temperature.py"},{"name":"distance.py"}],"state":"free"},
                  {"id":4,"kind":"Arduino","name":"Arduino_1","experiments":[{"name":"temperature.py"},{"name":"distance.py"}],"state":"free"},
                  ])



print(list(db.slaves.find()))