#-*- coding: utf-8 -*-
from apps.oclib.client import Redis, Mongo
import msgpack
import binascii

R2M_SET = 'r2m_set'

class Storage(object):
    def get(self, id):
        raise NotImplementedError

    def set(self, obj):
        raise NotImplementedError


class StorageRedis(Storage):
    def __init__(self, config):
        self.redis_list = [Redis(c['host'], c['port'], c['db']) for c in config]

    def get(self, _class, pk):
        key = self._get_cls_key(_class, pk)
        value = self.redis_list[self._hash(key)].get(key)
        if not value:
            return None
        value = msgpack.loads(value, encoding='utf-8')
        return _class.load(value)

    def set(self, obj, ex=None, r2m=True):
        key = self._get_obj_key(obj)
        value = self._to_msgpack(obj)

        redis = self.redis_list[self._hash(key)]
        if r2m:
            redis.sadd(R2M_SET, key)
        return redis.set(key, value, ex)

    def get_user_model(self, _class, uid):
        key = self._get_cls_key(_class, uid)
        value = self.redis_list[self._hash(uid)].get(key)
        if not value:
            return None
        value = msgpack.loads(value, encoding='utf-8')
        return _class.load(value)

    def set_user_model(self, obj):
        key = self._get_obj_key(obj)
        value = self._to_msgpack(obj)

        redis = self.redis_list[self._hash(obj.uid)]
        redis.sadd(R2M_SET, key)
        return redis.set(key, value)

    def mset_user_model(self, uid, user_model_set):
        redis = self.redis_list[self._hash(uid)]
        wkargs = {}
        for um in user_model_set:
            key = self._get_obj_key(um)
            wkargs[key] = self._to_msgpack(um)
            redis.sadd(R2M_SET, key)
        if wkargs:
            return redis.mset(**wkargs)
        return False

    def delete(self, obj):
        key = self._get_obj_key(obj)
        redis = self.redis_list[self._hash(key)]
        redis.srem(R2M_SET, key)
        return redis.delete(key)

    def delete_user_model(self, obj):
        key = self._get_obj_key(obj)
        redis = self.redis_list[self._hash(obj.uid)]
        redis.srem(R2M_SET, key)
        return redis.delete(key)

    def _get_obj_key(self, obj):
        return '%s:%s' %(obj.__class__.__name__.lower(), str(getattr(obj, obj.pk)))

    def _get_cls_key(self, _class, pk):
        return '%s:%s' %(_class.__name__.lower(), str(pk))

    def _to_msgpack(self, obj):
        return msgpack.dumps(obj.to_dict(), encoding='utf-8')

    def _hash(self, key):
        if len(self.redis_list) == 1:
            return 0
        return binascii.crc32(key) % len(self.redis_list)


class StorageMongo(Storage):
    def __init__(self, config):
        self.mongo = Mongo(config['db'], host=config['host'], port=config['port'], \
                           username=config['username'],password=config['password'])

    def get(self, _class, pk_value):
        collection = _class.__name__.lower()
        data = self.mongo[collection].get(_class.pk, pk_value)
        if data:
            return _class.load(data)
        return None

    def set(self, obj):
        collection = obj.__class__.__name__.lower()
        return self.mongo[collection].update(obj.pk, obj.to_dict())

    def insert(self, obj):
        collection = obj.__class__.__name__.lower()
        return self.mongo[collection].insert(obj.__dict__)

    def find(self, _class, query,**kwargs):
        collection = _class.__name__.lower()
        data_list = self.mongo[collection].find(query,**kwargs)
        if data_list:
            return [_class.load(data) for data in data_list]
        return None

    def orderby(self, _class, query, sort):
        """
        Orders documents after a find query

        Example:
            db.users.find( {"status": "active"}, [("uid", -1), ("name", 1)] )

        :param _class: class of object
        :param query: query used to find documents in ``collection``
        :type query: dict
        :param sort: (key, direction) pairs
        :type sort: list
        """
        collection = _class.__name__.lower()
        data_list = self.mongo[collection].find(query, sort=sort)
        if data_list:
            return [_class.load(data) for data in data_list]
        return None

    def delete(self, obj):
        collection = obj.__class__.__name__.lower()
        val = getattr(obj, obj.pk)
        if not isinstance(val,unicode):
            val = str(val)
        return self.mongo[collection].delete(obj.pk, val)

    def aggregate(self, _class, statement):
        """
        用法请看：　http://api.mongodb.org/python/current/examples/aggregation.html

        :param _class: class of object
        :param statement: 这是一个aggregate
        :type statement: dict/list/tuple
        """
        collection = _class.__name__.lower()
        output = self.mongo[collection].aggregate(statement)
        if output['ok'] == 1.0:
            return output['result']
