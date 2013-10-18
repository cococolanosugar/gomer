#-*- coding: utf-8 -*-
def memoize(f):
    cache = {}
    def ret(*args):
        if args in cache:
            return cache[args]
        else:
            answer = f(*args)
            cache[args] = answer
            return answer
    return ret
