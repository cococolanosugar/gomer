# -*- coding: utf-8 -*-
import os

from bson import Code
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


class Mongo(object):

    def __init__(self, db, host='localhost', port=27017, username=None,
                 password=None, max_pool_size=10, document_class=dict,
                 tz_aware=True, **kwargs):
        self.host = os.getenv('MONGO_HOST', host)
        self.port = os.getenv('MONGO_PORT', port)
        self.max_pool_size = max_pool_size
        self.document_class = dict
        self.tz_aware = True

        if username and password:
            auth = "%(username)s:%(password)s@" % dict(username=username,
                                                       password=password)
        else:
            auth = ''

        if not isinstance(self.host, (list, tuple)):
            self.host = "mongodb://%(auth)s%(host)s:%(port)s/%(db)s" % \
                dict(auth=auth,
                    host=host,
                    port=port,
                    db=db)

        connection_kwargs = self.__dict__

        try:
            self.conn = MongoClient(**connection_kwargs)
        except ConnectionFailure:
            print '***Connection Failure***'
            print 'Switching to localhost'
            self.host = 'localhost'
            self.conn = MongoClient(self.__dict__)
        self.db = self.conn[db]

    def __getattr__(self, name):
        """Get collection using dot notation

        :param name: collection name
        :type name: basestring
        """
        if name != "collection":
            self.collection = self.db[name]
            return self

    def __getitem__(self, name):
        """Get collection name using dict access

        :param name: collection name
        :type name: basestring
        """
        if name != "collection":
            self.collection = self.db[name]
            return self

    def get(self, pk, pk_value):
        """根据文件的pk去取文件

        db.collection.find_one( <query>, <projection> )

        :param pk: 主键名  pk_value: 主键值
        :type pk: basestring pk_value: basestring
        """
        query = {pk: pk_value}
        return self.collection.find_one(query)

    def find(self, query):
        """普通查询

        db.collection.find( <query>, <projection> )

        :param query: 查询条件
        :type query: dict
        """
        return self.collection.find(query)

    def delete(self, pk, pk_value):
        """根据文件的pk删除文件

        db.collection.remove( <query>, <justOne> )

        :param　pk: pk的属性
        :type pk: basestring
        :param pk_value: pk的值
        :type pk_value: basestring
        """
        query = {pk: pk_value}
        return self.collection.remove(query)

    def insert(self, data):
        """加一个文件

        db.collection.insert( <document(s)> )

        :param data: 要存储的文件
        :type data: dict
        """
        self.collection.insert(data)

    def update(self, pk, data):
        '''更新数据，如果找不到就新增
        '''
        query = {pk: data[pk]}
        return self.collection.update(query, data, upsert=True)

    def ensure_index(self, key_or_list, cache_for=300,
                     name=None, unique=False, **kwargs):
        """确保某某index的存在

        :param key_or_list: Takes either a single key or a list of
                            (key, direction) pairs.
                            如果只是一个key,它一定要属于basestring
                            如果是一个list：
                                [(key, direction), (key1, direction1), ...]

                                key: basestring
                                direction: pymongo.ASCENDING *OR* pymongo.DESCENDING
        :param cache_for: time window (in seconds) during which this index
                          will be recognized by subsequent calls to `ensure_index`
        :type cache_for: int
        :param name: name of this index (default=None)
        :param unique: should this index guarantee uniqueness?
        :type unique: boolean

        >>> db.users.ensure_index("uid")

        >>> db.users.ensure_index([("uid", pymongo.DESCENDING),
                                   ("name", pymongo.ASCENDING)])
        """
        if name:
            kwargs['name'] = name
        kwargs['unique'] = unique
        self.collection.ensure_index(key_or_list, cache_for=cache_for,
                                     **kwargs)

    def map_reduce(self, mapper, reduce, full_response=False, **kwargs):
        if isinstance(mapper, basestring):
            mapper = Code(mapper)
        if isinstance(reduce, basestring):
            reduce = Code(reduce)
        self.collection.map_reduce(mapper, reduce,
                                   full_response=full_response, **kwargs)
