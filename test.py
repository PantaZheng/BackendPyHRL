#!/usr/bin/env python

import asyncio
import websockets
import json

async def get_client(websocket,path):
    Greeting = await  websocket.recv()
    mes= json.loads(Greeting)
    print(mes)
    print(path)
    print(mes['id'])

if  __name__=="__main__":
    ws_server = websockets.serve(get_client, 'localhost', 80)
    asyncio.get_event_loop().run_until_complete(ws_server)
    asyncio.get_event_loop().run_forever()