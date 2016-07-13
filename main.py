#!/usr/bin/env python3

import json, random
from pymongo import ASCENDING
from tornado import websocket
from housepy import server, config, log, strings
    
class Home(server.Handler):

    def get(self, page=None):
        log.info("Home.get")
        if page == "data":
            result = list(self.db.stream.find().sort([('t_utc', ASCENDING)]))
            return self.json(result)
        return self.render("home.html", v=random.randint(0, 1000000))   # dont cache the js

    def post(self, nop=None):
        log.info("Home.post")
        try:
            data = self.request.body.decode('utf-8').split('\n')
            data = [[float(e) for e in d.split(',')] for d in data]
        except Exception as e:
            return log.error(e)
        self.db.stream.insert([{'t_utc': d[0], 'x': d[1], 'y': d[2], 'z': d[3], 'rms': d[4]} for d in data])
        log.info("OK")


class DisplaySocket(websocket.WebSocketHandler):

    sockets = {}

    def open(self):
        log.info("//////////// DisplaySocket.open")
        self.socket_id = strings.random_string(10)
        DisplaySocket.sockets[self.socket_id] = self
        self.device_id = None
        log.info("--> new display socket_id %s" % self.socket_id)
        DisplaySocket.send(self.socket_id, {'socket_id': self.socket_id})

    def on_message(self, data):
        log.info("//////////// DisplaySocket.on_message %s" % data)

    def on_close(self):
        log.info("//////////// DisplaySocket.on_close")
        log.info("--> closing display socket_id %s" % self.socket_id)                
        if self.socket_id in DisplaySocket.sockets:
            del DisplaySocket.sockets[self.socket_id]


class CollarSocket(websocket.WebSocketHandler):

    sockets = {}

    def open(self):
        log.info("//////////// CollarSocket.open")
        self.socket_id = strings.random_string(10)
        CollarSocket.sockets[self.socket_id] = self
        self.device_id = None
        log.info("--> new collar socket_id %s" % self.socket_id)
        CollarSocket.send(self.socket_id, {'socket_id': self.socket_id})

    def on_message(self, data):
        log.info("//////////// CollarSocket.on_message %s" % data)
        try:
            data = json.loads(data)
        except Exception as e:
            log.error(log.exc(e))
            return
        if 'device_id' in data:
            self.device_id = data['device_id']
            CollarSocket.send(self.socket_id, {'linked': True})
        if 'pulses' in data:    # relay for computer script to send pulses to connected devices
            log.info(data)
            CollarSocket.send(self.socket_id, {'success': True})
            for socket_id, socket in CollarSocket.sockets.items():
                if socket is self:
                    continue
                CollarSocket.send(socket_id, data)
        if 'acceleration' in data:  # we are receiving accelerometer data
            log.info(data)

    def on_close(self):
        log.info("//////////// CollarSocket.on_close")
        log.info("--> closing collar socket_id %s" % self.socket_id)                
        if self.socket_id in CollarSocket.sockets:
            del CollarSocket.sockets[self.socket_id]

    @classmethod
    def send(cls, socket_id, message):
        socket = CollarSocket.sockets[socket_id]
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
    (r"/displaysocket", DisplaySocket),    
    (r"/websocket", CollarSocket),    
    (r"/?([^/]*)", Home),
]    

server.start(handlers)
