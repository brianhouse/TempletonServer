#!/usr/bin/env python3

from housepy import config, log
from pymongo import MongoClient, GEOSPHERE, ASCENDING, DESCENDING

mongo = config['mongo']
client = MongoClient(mongo['host'], mongo['port'])
db = client[mongo['database']]

db.stream.remove()