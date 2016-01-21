#!/usr/bin/env python3

import pymongo
from housepy import drawing, config, log
import signal_processing as sp

mongo = config['mongo']
client = pymongo.MongoClient(mongo['host'], mongo['port'])
db = client[mongo['database']]

result = list(db.stream.find().sort([('t_utc', pymongo.ASCENDING)]))
# print(list(result))

ts = [r['t_utc'] for r in result]
xs = [r['x'] for r in result]

duration = ts[-1] - ts[0]
SAMPLING_RATE = 100

signal = sp.resample(ts, xs, duration * SAMPLING_RATE)
signal += 1 # change -1,1 to 0,2
signal = sp.normalize(signal, 0, 2)

ctx = drawing.Context(1000, 400)
ctx.plot(signal, stroke=(0.0, 0.0, 0.0, 1.0), thickness=1.0)
ctx.output("graphs")