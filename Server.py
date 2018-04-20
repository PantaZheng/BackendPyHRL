#!/usr/bin/env python
#coding:utf-8

import os
import asyncio
import websockets
import pymongo
import time
from bson import json_util as jsonb
import modbushandle as md
import raspiberry
import codecs

'''登录操作'''


def check_account(message):
    id = message["id"]
    password = message["password"]
    account_set = account.find_one({"id": id})
    if account_set == None:
        data = {"code": "101", "mes": "账户登录：错误，不存在账户", "data": None}
    else:
        account_set.pop("_id")
        if account_set["password"] != password:
            data = {"code": "102", "mes": "账户登录：错误，密码与账号不符", "data": None}
        else:
            data = {"code": "100", "mes": "账户登录：成功", "data": account_set}
    print("message:" + str(message) + "data:" + str(data))
    return data


'''改密操作'''


def modify_password(message):
    id = message["id"]
    password = message["password"]
    account.update({"id": id}, {"$set": {"password": password}})
    data = {"code": "200", "mes": "密码修改：成功", "data": None}
    print("message:" + str(message) + "data:" + str(data))
    return data


'''获取信息'''


def get_info(message):
    flag = message["flag"]
    if flag == "slaves":
        temp=list(db.slaves.find())
        for i in temp: i.pop("_id")
        data = {"code": "300", "mes": "获取信息：slaves，成功", "data":temp }
    elif flag == "log":
        id = message["id"]
        temp = list(db[id]["log"].find().sort("time", pymongo.DESCENDING).limit(10))
        for i in temp:
            t = i["time"]
            i["time"] = time.asctime(t)
            i.pop("_id")
        data = {"code": "301", "mes": "获取信息：log，成功", "data": temp}
    else:
        data = {"code": "302", "mes": "获取信息：标识错误！", "data": None}
    print("message:" + str(message) + "data:" + str(data))
    return data


def save_file(dir, docement):
    bin_file = codecs.open(os.path.abspath('.') + "\\" + dir + "\\" + docement["name"], "w+", "utf-8")
    bin_file.write(docement["content"])
    bin_file.close()


def make_file(dir, name):
    bin_file = codecs.open(os.path.abspath('.') + "\\" + dir + "\\" + name, "r","utf-8")
    temp = bin_file.read()
    bin_file.close()
    return temp


'''操作记录日志'''


def db_log(id, data):
    db[id].insert_one({"time": time.time(), "data": str(data)})


'''设备操作：对于设备相关，需要在此修改'''


def operate(message):
    flag = message["flag"]
    id = message["id"]
    slave = message["slave"]
    data={}
    if flag == "upload":
        save_file(slave["kind"],message["docement"])
        data = {"code": "400", "mes": "上传文件："+slave["name"]+",成功", "data": None}
    elif flag == "download":
        experiment = message["experiment"]
        slave_kind = message["slave"]["kind"]
        data = {"code": "401", "mes": "文件下载在D:\\"+experiment, "data": make_file(slave_kind, experiment)}
    elif flag == "start":
        experiment = message["experiment"]
        slave_kind = message["slave"]["kind"]
        slave_id = message["slave"]["id"]
        slave_state = message["slave"]["state"]
        ip = md.device_host[slave_id]
        db.slaves.update({"id": slave_id}, {"$set": {"state": slave_state}})
        if slave_kind == "RaspberryPi":
            data = {"code": "402", "mes": raspiberry.transport(ip, experiment),
                    "data": None}
        elif slave_kind == "CC3200":
            data = {"code": "402", "mes": "", "data": None}
        elif slave_kind == "Arduino":
            data = {"code": "402", "mes":"", "data": None}
        elif slave_kind == "STM32":
            data = {"code": "402", "mes":"" , "data": None}
    elif flag == "modbus":
        modbus_mes = message["modbus"]
        res = md.Master(message["slave"]["id"], modbus_mes["function_code"], modbus_mes["starting_address"],
                        modbus_mes["quantity_of_x"], )
        data = {"code": "403", "mes": "Modbus指令执行结果：" + str(res), "data": None}
    elif flag == "stop":
        slave_kind = message["slave"]["kind"]
        slave_id = message["slave"]["id"]
        slave_state = message["slave"]["state"]
        ip = md.device_host[slave_id]
        db.slaves.update({"id": slave_id}, {"$set": {"state": slave_state}})
        if slave_kind == "RaspberryPi":
            data = {"code": "404", "mes":  raspiberry.stop(ip),
                    "data": None}
        elif slave_kind == "CC3200":
            data = {"code": "404", "mes":"", "data": None}
        elif slave_kind == "Arduino":
            data = {"code": "404", "mes": "", "data": None}
        elif slave_kind == "STM32":
            data = {"code": "404", "mes": "", "data": None}
    print("message:" + str(message) + "data:" + str(data))
    db_log(id, {"message": message, "data": data})
    return data


async def Server(websocket, path):
    mode = (path.split("="))[1]
    if mode == "login":
        data = check_account(jsonb.loads(await websocket.recv()))
    elif mode == "modify":
        data = modify_password(jsonb.loads(await websocket.recv()))
    elif mode == "info":
        data = get_info(jsonb.loads(await websocket.recv()))
    elif mode == "operate":
        data = operate(jsonb.loads(await websocket.recv()))
    else:
        data = {"code": "001", "mes": "路径错误", "data": None}
    await websocket.send(jsonb.dumps(data, ensure_ascii=False))


if __name__ == "__main__":
    client = pymongo.MongoClient()
    db = client.hducloud
    account = db.account

    wsServer = websockets.serve(Server, 'localhost', 80)
    asyncio.get_event_loop().run_until_complete(wsServer)
    asyncio.get_event_loop().run_forever()
