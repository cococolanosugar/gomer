#-*- coding: utf-8 -*-
import unittest
import redis

from apps.oclib.client import Redis
from nose.tools import *


class RedisTestCase(unittest.TestCase):

    def setUp(self):
        self.r = Redis(host='localhost', port=6379)
        self.setup_sorted_sets()
        self.setup_sets()

    def setup_sorted_sets(self):
        self.r.zadd('maxstrike:win', 5, 'liyuan', 7, 'mark', lilei=2, shicai=3)

    def setup_sets(self):
        self.r.sadd('tomongo', "James", "Mark", "Rendy", "Chris")

    def test_connection_instance(self):
        assert_is_instance(self.r.conn, redis.StrictRedis)

    def test_ping_function_exists(self):
        ping_exists = 'ping' in dir(self.r.conn)
        assert_true(ping_exists)

    def test_connection(self):
        pong = self.r.conn.ping()
        assert_true(pong)

    def test_zadd_one(self):
        number_of_new_entries = self.r.zadd('maxstrike:win', 11, 'rendy')
        assert_is_instance(number_of_new_entries, int)
        eq_(number_of_new_entries, 1)

    def test_zadd_multi(self):
        number_of_new_entries = self.r.zadd('maxstrike:win', 11, 'rendy', 12, 'mandy')
        assert_is_instance(number_of_new_entries, int)
        eq_(number_of_new_entries, 2)

    def test_zadd_update(self):
        number_of_new_entries = self.r.zadd('maxstrike:win', 11, 'rendy')
        assert_is_instance(number_of_new_entries, int)
        eq_(number_of_new_entries, 1)

        updated = self.r.zadd('maxstrike:win', 12, 'rendy')
        assert_is_instance(updated, int)
        eq_(updated, 0)

        retrieve_updated = self.r.zscore('maxstrike:win', 'rendy')
        assert_is_instance(retrieve_updated, float)
        eq_(retrieve_updated, 12.0)

    def test_zcard(self):
        number_of_elements = self.r.zcard('maxstrike:win')
        assert_is_instance(number_of_elements, int)
        eq_(number_of_elements, 4)

    def test_zincrby(self):
        score = self.r.zincrby('maxstrike:win', 'shicai', amount=3)
        assert_is_instance(score, float)
        eq_(self.r.conn.zscore('maxstrike:win', 'shicai'), 6)

    def test_zscore(self):
        score = self.r.zscore('maxstrike:win', 'liyuan')
        expected = 5
        assert_is_instance(score, float)
        eq_(score, expected)

    def test_zrange(self):
        rrange = self.r.zrange('maxstrike:win', 0, 3)
        expected = ['mark', 'liyuan', 'shicai', 'lilei']
        eq_(rrange, expected)

    def test_zrange_ascending(self):
        rrange = self.r.zrange('maxstrike:win', 0, 3, desc=False)
        expected = ['lilei', 'shicai', 'liyuan', 'mark']
        eq_(rrange, expected)

    def test_zrange_withscores(self):
        rrange = self.r.zrange('maxstrike:win', 0, 3, withscores=True)
        expected = [
            ('mark', 7),
            ('liyuan', 5),
            ('shicai', 3),
            ('lilei', 2)
        ]
        eq_(rrange, expected)

    def test_zrank(self):
        rrank = self.r.zrank('maxstrike:win', 'shicai')
        expected = 1
        eq_(rrank, expected)

    def test_zrevrank(self):
        rrank = self.r.zrevrank('maxstrike:win', 'shicai')
        expected = 2
        eq_(rrank, expected)

    def test_zrem(self):
        remove = self.r.zrem('maxstrike:win', 'shicai')
        rrange = self.r.zrange('maxstrike:win', 0, 3, withscores=True)
        expected = [
            ('mark', 7),
            ('liyuan', 5),
            ('lilei', 2)
        ]
        eq_(remove, 1)
        eq_(rrange, expected)

    def test_zremrangebyrank(self):
        remove = self.r.zremrangebyrank('maxstrike:win', 2, 3)
        eq_(remove, 2)
        rrange = self.r.zrange('maxstrike:win', 0, 3,
                               desc=False, withscores=True)
        expected = [
            ('lilei', 2),
            ('shicai', 3)
        ]
        eq_(rrange, expected)

    def test_zremrangebyscore(self):
        remove = self.r.zremrangebyscore('maxstrike:win', 3, 5)
        eq_(remove, 2)
        rrange = self.r.zrange('maxstrike:win', 0, 3,
                               desc=False, withscores=True)
        expected = [
            ('lilei', 2),
            ('mark', 7)
        ]
        eq_(rrange, expected)

    def test_sadd(self):
        number_of_values = self.r.sadd('tomongo', "Jon", "Emily")
        expected = 2
        assert_is_instance(number_of_values, int)
        eq_(number_of_values, expected)

    def test_scard(self):
        total = self.r.scard('tomongo')
        expected = 4
        assert_is_instance(total, int)
        eq_(total, expected)

    def test_smembers(self):
        all_members = self.r.smembers("tomongo")
        expected = set([
            "James",
            "Mark",
            "Rendy",
            "Chris"
        ])
        assert_is_instance(all_members, set)
        eq_(all_members, expected)

    def test_spop(self):
        for i in range(2):
            self.r.spop("tomongo")
        number_left = self.r.scard("tomongo")
        expected = 2
        eq_(number_left, expected)

    def tearDown(self):
        self.r.zremrangebyrank('maxstrike:win', 0, 100)
        self.r.conn.flushdb()
        self.r = None


def suite():
    suite = unittest.TestSuite()
    suite.addTest(RedisTestCase())
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    test_suite = suite()
    runner.run(test_suite)
