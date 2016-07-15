#!/usr/bin/env python3

import json, random, os, __main__
from pymongo import ASCENDING
from tornado import websocket
from housepy import server, config, log, strings, s3

    
class Home(server.Handler):

    def get(self, page=None):
        log.info("Home.get")
        if page == "data":
            result = list(self.db.stream.find().sort([('t_utc', ASCENDING)]))
            return self.json(result)
        videos = [filename for filename in os.listdir(os.path.abspath(os.path.join(os.path.dirname(__main__.__file__), "static", "video"))) if filename[-3:] == "mov"]
        # videos = s3.list_contents()
        # "https://s3.amazonaws.com/%s/%s.wav" % (config['s3']['bucket'], data['t'])
        return self.render("home.html", v=random.randint(0, 1000000), videos=videos)   # dont cache the js

    def post(self, nop=None):
        log.info("Home.post")
        try:
            data = self.request.body.decode('utf-8').split('\n')
            data = [[float(e) for e in d.split(',')] for d in data]
        except Exception as e:
            return log.error(e)
        self.db.stream.insert([{'t_utc': d[0], 'x': d[1], 'y': d[2], 'z': d[3], 'rms': d[4]} for d in data])
        log.info("OK")


class Scripts(server.Handler):

    def get(self, script=None):
        log.info("Sketch.get %s" % script)
        videos = [filename for filename in os.listdir(os.path.abspath(os.path.join(os.path.dirname(__main__.__file__), "static", "video"))) if filename[-3:] == "mov"]        
        # videos = s3.list_contents()
        return self.render(script, server=config['url'], videos=videos)


class DisplaySocket(websocket.WebSocketHandler):

    sockets = {}

    def open(self):
        log.info("//////////// DisplaySocket.open")
        self.socket_id = strings.random_string(10)
        DisplaySocket.sockets[self.socket_id] = self
        log.info("--> new display socket_id %s" % self.socket_id)
        DisplaySocket.send(self.socket_id, {'socket_id': self.socket_id})

    def on_message(self, message):
        log.info("//////////// DisplaySocket.on_message %s" % data)
        try:
            message = json.loads(message)
        except Exception as e:
            log.error(log.exc(e))
            return
        if 'start' in message:
            log.info("Retrieving data for socket...")
            results = db.stream.find({'t_utc': {'$gt': util.timestamp(util.parse_date(message['start'], tz='America/New_York'))}}).sort([('t_utc', pymongo.ASCENDING)])
            log.info("--> done")
            while True:
                data = results.next()
                if data is None:
                    break
                DisplaySocket.send(self.socket_id, data)    # this needs to be asyncronous


    def on_close(self):
        log.info("//////////// DisplaySocket.on_close")
        log.info("--> closing display socket_id %s" % self.socket_id)                
        if self.socket_id in DisplaySocket.sockets:
            del DisplaySocket.sockets[self.socket_id]

    @classmethod
    def send(cls, socket_id, message):
        socket = DisplaySocket.sockets[socket_id]
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
    (r"/scripts/?([^/]*)", Scripts),     
    (r"/?([^/]*)", Home),
]    

server.start(handlers)
