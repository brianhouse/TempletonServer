#!/usr/bin/env python3

import json, pymongo
from housepy import server, config, log
    
class Home(server.Handler):

    def get(self, page=None):
        log.info("Home.get")
        result = list(self.db.stream.find().sort([('t_utc', pymongo.ASCENDING)]))
        return self.json(result)
        # return self.text("rat server!")

    def post(self, nop=None):
        log.info("Home.post")
        try:
            data = self.request.body.decode('utf-8').split('\n')
            data = [[float(e) for e in d.split(',')] for d in data]
        except Exception as e:
            return log.error(e)
        self.db.stream.insert([{'t_utc': d[0], 'x': d[1], 'y': d[2], 'z': d[3], 'rms': d[4]} for d in data])
        log.info("OK")

handlers = [
    (r"/?([^/]*)", Home),
]    

server.start(handlers)
