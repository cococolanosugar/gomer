# -*- coding: utf-8 -*-

import redis

from redis.connection import PythonParser


class Redis(object):
    """oclib wrapper library for Redis

    Implements basic functionality of Redis, mainly the get, set, delete
    functions.

    >>> r = Redis()
    >>> r.set('name', '李园')
    1
    >>> r.get('name')
    李园
    >>> r.delete('name')
    1
    """

    def __init__(self, host='localhost', port=6379, db=0, password=None,
                 encoding='utf-8', encoding_errors='strict',
                 socket_timeout=None, decode_responses=False,
                 parser_class=PythonParser):

        # Set instance attributes
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.encoding = encoding
        self.encoding_errors = encoding_errors
        self.socket_timeout = socket_timeout
        self.decode_responses = decode_responses
        self.parser_class = parser_class

        connection_kwargs = self.__dict__

        # Create connection pool
        self.connection_pool = redis.ConnectionPool(
            connection_class=redis.connection.Connection,
            max_connections=None,
            **connection_kwargs)

        # Create connection to StrictRedis
        self.conn = redis.StrictRedis(connection_pool=self.connection_pool)

    def get(self, key):
        """Gets the value from a redis key

        :param key: redis key
        :type key: str
        """
        return self.conn.get(key)

    def set(self, key, value, ex=None, px=None, nx=False, xx=False):
        """Sets the value to redis key

        :param key: redis key
        :type key: str
        :param value: value of key
        :type value: str
        :param ex: Expire (in seconds)
        :param px: Expire (in milliseconds)
        :param nx: if ``True``, set value at key if key **does not exist**
        :param xx: if ``True``, set value at key if key **exists**
        """
        return self.conn.set(key, value, ex=None, px=None, nx=False, xx=False)

    def delete(self, *keys):
        """Delete one or many keys

        :param *keys: one key (str) or list/tuple of keys
        """
        return self.conn.delete(*keys)

    def incr(self, key, amount=1):
        """Increase the value of a key by an amount

        :param key: key name
        :param amount: amount to increase by (default=1)
        :type amount: int
        """
        return self.conn.incr(key, amount)

    def mget(self, keys, *args):
        """Returns a list of values

        >>> r = Redis()
        >>> kwargs = {'a': 1, 'b': 2, 'c': 3}
        >>> r.mset(**kwargs)
        >>> r.mget(('a', 'b', 'c'))
        ['1', '2', '3']
        """
        return self.conn.mget(keys, *args)

    def mset(self, *args, **kwargs):
        """Sets key/values based on mapping.
        Mapping can be supplied as a single
        dictionary argument or as kwargs
        """
        self.conn.mset(*args, **kwargs)

    # Sorted set functions

    def zadd(self, set_name, *args, **kwargs):
        """Adds an score-name pair to the key ``name``.  Pairs can be
        specified in two ways:

            *args:  score1, name1, score2, name2
            **kwargs:  name1=score1, name2=score2

        Using args and kwargs together would be:
        >>> r = Redis()
        >>> r.zadd('mykey', 1, 'name1', 2, 'name2', name3=34, name4=46)
        4

        :param name: key name
        :type name: str
        :param args: positional arguments
        :param kwargs: keyword arguments
        """
        return self.conn.zadd(set_name, *args, **kwargs)

    def zcard(self, set_name):
        """Return number of elements in sorted set ``set_name``"""
        return self.conn.zcard(set_name)

    def zincrby(self, set_name, name, amount=1):
        """Increment the score of ``name`` in sorted set ``set_name`` by
        ``amount``

        :param set_name: sorted set name
        :param name: name of element in sorted set ``set_name``
        :param amount: amount to add to score of name ``name``
        :return: result of "score + amount"
        :rtype: float
        """
        return self.conn.zincrby(set_name, name, amount=amount)

    def zrange(self, set_name, start, end, desc=True,
               withscores=False, score_cast_func=float):
        """Return a range of values from sorted set ``set_name`` between
        ``start`` and ``end`` sorted in descending order (默认重大排到小)

        :param set_name: name of the sorted set
        :param start: starting index
        :type start: int
        :param end: ending index
        :type end: int
        :param desc: sort results descendingly (default True)
        :type desc: bool
        :param withscores: indicate whether to return (name, score) pairs
        :type withscores: bool
        :param score_cast_func: a callable used to cast score return value
        :type score_cast_func: function
        :rtype: list or list of tuples
        """
        return self.conn.zrange(set_name, start, end, desc=desc,
                         withscores=withscores, score_cast_func=score_cast_func)

    def zrank(self, set_name, name):
        """Returns a 0-based value indicating the *ASCENDING* rank of ``name``
        in sorted set ``set_name``

        :return: 0-based integer value of rank
        :rtype: int
        """
        return self.conn.zrank(set_name, name)

    def zrevrank(self, set_name, name):
        """Returns a 0-based value indicating the *DESCENDING* rank of ``name``
        in sorted set ``set_name``

        :return: 0-based integer value of rank
        :rtype: int
        """
        return self.conn.zrevrank(set_name, name)

    def zscore(self, set_name, name):
        """Returns the score of element ``name`` in sorted set ``set_name``

        :param set_name: sorted set name
        :param name: name of element in sorted set
        :return: score of ``name`` in sorted set ``set_name``
        :rtype: float
        """
        return self.conn.zscore(set_name, name)

    def zrem(self, set_name, *names):
        """Remove ``names`` from sorted set ``set_name``

        :param set_name: sorted set name
        :param *names: names to remove from sorted set ``set_name``
        :return: number of names removed
        :rtype: int
        """
        return self.conn.zrem(set_name, *names)

    def zremrangebyrank(self, set_name, min, max):
        """Remove all elements in the sorted set ``set_name`` with ranks
        between ``min`` and ``max``.  Values are 0-based, ordered from
        smallest score to largest score.  Values can be negative indicating the
        highest scores.

        :param set_name: sorted set name
        :param min: lowest rank
        :type min: int
        :param max: highest rank
        :type max: int
        :return: returns number of elements removed
        :rtype: int
        """
        return self.conn.zremrangebyrank(set_name, min, max)

    def zremrangebyscore(self, set_name, min, max):
        """Remove all elements in the sorted set ``set_name`` with scores
        between ``min`` and ``max``.

        :param set_name: sorted set name
        :param min: lowest score
        :type min: int
        :param max: highest score
        :type max: int
        :return: number of elements removed
        :rtype: int
        """
        return self.conn.zremrangebyscore(set_name, min, max)

    def sadd(self, name, *values):
        """Add ``value(s)`` to set ``name``

        >>>r = Redis()
        >>>r.sadd("test-set", 1, 2, 3, 4)
        4

        :param name: set name
        :param *values: one or more values
        :return: number of values added
        :rtype: int
        """
        return self.conn.sadd(name, *values)

    def scard(self, name):
        """Return the number of elements in set ``name``

        >>>r = Redis()
        >>>r.sadd("test-set", 1, 2, 3, 4)
        >>>r.scard("test-set")
        4

        :param name: set name
        :return: number of elements in set ``name``
        :rtype: int
        """
        return self.conn.scard(name)

    def smembers(self, name):
        """Return all members of the set ``name``

        :param name: set name
        :return: return all members of the set
        :rtype: list
        """
        return self.conn.smembers(name)

    def spop(self, name):
        """Randomly pops a member from set ``name``

        :param name: set name
        :return: a random member of the set
        :rtype: str
        """
        return self.conn.spop(name)

    def srem(self, name, *values):
        """Removes one/many specific member in a set

        :param name: name of set
        :param *values: one/many members to remove from set
        :return: number of members removed from set
        :rtype: int
        """
        return self.conn.srem(name, *values)
