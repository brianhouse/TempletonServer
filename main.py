#!/usr/bin/env python3

import json
from pymongo import ASCENDING
from tornado import websocket
from housepy import server, config, log, strings
    
class Home(server.Handler):

    def get(self, page=None):
        log.info("Home.get")
        if page == "data":
            result = list(self.db.stream.find().sort([('t_utc', ASCENDING)]))
            return self.json(result)
        return self.text("data/")

    def post(self, nop=None):
        log.info("Home.post")
        try:
            data = self.request.body.decode('utf-8').split('\n')
            data = [[float(e) for e in d.split(',')] for d in data]
        except Exception as e:
            return log.error(e)
        self.db.stream.insert([{'t_utc': d[0], 'x': d[1], 'y': d[2], 'z': d[3], 'rms': d[4]} for d in data])
        log.info("OK")


class WebSocket(websocket.WebSocketHandler):

    sockets = {}

    def open(self):
        log.info("//////////// WebSocket.open")
        socket_id = strings.random_string(10)
        WebSocket.sockets[socket_id] = self
        log.info("--> new socket_id %s" % socket_id)
        WebSocket.send(socket_id, socket_id)

    def on_message(self, data):
        log.info("//////////// WebSocket.on_message %s" % data)
        try:
            data = json.loads(data)
            socket_id = data['socket_id']
        except Exception as e:
            log.error(log.exc(e))
            return
        WebSocket.send(socket_id, "OK")

    def on_close(self):
        log.info("//////////// WebSocket.on_close")
        socket_id = None
        for sid, instance in WebSocket.sockets.items():
            if instance == self:
                socket_id = sid
        log.info("--> closing socket_id %s" % socket_id)                
        if socket_id in WebSocket.sockets:
            del WebSocket.sockets[socket_id]

    @classmethod
    def send(cls, socket_id, message):
        socket = WebSocket.sockets[socket_id]
        log.info("--> sending [%s] to %s" % (message, socket_id))
        try:
            socket.write_message(message)
        except Exception as e:
            log.error(log.exc(e))


handlers = [
    (r"/websocket", WebSocket),    
    (r"/?([^/]*)", Home),
]    

server.start(handlers)
