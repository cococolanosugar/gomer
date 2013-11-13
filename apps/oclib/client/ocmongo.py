# -*- coding: utf-8 -*-
import os

from bson import Code
from bson import ObjectId
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


class Mongo(object):

    def __init__(self, db='', host='localhost', port=27017, username=None,
                 password=None, max_pool_size=10, document_class=dict,
                 tz_aware=True, **kwargs):
        self.host = host#os.getenv('MONGO_HOST', host)
        self.port = port#os.getenv('MONGO_PORT', port)
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

        self.conn = MongoClient(**connection_kwargs)
        self.db = self.conn[db]

    def __getattr__(self, name):
        """Get collection using dot notation

        :param name: collection name
        :type name: basestring
        """
        if name != "collection":
            if name in ('conn', 'db'):
                pass
            self.collection = self.db[name]
            return self

    def __getitem__(self, name):
        """Get collection name using dict access

        :param name: collection name
        :type name: basestring
        """
        if name != "collection":
            if name in ('conn', 'db'):
                pass
            self.collection = self.db[name]
            return self

    def get(self, pk, pk_value, **kwargs):
        """根据文件的pk去取文件

        db.collection.find_one( <query>, <projection> )

        :param pk: 主键名  pk_value: 主键值
        :type pk: basestring pk_value: basestring
        """
        exclude_id = {'_id': False}

        if pk == '_id':
            pk_value = ObjectId(pk_value)

        if 'fields' in kwargs:
            if isinstance(kwargs['fields'], dict):
                kwargs['fields'].update(exclude_id)

        query = {pk: pk_value}
        return self.collection.find_one(query, **kwargs)

    def find(self, query, **kwargs):
        """普通查询

        db.collection.find( <query>, <projection> )

        :param query: 查询条件
        :type query: dict
        """
        exclude_id = {'_id': False}
        if 'fields' in kwargs:
            if isinstance(kwargs['fields'], dict):
                kwargs['fields'].update(exclude_id)

        return self.collection.find(query, **kwargs)

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
        :return: `_id` value or list of `_ids`
        :rtype: str
        """
        docid = self.collection.insert(data)
        return docid

    def update(self, pk, data):
        '''更新数据，如果找不到就新增
        '''
        query = {pk: data[pk]}
        return self.collection.update(query, data, upsert=True)

    def drop_indexes(self):
        return self.collection.drop_indexes()

    def drop_index(self, idx):
        return self.collection.drop_index(idx)

    def create_index(self, key_or_list, cache_for=157784630, name=None,
                     unique=False, **kwargs):
        if name:
            kwargs['name'] = name
        kwargs['unique'] = unique
        return self.collection.create_index(key_or_list, cache_for=cache_for,
                                            **kwargs)

    def ensure_index(self, key_or_list, cache_for=157784630,
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
                          value must be in seconds (default 5 years=157784630s)
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
        return self.collection.ensure_index(key_or_list, cache_for=cache_for,
                                     **kwargs)

    def index_information(self):
        """Get information about a collection's indexes"""
        return self.collection.index_information()

    def map_reduce(self, mapper, reducer, out, full_response=False, **kwargs):
        if isinstance(mapper, basestring):
            mapper = Code(mapper)
        if isinstance(reducer, basestring):
            reducer = Code(reducer)
        return self.collection.map_reduce(mapper, reducer, out,
                                          full_response=full_response, **kwargs)

    def aggregate(self, mongo_statement):
        """
        Example:
            db.collection.aggregate( {"$group": {"_id": "$status", "count": {"$sum": 1}}} )
        Output:
            {'ok': 1.0, 'result': [{'count': 3, '_id': 'inactive'}, {'count': 2, '_id': 'active'}]}

        :param mongo_statement: a mongo aggregate statement
        :type mongo_statement: dict/list/tuple
        :return: a dictionary with keys "ok" and "result"
        """
        return self.collection.aggregate(mongo_statement)
