#!/usr/bin/env python
# coding:utf-8

import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import tornado.options
from uuid import uuid4
from MongoDB import  db

import os
import asyncio
import websockets
import pymongo
import time
from bson import json_util as jsonb
from MongoDB import mongodb
from Update import RaspberryPi
import codecs
import tornado.webscoket


lab_db=db.LabDB().db#mongodb


def save_file(document_dir, document):
    bin_file = codecs.open(os.path.abspath('.') + "\\" + document_dir + "\\" + document["name"], "w+", "utf-8")
    bin_file.write(document["content"])
    bin_file.close()


def make_file(document_dir, name):
    bin_file = codecs.open(os.path.abspath('.') + "\\" + document_dir + "\\" + name, "r", "utf-8")
    temp = bin_file.read()
    bin_file.close()
    return temp

class RemoteLab(object):
    callbacks = []

'''Http'''
class LoginHandler(tornado.web.RequestHandler):
    def post(self):
        account= self.get_argument("account")
        password = self.get_argument("password")
        account_set=lab_db.login_check(account,password)
        if account_set is None:
            self.write(jsonb.dumps({"code": 201, "message": "Login error!","data":None}))
        else:
            self.write(jsonb.dumps({"code": 200, "message": "Login successful!",
                                    "data":account_set}))

class OperateHandler(tornado.web.RequestHandler):
    def get(self):
        account = self.get_argument("account")
        token = self.get_argument("token")
        if lab_db.token_check(account, token):
            kind = self.get_argument("kind")
            if kind=="experiment":
                #db提供查询
            elif kind=="log":
                #db提供查询，前端传过去审查role
        else:
            self.write(jsonb.dumps({"code": 201, "message": "Token error",
                                    "data": None}))



    def post(self):
        account = self.get_argument("account")
        token = self.get_argument("token")
        if lab_db.token_check(account,token):
            action = self.get_argument("action")
            id action=="modify":

        else:
            self.write(jsonb.dumps({"code": 201, "message": "Token error",
                                    "data": None}))


'''WebSocket'''

class LabHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.application.shoppingCart.register(self.callback)

    def on_close(self):
        self.application.shoppingCart.unregister(self.callback)

    def on_message(self, message):
        pass

    def callback(self, count):
        self.write_message('{"inventoryCount":"%d"}' % count)


class Application(tornado.web.Application):
    def __init__(self):
        self.remote_lab = RemoteLab()


        handlers = [
            (r'/login', LoginHandler),
            (r'/operate',OperateHandler)
            (r'/download',LoadHandler)
            (r'/ws',LabHandler)
        ]

        settings = {
            'template_path': 'templates',
            'static_path': 'static'
        }

        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    tornado.options.parse_command_line()

    app = Application()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
