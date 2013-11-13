#-*- coding: utf-8 -*-
import datetime
from apps.oclib import app
from django.conf import settings

GAME_UID_KEY = settings.GAME_UID_KEY
GAME_START_DATE = datetime.datetime.strptime(settings.GAME_START_DATE, '%Y-%m-%d')
GAME_UID_MIN = settings.GAME_UID_MIN

def next_uid(app_id='', plat_id=''):

    days = (datetime.datetime.now() - GAME_START_DATE).days
    days = str(days + 1000)

    num = app.redis_store.redis_list[0].incr(GAME_UID_KEY) + GAME_UID_MIN
    if num >= 1000000:
        num = GAME_UID_MIN
        app.redis_store.redis_list[0].set(GAME_UID_KEY,0)

    nls = list(str(num))
    if len(nls) != 6:
        return None

    for i in range(len(nls)):
        if i % 2 == 0:
            nls[i], nls[i+1] = nls[i+1], nls[i]
    nls.reverse()
    seq = ''.join(nls)

    uid = '%s%s%s%s' % (app_id, plat_id, days, seq)
    return uid
