#-*- coding: utf-8 -*-
import unittest

from nose.tools import *
from apps.oclib.client import Redis
from apps.oclib.model import BaseModel
from apps.oclib.model import UserModel
from apps.oclib.model import TmpModel
from apps.oclib.model import LogModel
from apps.oclib.model import TopModel
from apps.oclib.model import MongoModel
from apps.oclib import app

class User(UserModel):
    pk = 'uid'
    fields = ['uid','data']

    @classmethod
    def create(cls):
        um = User()
        um.uid = '123456'
        um.data = {'a':1,'b':2}
        return um


class Config(BaseModel):
    pk = 'config_name'
    fields = ['config_name','config_value']

    @classmethod
    def create(cls,config_name,config_value):
        conf = Config()
        conf.config_name = config_name
        conf.config_value = config_value
        return conf

class Tmp(TmpModel):
    pk = 'pid'
    fields = ['pid','uid','data']

    @classmethod
    def create(cls, pid, uid, data):
        t = cls()
        t.uid = uid
        t.pid = pid
        t.data = data
        return t

class Log(LogModel):

    @classmethod
    def create(cls, time, uid, pid, url, api):
        l = cls()
        l.time = time
        l.uid = uid
        l.pid = pid
        l.url = url
        l.api = api
        return l

class Admin(MongoModel):
    pk = 'uid'
    fields = ['name','password','uid','mail']

    @classmethod
    def create(cls, uid, name, password, mail):
        a = cls()
        a.uid = uid
        a.name = name
        a.password = password
        a.mail = mail
        return a


class AdminTestCase(unittest.TestCase):

    def setUp(self):
        self.admin = Admin.create(123456, 'mark.huang', 'abc123', 'mark.huang@newsnsgame.com')
        self.george = Admin.create(123455, 'xu.shicai', 'abc123', 'xu.shicai@newsnsgame.com')
        self.admin.put()
        self.george.put()

    def test_put(self):
        new_user = Admin.create(123457, 'liyuan', 'abc123', 'liyuan@newsnsgame.com')
        new_user.put()
        liyuan_class = Admin.get(123457)
        assert_is_instance(liyuan_class, Admin)
        eq_(liyuan_class.mail, 'liyuan@newsnsgame.com')
        eq_(liyuan_class.uid, 123457)
        new_user.delete()

        admin_class = Admin.get(123456)
        eq_(admin_class.uid, self.admin.uid)
        eq_(admin_class.mail, self.admin.mail)
        eq_(admin_class.name, self.admin.name)
        eq_(admin_class.password, self.admin.password)

    def test_find(self):
        query = {"password": 'abc123'}
        admin_list = Admin.find(query)
        expected_length = 2
        eq_(len(admin_list), expected_length)

        query = {"mail": "mark.huang@newsnsgame.com"}
        admin_list = Admin.find(query)
        expected_length = 1
        eq_(len(admin_list), expected_length)

    def tearDown(self):
        self.admin = None
        app.mongo_store.mongo.db.drop_collection('admin')


class ConfigTestCase(unittest.TestCase):
    def setUp(self):
        self.config = Config.create("card_config", {"a": 0, "b": 1})
        self.config.put()
        for i, v in enumerate(app.redis_store.redis_list):
            setattr(self, 'redis%s' % (i), v)

    def test_get(self):
        the_config = Config.get('card_config')
        expected = {'a': 0, 'b': 1}
        eq_(the_config.config_value, expected)

    def test_delete(self):
        self.config.delete()
        deleted = Config.get('card_config')
        expected = None
        eq_(deleted, expected)

    def test_config_name(self):
        config_name = self.config.config_name
        expected = "card_config"
        eq_(config_name, expected)

    def test_config_value(self):
        config_value = self.config.config_value
        expected = dict(a=0, b=1)
        eq_(config_value, expected)

    def tearDown(self):
        self.config = None
        self.redis0.conn.flushdb()
        self.redis1.conn.flushdb()
        self.redis2.conn.flushdb()


class UserTestCase(unittest.TestCase):

    def setUp(self):
        self.user = User.create()
        for i, v in enumerate(app.redis_store.redis_list):
            setattr(self, 'redis%s' % (i), v)

    def test_uid(self):
        uid = self.user.uid
        expected = '123456'
        assert_is_instance(uid, str)
        eq_(uid, expected)

    def test_data(self):
        data = self.user.data
        expected = {'a':1,'b':2}
        assert_is_instance(data, dict)
        eq_(data, expected)

    def test_instance_of_base_model(self):
        assert_is_instance(self.user, BaseModel)

    def test_put_operation(self):
        result = self.user.do_put()
        assert_is_instance(result, int)
        eq_(result, 1)

    def test_get_operation(self):
        result = self.user.do_put()
        assert_is_instance(result, int)
        eq_(result, 1)

        user = User.get(self.user.uid)
        eq_(user.uid, self.user.uid)

    def tearDown(self):
        self.user = None
        self.redis0.conn.flushdb()
        self.redis1.conn.flushdb()
        self.redis2.conn.flushdb()


class TmpModelTestCase(unittest.TestCase):
    pass

class LogModelTestCase(unittest.TestCase):
    pass

class TopModelTestCase(unittest.TestCase):
    def setUp(self):
        self.tm = TopModel.create('test_top')
        self.setup_top_model()
        self.redis = Redis(db=15)

    def setup_top_model(self):
        self.tm.set('liyuan', 123)
        self.tm.set('mark', 12)

    def test_set(self):
        result = self.tm.set('liyuan', 321)
        expected = 0
        eq_(result, expected)

    def test_get(self):
        get_result = self.tm.get()
        expected = [('liyuan', 123), ('mark', 12)]
        eq_(get_result, expected)

        get_result2 = self.tm.get(3, False)
        expected = [('mark', 12), ('liyuan', 123)]
        eq_(get_result2, expected)

    def test_remove(self):
        added = self.tm.set('li', 1)
        expected_added = 1
        eq_(added, expected_added)

        to_be_removed = ('li',)
        removed = self.tm.remove(*to_be_removed)
        expected_removed = 1
        eq_(removed, expected_removed)

    def test_remove_by_score(self):
        result = self.tm.set('li', 1)
        expected = 1
        eq_(result, expected)

        remove = self.tm.remove_by_score(0, 2)
        expected = 1
        eq_(remove, expected)

    def test_remove_last(self):
        eq_(1, self.tm.set('li', 1))
        eq_(1, self.tm.remove_last(1))
        eq_(1, self.tm.set('li', 1000))
        eq_(1, self.tm.remove_last(1, False))

    def test_rank(self):
        eq_(0, self.tm.rank('liyuan'))

    def test_count(self):
        eq_(2, self.tm.count())

    def tearDown(self):
        self.redis.conn.flushdb()
        self.redis = None
        self.tm = None

def suite():
    suite = unittest.TestSuite()
    suite.addTest(UserModelTestCase())
    suite.addTest(ConfigTestCase())
    suite.addTest(TopModelTestCase())
    suite.addTest(AdminTestCase())
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    test_suite = suite()
    runner.run(test_suite)

