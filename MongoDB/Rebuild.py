import pymongo
import csv
import os

client=pymongo.MongoClient()
db=client.hducloud

#定义设备类型映射表: 类型转化为数字,采用
slaves_table=[]

def all_rebuild():
    db.drop()
    db=client.hducloud
    staff   = db.staff
    slaves  = db.slaves

def staff_rebuild():
    staff = db.staff
    staff.drop()
    staff = db.staff
    csv_reader = csv.reader(open('D:\TestData\\voter-utf-8.csv', encoding='utf-8'))

def slaves_rebuild():
    dir_list = next(os.walk('Devices'))
    return dir_list
    # slaves = db.slaves
    # slaves.drop()
    # slaves=db.slaves
    # db.slaves.insert([{"id":1,"kind":"RaspberryPi","name":"树莓派_1","experiments":[{"name":"temperature.py"},{"name":"distance.py"},{"name":"helloworld.py"},{"name":"hc-sr04_ultrasonic_sensor.py"}],"state":"free"},
    #               {"id":2,"kind":"CC3200","name":"CC3200_1","experiments":[{"name":"temperature.py"},{"name":"distance.py"}],"state":"free"},
    #               {"id":3,"kind":"STM32","name":"STM32_1","experiments":[{"name":"temperature.py"},{"name":"distance.py"}],"state":"free"},
    #               {"id":4,"kind":"Arduino","name":"Arduino_1","experiments":[{"name":"temperature.py"},{"name":"distan



