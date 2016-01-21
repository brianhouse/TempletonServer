#!/usr/bin/env python3

from housepy import config, log
from pymongo import MongoClient, GEOSPHERE, ASCENDING, DESCENDING

mongo = config['mongo']
client = MongoClient(mongo['host'], mongo['port'])
db = client[mongo['database']]

def make_indexes():
  try:
      db.stream.create_index([("t_utc", ASCENDING)])
  except Exception as e:
      log.error(log.exc(e))

if __name__ == "__main__":
  make_indexes()
