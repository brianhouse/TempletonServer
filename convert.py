#!/usr/bin/env python3

import pymongo, json, csv
import signal_processing as sp
from housepy import drawing, config, log, util
from mongo import db

START = "2016-07-05 00:00:00"
END = "2016-07-06"

log.info("Retrieving data...")
results = db.stream.find({'t_utc': {'$gt': util.timestamp(util.parse_date(START, tz='America/New_York')), '$lt': util.timestamp(util.parse_date(END, tz='America/New_York'))}}).sort([('t_utc', pymongo.ASCENDING)])
log.info("--> done")

with open("rats.csv", 'w', newline='') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow(('t_utc', 'x', 'y', 'z', 'rms'))
    for result in results:
        writer.writerow((result['t_utc'], result['x'], result['y'], result['z'], result['rms']))

