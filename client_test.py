#!/usr/bin/env python
#coding:utf-8

import os
import sys
import asyncio
import websockets
import json
import codecs

async def to_server(mode, data):
    async with websockets.connect('ws://localhost:80/mode='+ mode) as websocket:
        print('------------------->')
        await websocket.send(data)
        a=await websocket.recv()
        print(a)

if  __name__=="__main__":
    id='14051238'
    password='14051238'
    log_id="5a98fcb8a970a13064ccff4"
    data=json.dumps({"id":id,"password":password})
    operate='operate'
    asyncio.get_event_loop().run_until_complete(to_server(operate,data))