#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import argparse
import textwrap
from ast import literal_eval as eval

from apps.oclib.client import Mongo

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

log = logging.getLogger('indexer')
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)

description = '''\
    *****************************************
    初始化MaxStrike
    *****************************************
    MaxStrike启动前需要建MongoDB的索引．

    用户需要提供一或多个目标服务器才能运行脚本
'''

MONGODB = {
    'dev': {
        'mongodb': {
            'host': 'localhost',
            'port': 27017,
            'db': 'maxstrike',
            'username': '',
            'password': ''
        },
        'log_mongodb': {
            'host': 'localhost',
            'port': 27017,
            'db': 'maxstrike_log',
            'username': '',
            'password': ''
        }
    },
    'qa': {
        'mongodb': {
            'host': '10.200.55.32',
            'port': 27017,
            'db': 'maxstrike',
            'username': '',
            'password': ''
        },
        'log_mongodb': {
            'host': '10.200.55.32',
            'port': 27017,
            'db': 'maxstrike_log',
            'username': '',
            'password': ''
        }
    },
    'prod': {
        'mongodb': {
            'host': '10.6.2.9',
            'port': 27017,
            'db': 'cnmaxstrikedb1a',
            'username': 'cnmaxstrikeuser1a',
            'password': 'cnmaxstrikeuPwD1a0%'
        },
        'log_mongodb': {
            'host': '10.6.2.9',
            'port': 27017,
            'db': 'logcnmaxstrikedb1a',
            'username': 'logcnmaxstrikeuser1a',
            'password': 'logcnmaxstrikeuPWd10a%'
        }
    },
    'appstore_prod': {
        'mongodb': {
            'host': '172.31.25.6',
            'port': 27017,
            'db': 'awsmaxstrikedb1a',
            'username': 'awsmaxstrikeuser1a',
            'password': 'awsmaxstrikeuPwD1ao%'
        },
        'log_mongodb': {
            'host': '172.31.25.6',
            'port': 27017,
            'db': 'logawsmaxstrikedb1a',
            'username': 'logawsmaxstrikeuser1a',
            'password': 'logawsmaxstrikeuPWd1oa%'
        }
    }
}

def main():
    """
    Indexes MongoDB
    """
    parser = init_parser(description)
    args = parser.parse_args()

    # 把读进来的配置文件转成字典
    config = eval(args.config.read())

    if isinstance(args.target, list):
        for target in args.target:
            log.debug("切换环境： %s" % target)
            log.debug("\n")
            the_mongo = MONGODB[target]
            if isinstance(the_mongo, dict):
                process_index('mongodb', the_mongo, config)
                process_index('log_mongodb', the_mongo, config)

def process_index(database, connection_settings, config_dict):
    """
    Adds index to mongodb

    :param database: key name of mongodb instance(s) in settings.py
    :type database: str
    :param connection_settings: mongodb connection parameters of TARGET
    :type connection_settings: dict
    :param config_dict: indexing config file converted to python dict
    :type config_dict: dict
    """

    # 这是针对某某database (mongodb 或 log_mongodb)的连接
    db = connect(connection_settings, database)
    log.debug("%s连接成功" % database)
    log.debug("-"*40)
    log.debug('\n')

    # 取出某某database的索引配置
    conf = config_dict[database]

    if conf and isinstance(conf, dict):
        for collection, index in conf.iteritems():
            if isinstance(index, dict):
                index_name = db[collection].create_index(index['index'], unique=index.get('unique', False))
                log.debug("集合： %s\t\t建索引： %s" % (collection, index_name))
            elif isinstance(index, list):
                for idx in index:
                    index_name = db[collection].create_index(idx['index'], unique=idx.get('unique', False))
                    log.debug("集合： %s\t\t建索引： %s" % (collection, index_name))
        log.debug("\n")

def connect(connection_settings, database):
    return Mongo(**connection_settings[database])

def init_parser(description):
    """
    Initialize parser
    """
    parser = argparse.ArgumentParser(
        prog='indexer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(description))
    parser.add_argument('target',
                        type=str,
                        choices=['dev', 'qa', 'prod','appstore_prod'],
                        nargs='+',
                        default='dev',
                        help='建索引的目标服务器: dev=localhost, qa=测试服务器, prod=发布服务器, appstore_prod=appstore发布服务器'
                        )
    parser.add_argument('-f',
                        '--file',
                        dest='config',
                        metavar='config',
                        type=argparse.FileType('r'),
                        required=True,
                        help='请提供一个索引配置文件'
                        )
    return parser

if __name__ == '__main__':
    main()
