#!/usr/bin/env python3

import pymongo, time
from housepy import video, config, log, animation, util
from collections import deque
from mongo import db

PATH = "/Users/house/Projects/rats/bronx_lab/1467738431_.mov"
# PATH = "/Users/house/Projects/rats/bronx_lab/BDMV_5.mov"
# PATH = "/Users/house/Projects/rats/bronx_lab/video-720p-h264.mov"


START = "2016-07-05 12:30:00"
END = "2016-07-06"

log.info("Retrieving data...")
results = db.stream.find({'t_utc': {'$gt': util.timestamp(util.parse_date(START, tz='America/New_York')), '$lt': util.timestamp(util.parse_date(END, tz='America/New_York'))}}).sort([('t_utc', pymongo.ASCENDING)])
log.info("--> done")


ctx = animation.Context(640, 480, background=(1.0, 1.0, 1.0, 1.), fullscreen=False, title="collar stream")    

graph = deque()
start_time = time.time()
current_data = results.next()
data_start_time = current_data['t_utc']

def draw():
    global start_time, data_start_time, current_data
    elapsed_time = time.time() - start_time    
    while True:
        data_elapsed_time = current_data['t_utc'] - data_start_time
        # print("data_elapsed_time", data_elapsed_time)
        if data_elapsed_time >= elapsed_time:
            break
        graph.appendleft(current_data['rms'])
        if len(graph) == ctx.width:
            graph.pop()        
        current_data = results.next()
            
    ctx.plot(graph)

ctx.start(draw)
