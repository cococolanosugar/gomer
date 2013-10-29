#!/usr/bin/env python
#-*- coding: utf-8 -*-
import msgpack
import time
import sys
import logging
import datetime
import traceback
import argparse
import textwrap
from bson.errors import InvalidDocument
from ast import literal_eval as eval
from apps.oclib.client import Redis, Mongo
from django.conf import settings

LOGDIR = settings.BASE_ROOT+"/logs/asyncwrite_logs"
R2M = "r2m_set"

description = '''\
    *****************************************
    异步写
    *****************************************
    将redis的数据写入到mongo
'''

MONGO_CONF = {
    'host': 'localhost',
    'port': 27017,
    'db': 'maxstrike',
    'username': '',
    'password': ''
}

mongo = Mongo(**MONGO_CONF)

EXCEPT_KEYS = []

def retrieve_data(rslave,key):
    # Retrieves msgpack string
    data = rslave.get(key)
    if not data:
        return {}

    # Convert to python dict for mongodb
    return msgpack.loads(data, encoding='utf-8')

def pop_from_set(rmaster):
    return rmaster.spop(R2M)

def add_to_set(rmaster,key):
    return rmaster.sadd(R2M, key)

def init_parser(description):
    """
    Initialize parser
    """
    parser = argparse.ArgumentParser(
        prog='async_write',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(description))
    parser.add_argument('target',
                        type=str,
                        nargs='+',
                        default='0',
                        help='对应的配置文件中的外层id'
                        )
    parser.add_argument('-f',
                        '--file',
                        dest='config',
                        metavar='config',
                        type=argparse.FileType('r'),
                        required=True,
                        help='请提供一个redis配置文件'
                        )
    return parser

def process_async_write(rmaster,rslave,log):
    key = pop_from_set(rmaster)
    log.info("writeToDB begin at %s", datetime.datetime.now())
    log.info("first key: %s", key)
    write_key_cnt = 0
    #加回去
    global EXCEPT_KEYS
    EXCEPT_KEYS = list(set(EXCEPT_KEYS))
    log.info("EXCEPT_KEYS:%s" % str(EXCEPT_KEYS))
    while EXCEPT_KEYS:
        add_to_set(rmaster,EXCEPT_KEYS.pop())
    while key:
        data = retrieve_data(rslave,key)
        _class_name, pk = key.split(":")
        for dkey, dvalue in data.iteritems():
            if str(dvalue) == str(pk):
                try:
                    mongo[_class_name].update(dkey, data)
                    write_key_cnt += 1
                except InvalidDocument,TypeError:
                    log.error("%s TypeError or InvalidDocument" % key)
                    log.error(sys.exc_info())
                except:
                    log.error("%s could not be write to mongo" % key)
                    log.error(sys.exc_info())
                    EXCEPT_KEYS.append(key)
                break
        else:
            log.error("%s could not be found" % key)
        key = pop_from_set(rmaster)
    
    log.info("total write cnt:%s" % write_key_cnt)

def main():
    parser = init_parser(description)
    args = parser.parse_args()

    if isinstance(args.target, list):
        target = args.target[0]

        log = logging.getLogger('async_write')
        hdlr = logging.FileHandler(LOGDIR+"/write_to_mongo%s.log" % target)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', '%T')
        hdlr.setFormatter(formatter)
        log.addHandler(hdlr)
        log.setLevel(logging.DEBUG)
        # 把读进来的配置文件转成字典
        try:
            config = eval(args.config.read())
        except:
            config = None
            log.error(sys.exc_info())
            return

        if config and target in config:
            rmaster = Redis(**config[target]['rmaster'])
            rslave = Redis(**config[target]['rslave'])
            while 1:
                try:
                    process_async_write(rmaster,rslave,log)
                except:
                    log.error(traceback.format_exc())
                    log.error(sys.exc_info())
                time.sleep(5*60)
        else:
            log.error("conf:%s not exist or async_write_conf.py null" % target)



if __name__ == '__main__':
    main()

