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
        self.put_data = {}
        self.store = store
        self.get_data = {}
        self.use = use

    def add(self, user_model):
        uid = user_model.uid
        self.put_data.setdefault(uid, [])
        if user_model not in self.put_data[uid]:
            self.put_data[uid].append(user_model)
        self.get_data.setdefault(uid, [])
        if user_model not in self.get_data[uid]:
            self.get_data[uid].append(user_model)
    
    def add_get_data(self, user_model):
        uid = user_model.uid
        self.get_data.setdefault(uid, [])
        if user_model not in self.get_data[uid]:
            self.get_data[uid].append(user_model)

    def save(self):
        if not self.put_data:
            return
        for uid, um_list in self.put_data.iteritems():
            self.store.mset_user_model(uid, set(um_list))
        self.clear()

    def clear(self):
        self.put_data.clear()
        self.get_data.clear()

    def get(self, _class, uid):
        um_list = self.get_data.get(uid)
        if not um_list:
            return None
        for um in um_list:
            if isinstance(um, _class):
                return um
        return None



app = App(settings.STORAGE_CONFIG[settings.STORAGE_INDEX])
