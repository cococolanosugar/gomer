#!/usr/bin/env python
# encoding: utf-8
#******************************
# 绱㈠紩閰嶇疆鏂囦欢
#
#******************************

{
   'mongodb': {
        # Collection
        'config': {
            'index': 'config_name',
            'unique': True
        },
        'accountmapping': {
            'index': 'pid',
            'unique': True
        },
        'accountoneclick': {
            'index': 'pid',
            'unique': True
        },
        'usercollection': {
            'index': 'uid',
            'unique': True
        },
        'friend': {
            'index': 'uid',
            'unique': True
        },
        'exceptusers': {
            'index': 'except_type',
            'unique': True
        },
        'leveluser': {
            'index': 'lv',
            'unique': True
        },
        'ptusers': {
            'index': 'pt_lv',
            'unique': True
        },
        'userbase': {
            'index': 'uid',
            'unique': True
        },
        'usercards': {
            'index': 'uid',
            'unique': True
        },
        'usercity': {
            'index': 'uid',
            'unique': True
        },
        'userdungeon': {
            'index': 'uid',
            'unique': True
        },
        'userequips': {
            'index': 'uid',
            'unique': True
        },
        'usergift': {
            'index': 'uid',
            'unique': True
        },
        'userlend': {
            'index': 'uid',
            'unique': True
        },
        'userlogin': {
            'index': 'uid',
            'unique': True
        },
        'userproperty': {
            'index': 'uid',
            'unique': True
        },
        'userpvp': {
            'index': 'uid',
            'unique': True
        },
        'username': [
            {
                'index': 'name',
                'unique': True
            },
            {
                'index': 'uid',
                'unique': True
            },
        ],

    },
    'log_mongodb': {
        #充值记录
        'chargerecord': [
            {
                'index': 'oid',
                'unique': True
            },
            {
                'index': 'uid'
            },
            {
                'index': 'platform'
            },
            {
                'index': 'createtime'
            }
        ],
        #消费记录
        'consumerecord': [
            {
                'index': 'uid',
            },
            {
                'index': 'consume_type'
            },
            {
                'index': 'createtime'
            }
        ],


    }
}
