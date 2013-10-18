# -*- coding: utf-8 -*-
import time

from apps.oclib.client import Redis
from random import random
from functools import wraps

NUMBER_OF_MEMBERS = 1000000

names = []
scores = []


def timed(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        start = time.time()
        result = f(*args, **kwds)
        elapsed = time.time() - start
        print "%s took %2.2f seconds to finish" % (f.__name__, elapsed)
        return result
    return wrapper

def generate_lists():
    for i in xrange(NUMBER_OF_MEMBERS):
        names.append(str(i))
        scores.append(int(100000*random()))
    return names, scores

def generate_pairs(names, scores):
    return dict(zip(names, scores))

@timed
def zrange(db):
    db.zrange('max:loss', 0, 30, withscores=True)

@timed
def zadd(db, kwargs):
    for k,v in kwargs.iteritems():
        db.zadd('abc:loss', v, k)

def main():
    db = Redis()
    db.conn.flushdb()
    names, scores = generate_lists()
    kwargs = generate_pairs(names, scores)
    zadd(db, kwargs)
    zrange(db)

if __name__ == '__main__':
    main()
