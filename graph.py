#!/usr/bin/env python3

import pymongo, json
import signal_processing as sp
from housepy import drawing, config, log, util
from mongo import db

START = "2016-07-05 00:00:00"
END = "2016-07-06"

log.info("Retrieving data...")
results = list(db.stream.find({'t_utc': {'$gt': util.timestamp(util.parse_date(START, tz='America/New_York')), '$lt': util.timestamp(util.parse_date(END, tz='America/New_York'))}}).sort([('t_utc', pymongo.ASCENDING)]))
log.info("--> done")

##

ts = [r['t_utc'] for r in results]
xs = [r['x'] for r in results]

duration = ts[-1] - ts[0]
SAMPLING_RATE = 100

log.info("Resampling...")
signal = sp.resample(ts, xs, duration * SAMPLING_RATE)
signal += 1 # change -1,1 to 0,2
signal = sp.normalize(signal, 0, 2)
log.info("--> done")

log.info("Drawing...")
ctx = drawing.Context(1000, 400)
ctx.plot(signal, stroke=(0.0, 0.0, 0.0, 1.0), thickness=1.0)
ctx.output("graphs")
log.info("--> done")

