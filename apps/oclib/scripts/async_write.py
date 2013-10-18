#!/usr/bin/env python
#-*- coding: utf-8 -*-
import json
import time
from apps.oclib.client import Redis, Mongo


R2M = "r2m_set"

REDIS_CONF = {
    'rmaster': {
        'host': 'localhost',
        'port': 6379,
        'db': 0
    },
    'rslave': {
        'host': 'localhost',
        'port': 6380,
        'db': 0
    }
}

MONGO_CONF = {
    'host': 'localhost',
    'port': 27017,
    'db': 'maxstrike',
    'username': '',
    'password': ''
}

rmaster = Redis(**REDIS_CONF['rmaster'])
rslave = Redis(**REDIS_CONF['rslave'])
mongo = Mongo(**MONGO_CONF)

def retrieve_data(key):
    # Retrieves JSON string
    data = rslave.get(key)

    # Convert to python dict for mongodb
    return json.loads(data)

def pop_from_set():
    return rmaster.spop(R2M)

def main():
    key = pop_from_set()
    while key:
        data = retrieve_data(key)
        _class_name, pk = key.split(":")
        mongo[_class_name].set(data)
        key = pop_from_set()


if __name__ == '__main__':
    while 1:
        main()
        time.sleep(5*60)
