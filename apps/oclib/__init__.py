#-*- coding: utf-8 -*-
from django.conf import settings
from apps.oclib.storage import StorageRedis, StorageMongo
from apps.oclib.client import Redis


class App():
    def __init__(self, store_config):
        self.redis_store = StorageRedis(store_config['redis'])

        self.mongo_store = StorageMongo(store_config['mongodb'])

        rtc = store_config['top_redis']
        self.top_redis = Redis(rtc['host'], rtc['port'], rtc['db'])

        self.log_mongo = StorageMongo(store_config['log_mongodb'])

        self.pier = Pier(self.redis_store, settings.PIER_USE)


class Pier(object):
    """用来临时存储等待保存到redis中的用户数据"""
    def __init__(self, store, use):
        self.data = {}
        self.store = store
        self.use = use

    def add(self, user_model):
        uid = user_model.uid
        self.data.setdefault(uid, [])
        self.data[uid].append(user_model)

    def save(self):
        if not self.data:
            return
        for uid, um_list in self.data.iteritems():
            self.store.mset_user_model(uid, set(um_list))
        self.data.clear()

    def clear(self):
        self.data.clear()



app = App(settings.STORAGE_CONFIG)
