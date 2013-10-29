#!/usr/bin/env python
# encoding: utf-8
"""
simplejson库包装，增加datetime, date类型转换支持

Copyright (c) 2011 Rekoo Media. All rights reserved.
"""
import time
from datetime import date
from datetime import datetime

try:
    import json as json
except:
    import simplejson as json


__all__ = ['dump', 'dumps', 'load', 'loads']

def _dumps(obj, skipkeys=False, ensure_ascii=True, check_circular=True,
        allow_nan=True, cls=None, indent=None, separators=None,
        encoding='utf-8', default=None, **kw):
    """为simplejson增加datetime, date类型转换支持
        datetime类型转换为时间戳
        date类型转换为'%Y-%m-%d'格式的字符串
    """
    return json.dumps(obj, skipkeys=skipkeys, ensure_ascii=ensure_ascii, check_circular=check_circular,
                allow_nan=allow_nan, cls=cls, indent=indent, separators=separators,
                encoding=encoding, **kw)
#    def datetime_handler(obj):
#        if isinstance(obj, datetime):
#            return int(time.mktime(obj.timetuple()))
#        elif isinstance(obj, date):
#            return obj.strftime('%Y-%m-%d')
#        else:
#            raise TypeError('%r is not JSON serializable' % obj)

#    return json.dumps(obj, skipkeys=skipkeys, ensure_ascii=ensure_ascii, check_circular=check_circular,
#                allow_nan=allow_nan, cls=cls, indent=indent, separators=separators,
#                encoding=encoding, default=datetime_handler, **kw)

load = json.load
loads = json.loads
dump = json.dump
dumps = _dumps
