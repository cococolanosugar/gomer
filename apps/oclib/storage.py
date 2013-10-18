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
        key = _class.__name__.lower() + ':' + str(pk)
        value = self.redis_list[self._hash(key)].get(key)
        if not value:
            return None
        value = msgpack.loads(value, encoding='utf-8')
        return _class.load(value)

    def set(self, obj, ex=None):
        key = self._get_obj_key(obj)
        value = self._to_msgpack(obj)

        redis = self.redis_list[self._hash(key)]
        redis.sadd(R2M_SET, key)
        return redis.set(key, value, ex)

    def get_user_model(self, _class, uid):
        key = _class.__name__.lower() + ':' + str(uid)
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
        return self.redis_list[self._hash(key)].delete(key)

    def _get_obj_key(self, obj):
        return obj.__class__.__name__.lower() + ":" + str(getattr(obj, obj.pk))

    def _to_msgpack(self, obj):
        return msgpack.dumps(obj.to_dict(), encoding='utf-8')

    def _hash(self, key):
        return binascii.crc32(key) % len(self.redis_list)


class StorageMongo(Storage):
    def __init__(self, config):
        self.mongo = Mongo(config['db'], host=config['host'], port=config['port'])

    def get(self, _class, pk_value):
        collection = _class.__name__.lower()
        data = self.mongo[collection].get(_class.pk, pk_value)
        if data:
            return _class.load(data)
        return None

    def set(self, obj):
        collection = obj.__class__.__name__.lower()
        return self.mongo[collection].update(obj.pk,obj.to_dict())

    def insert(self, obj):
        collection = obj.__class__.__name__.lower()
        return self.mongo[collection].insert(obj.__dict__)

    def find(self, _class, query):
        collection = _class.__name__.lower()
        data_list = self.mongo[collection].find(query)
        if data_list:
            return [_class.load(data) for data in data_list]
        return None

    def delete(self, obj):
        collection = obj.__class__.__name__.lower()
        return self.mongo[collection].delete(obj.pk, str(getattr(obj, obj.pk)))

