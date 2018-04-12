#!/usr/bin/env python
#coding:utf-8

import asyncio
import websockets
import pymongo
import json
import time
import modbushandle

'''信息代码表'''
message_table={
    "100":"一切正常",
    "101":"路径错误",
    "102":"账户不存在",
    "103":"账户与密码不匹配，请检查账户和密码",
    "104":"密码成功修改为："
}

'''记录时间戳到用户db'''
def db_log(id, data):
    logTime=time.asctime( time.localtime(time.time()) )
    db[id].insert_one({"time":logTime,"data":data})

'''账户校验'''
def check_account(mode, id, pwd):
    account_set=(account.find_one({"id":id}))
    if account_set==None:
        data={"code":"102","mes":{"message":message_table["102"]}}
    else:
        log_id = str(account_set["_id"])
        if mode=="login":
            if account_set["password"]!=pwd:
                data={"code":"103","mes":{"message":message_table["103"]}}
            else:
                data={"code":"100","mes":{"log_id":str(account_set["_id"]),"id":account_set["id"],
                                          "password":account_set["password"],"name":account_set["name"],
                                          "role":account_set["role"]}}
                db_log(log_id, {"mode":mode})
        elif mode=="modify":
            account.update_one({"id":id},{"$set":{"password":pwd}})
            data={"code":"104","mes":{"message":message_table["104"]+str(pwd)}}
            db_log(log_id, {"mode:":mode, "new_password":pwd})
    return data

'''modbus操作'''
def operate_modbus(mode, log_id, device, modbus):
    modbus_res=modbushandle.Master(device, modbus["function_id"], modbus["starting_address"], modbus["quantity_x"], modbus["output_value"])
    data={"code":100,"mes":{"modbus_res":modbus_res}}
    db_log(log_id, {"mode":mode, "modbus":modbus, "modbus_res":modbus_res})
    return data

async def Server(websocket, path):
    mode=(path.split("="))[1]
    if mode=="login":
        id_pwd=json.loads(await websocket.recv())
        print("-------------------id_pwd---------------")
        print(id_pwd)
        id=id_pwd["id"]
        pwd=id_pwd["password"]

        print("-------------------data------------")
        data=check_account(mode, id, pwd)
        print(data)
        await websocket.send(json.dumps(data,ensure_ascii=False))

    elif mode=="modify":
        id_newpwd=json.loads(await websocket.recv())
        id=id_newpwd["id"]
        newpwd=id_newpwd["new_password"]

        data=check_account(mode, id, newpwd)
        await websocket.send(json.dumps(data, ensure_ascii=False))

    elif mode=="operate":
        log_device_modbus = json.loads(await websocket.recv())
        log_id=log_device_modbus["log_id"]
        device=log_device_modbus["device"]
        modbus=log_device_modbus["modbus"]

        data=operate_modbus(mode, log_id, device, modbus)
        await websocket.send(json.dumps(data, ensure_ascii=False))
    elif mode=="update":
        pass
    else:
        response=json.dumps({"code":101,"data":message_table[101]})
        await websocket.send(response)


if  __name__=="__main__":

    client = pymongo.MongoClient()
    db = client.hducloud
    account = db.account

    wsServer = websockets.serve(Server, 'localhost', 80)
    asyncio.get_event_loop().run_until_complete(wsServer)
    asyncio.get_event_loop().run_forever()