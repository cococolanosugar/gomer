#-*- coding: utf-8 -*-
import unittest
import redis

from nose.tools import *
from apps.oclib.model import BaseModel
from apps.oclib import storage


class UserModel(BaseModel):
    pk = 'uid'
    fields = ['uid', 'value']

    @classmethod
    def create(cls):
        um = cls()
        um.uid = '123456'
        um.value = {'a': 1, 'b': 2}
        return um


class StorageTestCase(unittest.TestCase):

    def setUp(self):
        self.storage = storage.Storage()

    def test_get(self):
        self.assertRaises(NotImplementedError, self.storage.get, 1)

    def test_set(self):
        self.assertRaises(NotImplementedError, self.storage.set, {'a': 1})

    def tearDown(self):
        self.storage = None


class StorageRedisTestCase(unittest.TestCase):

    def setUp(self):
        config = [{'host': 'localhost', 'port': 6379, 'db': 0}]
        self.redis = storage.StorageRedis(config)
        self.user = UserModel.create()

    def test_hostname(self):
        hostname = self.redis.redis_list[0].host
        eq_(hostname, 'localhost', 'Hostname is not "localhost"')

    def test_port(self):
        port = self.redis.redis_list[0].port
        eq_(port, 6379, 'Port is not set to 6379')

    def test_db(self):
        db = self.redis.redis_list[0].db
        eq_(db, 0, 'DB is not set to 0')

    def test_redis_connection(self):
        redis_connection = self.redis.redis_list[0].conn
        assert_is_instance(redis_connection, redis.StrictRedis)

    def test_set(self):
        set_response = self.redis.set(self.user)
        assert_true(set_response)

    def test_get(self):
        self.redis.set(self.user)
        obj = self.redis.get(UserModel, 123456)
        assert_is_instance(obj, UserModel)

    def tearDown(self):
        self.user = None
        self.redis.redis_list[0].conn.flushdb()
        self.redis = None


def suite():
    suite = unittest.TestSuite()
    suite.addTest(StorageTestCase())
    suite.addTest(StorageRedisTestCase())
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    test_suite = suite()
    runner.run(test_suite)
