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
from MongoDB import db
from Update import RaspberryPi
import codecs
import tornado.webscoket


lab_db=db.LabDB().db

class RemoteLab(object):
    callbacks = []


class WelcomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class LoginHandler(tornado.web.RequestHandler):
    def post(self):
        account= self.get_argument("account")
        password = self.get_argument("password")
        token=lab_db.login_confirm(account,password)
        if token is None:
            self.write(jsonb.dumps({"code": 201, "message": "Login failed!"}))
        else:
            self.write(jsonb.dumps({"code": 200, "message": token}))

class OperateHandler(tornado.web.RequestHandler):
    def post(self):
        elif action=="modify":
            lab_db.moify_pwd(account,password)
            self.write(jsonb.dumps({"code": 200, "message": "Modify successful!"}))
        else:
            self.set_status(400)


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
            (r'/',WelcomeHandler)
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
