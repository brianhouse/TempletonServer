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
        self.socket_id = strings.random_string(10)
        WebSocket.sockets[self.socket_id] = self
        self.device_id = None
        log.info("--> new socket_id %s" % self.socket_id)
        WebSocket.send(self.socket_id, {'socket_id': self.socket_id})

    def on_message(self, data):
        log.info("//////////// WebSocket.on_message %s" % data)
        try:
            data = json.loads(data)
        except Exception as e:
            log.error(log.exc(e))
            return
        if 'device_id' in data:
            self.device_id = data['device_id']
            WebSocket.send(self.socket_id, {'linked': True})

    def on_close(self):
        log.info("//////////// WebSocket.on_close")
        log.info("--> closing socket_id %s" % self.socket_id)                
        if self.socket_id in WebSocket.sockets:
            del WebSocket.sockets[self.socket_id]

    @classmethod
    def send(cls, socket_id, message):
        socket = WebSocket.sockets[socket_id]
        try:
            message = json.dumps(message)
        except:
            log.error("--> message not json formatted")
        else:
            log.info("--> sending %s to %s" % (message, socket_id))
            try:
                socket.write_message(message)
            except Exception as e:
                log.error(log.exc(e))


handlers = [
    (r"/websocket", WebSocket),    
    (r"/?([^/]*)", Home),
]    

server.start(handlers)
