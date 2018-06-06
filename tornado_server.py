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
import tornado.websocket


lab_db = db.LabDB().db  # mongodb


def save_file(document_dir, document):
    bin_file = codecs.open(os.path.abspath('.') + "\\" + document_dir
                           + "\\" + document["name"], "w+", "utf-8")
    bin_file.write(document["content"])
    bin_file.close()


def make_file(document_dir, name):
    bin_file = codecs.open(os.path.abspath('.') + "\\" + document_dir
                           + "\\" + name, "r", "utf-8")
    temp = bin_file.read()
    bin_file.close()
    return temp


class RemoteLab(object):
    callbacks = []


'''Http'''


class LoginHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def post(self):
        account = self.get_argument("account")
        password = self.get_argument("password")
        account_set = lab_db.login_check(account, password)
        if account_set is None:
            self.write(jsonb.dumps({"code": 201, "message": "Login error!",
                                    "data": None}))
        else:
            self.write(jsonb.dumps({"code": 200, "message": "Login successful!",
                                    "data": account_set}))


class OperateHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        account = self.get_argument("account")
        token = self.get_argument("token")
        if lab_db.token_check(account, token):
            kind = self.get_argument("kind")
            if kind == "slaves":
                self.write(jsonb.dumps({"code": 200,
                                        "message": "Get slaves data successful!",
                                        "data": lab_db.slaves_get()}))
            elif kind == "staff_log":
                data = lab_db.log_get_staff(self.get_argument("staff_id"))
                if data is None:
                    self.write(jsonb.dumps({"code": 202,
                                            "message": "No such staff data!",
                                            "data": data}))
                else:
                    self.write(jsonb.dumps({"code": 200,
                                            "message": "Get staff_log data successful!",
                                            "data": data}))
            elif kind == "slave_log":
                data = lab_db.log_get_slave(self.get_argument("slave_id"))
                if data is None:
                    self.write(jsonb.dumps({"code": 202,
                                            "message": "No such device data!",
                                            "data": data}))
                else:
                    self.write(jsonb.dumps({"code": 200,
                                            "message": "Get device_log data successful!",
                                            "data": data}))
            elif kind == "all_log":
                data = lab_db.log_get_all()
                if data is None:
                    self.write(jsonb.dumps({"code": 202,
                                            "message": "No log data!",
                                            "data": data}))
                else:
                    self.write(jsonb.dumps({"code": 200,
                                            "message": "Get all_log data successful!",
                                            "data": data}))
            else:
                self.set_status(400)
        else:
            self.write(jsonb.dumps({"code": 201, "message": "Token error",
                                    "data": None}))

    def post(self):
        account = self.get_argument("account")
        token = self.get_argument("token")
        if lab_db.token_check(account, token):
            action = self.get_argument("action")
            if action == "modify":
                password = self.get_argument("password")
                lab_db.modify_password(account, password)
        else:
            self.write(jsonb.dumps({"code": 201, "message": "Token error",
                                    "data": None}))


'''WebSocket'''


class LabHandler(tornado.websocket.WebSocketHandler):
    def data_received(self, chunk):
        pass

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
            (r'/operate', OperateHandler)
            (r'/ws', LabHandler)
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
