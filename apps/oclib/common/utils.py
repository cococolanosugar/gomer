#-*- coding: utf-8 -*-
import random
import operator
import traceback, sys, cStringIO, os
import datetime, time
from cgi import parse_qsl
import cPickle as pickle
import socket
import os
import urllib
import copy
import string

import pytz
import pycurl

import json

def random_100_occur(probability = 50):
    """
        概率为1--100整数进制
    """
    r = random.randint(1,100)
    if r <= probability:
        return True
    else:
        return False

def random_occur(probability = 0.5):
    r = random.random()
    if r<probability:
        return True
    else:
        return False

def random_int_choice(config, num = 10000):
    '''
    概率为1--100整数进制， num要为100的倍数
    '''
    #config = [(10, 'data'), (20, 'data'), (70, 'data')]
    #thesum = reduce(operator.add, [item[0] for item in config], 0)
    #if thesum>1:
    #    raise Exception, 'config error'

    mul = num/100
    r = random.randint(1,num)
    kk = 0
    for item in config:
        kk += item[0] * mul
        if r<=kk:
            return item[1]

def random_choice(config):
    #config = [(0.1, 20), (0.2, 30), (0.7, 40)]
    #thesum = reduce(operator.add, [item[0] for item in config], 0)
    #if thesum>1:
    #    raise Exception, 'config error'

    r = random.random()
    kk = 0
    for item in config:
        kk += item[0]
        if r<kk:
            return item[1]

def random_range(start, end):
    r = random.random()
    return r*(end-start)+start

def random_range_multi(start, end, num, interval):
    #0, 24, 4, 1 从0-24中选择4个数且间隔不能小于1
    res = []
    section_range = (end-start)/(num+0.0)

    select_num = None
    for i in range(num):
        if select_num is None:
            select_start = start
        else:
            select_start = select_num + interval

        select_end = start + section_range*(i+1)

        select_num = random_range(select_start, select_end)
        res.append(select_num)

    return res


#str转化成datetime
def str_to_datetime(datestr,format):
    return datetime.datetime.strptime(datestr,format)

#两个时间间隔的天数
def date_diff(begin_date,end_date):
    format="%Y-%m-%d";
    bd=str_to_datetime(begin_date,format)
    ed=str_to_datetime(end_date,format)
    oneday=datetime.timedelta(days=1)
    count=0
    while bd!=ed:
        ed=ed-oneday
        count+=1
    return count



#增加字典某个字段的值
def add2dict(d, k, v):
    if d.has_key(k):
        d[k] += v
    else:
        d[k] = v

#将两个字典的value合并成一个列表
def merge_dict(d1, d2):

    d3 = {}
    for k in d1:
        d2_value = d2[k] if d2.has_key(k) else 0
        d3[k] = [d1[k], d2_value]

    return d3

#将两个字典的key value 合并成一个字典
def merge_dict2(d1, d2):
    d3 = d1.copy()
    for k in d2:
        if d3.has_key(k):
            d3[k] += d2[k]
        else:
            d3[k] = d2[k]
    return d3

def change_str(date_str):
    '''
    #{{{ 时间转换格式
    '''
    t = time.strptime(date_str, '%Y-%m-%d')
    return datetime.date(*t[0:3])
    #}}}

def get_err():
    f = cStringIO.StringIO( )
    traceback.print_exc(file=f)
    return f.getvalue( )

def print_err():
    sys.stderr.write('=='*30+os.linesep)
    sys.stderr.write('err time: '+str(datetime.datetime.now())+os.linesep)
    sys.stderr.write('--'*30+os.linesep)
    traceback.print_exc(file=sys.stderr)
    sys.stderr.write('=='*30+os.linesep)

def utc_to_tz(utc_dt_str, utc_fmt='%Y-%m-%dT%H:%M:%SZ', tz=None):
    """
        将UTC时区的时间转换为当前时区的时间
        当前时区取django settings.py 中设置的时区
        如：在settings.py文件中的设置
        TIME_ZONE = 'Asia/Tokyo'

        PARAMS:
            * utc_dt_str - utc时区时间，字符串类型。如：2010-01-14T07:00:20Z
            * utc_fmt - utc时区时间格式。如：%Y-%m-%dT%H:%M:%SZ
            * tz - 当前时区，如：Asia/Tokyo

        RETURNS: tz_dt
    """
    if tz is None:
        tz = os.environ['TZ']

    utc_fmt_dt = datetime.datetime.strptime(utc_dt_str, utc_fmt)
    utc_dt = datetime.datetime(utc_fmt_dt.year, utc_fmt_dt.month, utc_fmt_dt.day, utc_fmt_dt.hour, utc_fmt_dt.minute, utc_fmt_dt.second, tzinfo=pytz.utc)
    tz_dt = utc_dt.astimezone(pytz.timezone(tz))

    return tz_dt


def gift_dict2list(rand_res):
    """#{{{ gift_dict2list: 将传进来单个givegift礼物字典转成列表
    args:
        rand_res:    ---   {'farm' : {'seeds' : {'niuyouyumi':1}}}
                        {'ranch':{'properties':{'feedstuffs':{'xunjie':3}}}
    returns:
        0    ---    ['farm', 'seeds', '', 'niuyouyumi', 1]
                    ['ranch', 'properties', 'feedstuffs', 'xunjie', 3]
    """
    for scene_type in rand_res :
        for res_type in rand_res[scene_type]:
            if res_type in ['seeds', 'babies', 'gift_bags', 'mystic_bags', 'dog', 'dog_food', 'harvest', 'cake_ticket']:
                for name in rand_res[scene_type][res_type]:
                    num = rand_res[scene_type][res_type][name]
                    return [scene_type, res_type, '', name, num]

            elif res_type in ['properties', 'decorations']:
                for item_type in rand_res[scene_type][res_type]:
                    for name in rand_res[scene_type][res_type][item_type]:
                        num = rand_res[scene_type][res_type][item_type][name]
                        return [scene_type, res_type, item_type, name, num]
            else:
                pass

def list2list(rand_res):
    """
        整理列表，
        args:['farm', 'seeds', '', 'niuyouyumi', 1]
        result:['farm', 'seeds','niuyouyumi', 1]
    """
    if rand_res[1] in ['seeds', 'babies', 'gift_bags', 'mystic_bags', 'dog', 'dog_food', 'harvest', 'cake_ticket']:
        return [rand_res[0],rand_res[1],rand_res[3],rand_res[4]]
    return rand_res

def gift_list2dict(goods_list):
    """#{{{ gift_list2dict: 将传进来列表转成givegift接口得结构
    args:
        goods_list:    ---    like ['farm', 'properties', 'fertilizer', 'test', 1]
    returns:
        0    ---
    """
    scene_type, category, goods_type, goods_name, give_num = goods_list
    if not goods_type:
        return {
                scene_type: {
                    category: {
                        goods_name: give_num,
                    },
                },
        }
    else:
        return {
                scene_type: {
                    category: {
                        goods_type:{
                            goods_name: give_num,
                        }
                    },
                },
        }
    #}}}

def gift_list2dict_multi(goods_lists):
    """#{{{ gift_list2dict_multi: docstring
    args:
        goods_list:    ---    arg
    returns:
        0    ---
    """
    if not goods_lists:
        return []
    if len(goods_lists) == 1:
        return [gift_list2dict(goods_lists[0])]
    type_same = []
    no_same = []
    goods_lists = sorted(list(copy.deepcopy(goods_lists)))
    for i, goods_list in enumerate(goods_lists):
        if not i:
            pre_goods = goods_list
            continue
        # type_same
        if goods_list[:3] == pre_goods[:3]:
            if i == 1:
                type_same = [pre_goods]
            type_same.append(goods_list)
        # no_same
        else:
            if i == 1:
                no_same = [pre_goods]
            no_same.append(goods_list)
        pre_goods = goods_list
    all_result = []
    if type_same and no_same:
        if type_same[0] in no_same:
            type_same.append(type_same[0])
            no_same.remove(type_same[0])
    if no_same:
        for goods in no_same:
            all_result.append(gift_list2dict(goods))
    if type_same:
        scene_type, category, goods_type = type_same[0][:3]
        result = gift_list2dict(type_same[0])
        d = result[scene_type][category][goods_type] if goods_type else result[scene_type][category]
        for goods in type_same[1:]:
            d[goods[3]] = d.setdefault(goods[3], 0) + goods[4]
        all_result.append(result)
    return sorted(all_result)
    #}}}


def make_dict(goods_dict):
    '''
        #{{{将传进来的商品参数，包装成字典，然后调用统一的商品接口
        goods_dict = {
            'scene_type'    : 'farm' or 'ranch' or 'factory' or 'common'
            'category'      : 'seeds' or 'babies' or 'property' or 'decorations' or 'juice'
            'goods_type'    : 'fertilizer' or 'feedstuffs'
            'name'          : goods_english_name,
            'num'           : int,
        }
    '''
    scene_type  = goods_dict['scene_type']
    category    = goods_dict['category']
    goods_type  = goods_dict.get('goods_type','')
    goods_name  = goods_dict['name']
    give_num    = goods_dict['num']

    #只判断物品的小分类，由此来确定如何组装字典
    if not goods_type:
        return {
                scene_type: {
                    category: {
                        goods_name: give_num,
                    },
                },
        }
    else:
        return {
                scene_type: {
                    category: {
                        goods_type:{
                            goods_name: give_num,
                        }
                    },
                },
        }
    #}}}

addr_dict = {
        # 用于生成地址的字典，为下面的make_image_addr服务
        'farm_harvest'          :'seed/',
        'farm_seeds'            :'seed/',
        'farm_flower'           :'flower/',
        'farm_fertilizer'       :'property/fertilizer_',
        'ranch_babies'          :'baby/',
        'ranch_harvest'         :'harvest/',
        'ranch_feedstuffs'      :'property/feedstuffs_',
        'common_mystic_bags'    : 'mystic_bag/',
        'common_gift_bags'      : 'gift_bag/',
    }
def make_image_addr(scene_type, category, goods_key, goods_type=''):
    """#{{{ make_image_addr: 用户生成种子，花，farm收获物，ranch收获物，化肥，饲料的
                                图片地址
    args:
        scene_type      ---    场景类型，'farm', 'ranch'
        category        ---    类别，'seeds', 'babies', 'property', 'harvest'
        goods_key       ---    产品的英文key
        goods_type      ---    子类，'flower', 'fertilizer', 'feedstuffs'
    returns:
        图片地址
    """

    type = goods_type or category
    pic =  ''.join([
                    'assets/images/item/',
                    addr_dict.get(scene_type+'_'+type, 'seed/'),
                    goods_key,
                    '.swf'
                ])
    return pic
    #}}}

configs = {
            'farm_seeds'        : "common_config.farm_config.crops",
            'farm_harvest'      : "common_config.farm_config.crops",
            'farm_properties'   : "common_config.farm_config.properties",
            'farm_decorations'  : "common_config.farm_config.decorations",
            'ranch_babies'      : "common_config.ranch_config.babies",
            'ranch_harvest'     : "common_config.ranch_config.babies",
            'ranch_properties'  : "common_config.ranch_config.properties",
            'factory_juice'     : "common_config.fac_config['goods']['juice']",
            'common_mystic_bags': "common_config.mystic_bags",
            'common_gift_bags'  : "common_config.gift_bags",
          }
def get_goods_info(scene_type, category, goods_type, goods_key):
    """#{{{ get_gift_name_cn: 获得物品的信息
    gift:    ---    [sence_type, category, goods_type, goods_key, num]
    return:
            字符窜，需要用eval获得真正的数据
    """
    config_str = '_'.join([scene_type, category])
    if goods_type:
        return '%s.get("%s").get("%s")'%(configs[config_str], goods_type, goods_key)
    else:
        return '%s.get("%s")'%(configs[config_str], goods_key)
    #}}}

    #}}}


    #}}}

def get_date_str(dt = None):
    if dt is None:
        dt = datetime.datetime.now()

    return dt.strftime('%Y-%m-%d')

def parse_date_str(date_str,format="%Y-%m-%d"):
    d = datetime.datetime.strptime(date_str,format)

    return d

def get_time_str(dt = None):
    if dt is None:
        dt = datetime.datetime.now()

    return dt.strftime('%Y-%m-%d %H:%M:%S')

def get_time_str2(t):
    """#{{{ get_time_str2: 将time.time()的值转换成'%Y-%m-%d %H:%M:%S'
    args:
        t:    ---    arg
    returns:
        0    ---
    """
    t2 = time.localtime(t)
    return time.strftime('%Y-%m-%d %H:%M:%S', t)
    #}}}

def parse_time_str(date_str):
    t = time.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    return datetime.datetime(*t[0:6])

def format_time(target_time):
  now = datetime.datetime.now()
  tdelta = now - target_time

  if tdelta.days < 0:
    ret_time = u"就在刚才"
  else:
    if tdelta.days > 0:
      ret_time = u"%d天前" % tdelta.days
    elif (tdelta.seconds / (60*60)) > 0:
      ret_time = u"%d小时前" % (tdelta.seconds / (60*60))
    elif (tdelta.seconds / (60)) > 0:
      ret_time = u"%d分钟前" % (tdelta.seconds / 60)
    else:
      ret_time = u"就在刚才"

  return ret_time

def dec2s2(dec):
    """#{{{ dec2s2: 将10进制int数转换成62进制
    args:
        dec:    ---    10进制数
    returns:
        0    ---
    """
    dec = int(dec)
    numbers = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    result = ''

    while dec != 0:
        result = numbers[dec%62] + result
        dec = dec/62

    return result
    #}}}

def s22dec(s2):
    """#{{{ s22dec: 将62进制数转换成10进制数
    args:
        s2:    ---    62位数
    returns:
        0    ---
    """
    numbers = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    result = 0
    l = len(s2)

    n = 0
    while n < l:
        result *= 62
        result += numbers.index(s2[n])
        n += 1

    return result
    #}}}

def make_key(i):
    """#{{{ make_key: 借用输入的int和time.time()生成一个uuid，输出uuid.int的62位码
                        为保证唯一性，i应该<15位
    args:
        i:    ---    int
    returns:
        62位数字, 字符串
    """
    import time, uuid
    i = abs(int(i))
    time_ = time.time()
    time_ = str(time_).replace('.', '')[::-1]
    node = str(i)+time_
    node = int(node[:14])
    uuid_ = uuid.uuid1(node=node)
    return dec2s2(uuid_.int)
    #}}}

def print_(msg='', mark='', need_locals=True):
    from django.conf import settings
    if not getattr(settings, 'DEBUG', False):
        return
    frame = sys._getframe().f_back
    fc = frame.f_code
    pre_frame = frame.f_back
    pre_fc = pre_frame.f_code
    print '\t'.join([mark,'caller:',  pre_fc.co_filename, pre_fc.co_name, str(pre_frame.f_lineno)])
    print '\t'.join([mark, fc.co_filename, fc.co_name, str(frame.f_lineno)]), ":"
    if need_locals:
        print mark, '\t', frame.f_locals
    print mark, '\t', msg



def pycurl_get(url, timeout_ms = 3000, headers = [], verbose = 0):
    """
        pycurl HTTP GET 请求

        timeout_ms - 超时时间，微妙
        headers - HTTP HEADER 信息
        verbose - 0：打印请求信息；1：不打印请求信息
    """
    write_func = cStringIO.StringIO()

    curl = pycurl.Curl()

    curl.setopt(pycurl.URL, url)
    curl.setopt(curl.WRITEFUNCTION, write_func.write)
    curl.setopt(pycurl.VERBOSE, verbose)
    curl.setopt(pycurl.TIMEOUT_MS, timeout_ms)
    curl.setopt(pycurl.FOLLOWLOCATION, 1)
    curl.setopt(pycurl.MAXREDIRS, 5)

    if headers is not None and len(headers) > 0:
        curl.setopt(pycurl.HTTPHEADER, headers)

    curl.perform()

    data = {}
    data['http_status_code'] = curl.getinfo(pycurl.HTTP_CODE)
    data['response'] = write_func.getvalue()

    return data

def pycurl_post(url, post_data, timeout_ms = 3000, headers = [], verbose = 0):
    """
        pycurl HTTP POST 请求

        post_data - post 数据，字典类型
        timeout_ms - 超时时间，微妙
        headers - HTTP HEADER 信息
        verbose - 0：打印请求信息；1：不打印请求信息
    """
    write_func = cStringIO.StringIO()

    curl = pycurl.Curl()

    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.POST, 1)
    curl.setopt(pycurl.POSTFIELDS, urllib.urlencode(post_data))
    curl.setopt(curl.WRITEFUNCTION, write_func.write)
    curl.setopt(pycurl.VERBOSE, verbose)
    curl.setopt(pycurl.TIMEOUT_MS, timeout_ms)
    curl.setopt(pycurl.FOLLOWLOCATION, 1)
    curl.setopt(pycurl.MAXREDIRS, 5)

    if headers is not None and len(headers) > 0:
        curl.setopt(pycurl.HTTPHEADER, headers)

    curl.perform()

    data = {}
    data['http_status_code'] = curl.getinfo(pycurl.HTTP_CODE)
    data['response'] = write_func.getvalue()

    return data


def make_feed_finaldata(sessionid, feed_data):
    """#{{{ make_feed: 生成用于和mixi交互的feed信息
    args:
        feed_data   --- feed原始数据
    """
    result = {}
    result['title'] = feed_data.get('title', '')
    if feed_data.get('image'):
        imageUrl = 'http://i.rekoo.com/static/mixi/farm' + feed_data['image']
        result['image'] = urllib.quote(imageUrl) + ',image/jpeg'
    result['mobileUrl'] = feed_data.get('mb_url', '')
    result['url'] = feed_data.get('pc_url', '')
    callback_url = settings.BASEURL + '/m/common_feed_callback/?sessionid=%s&ft=%s&%s'\
                                        % (
                                            sessionid,
                                            feed_data['opt_callback'].get('ft','None'),
                                            feed_data['opt_callback'].get('mb_callback_url','')
                                          )
    result['callback_Url'] = "create:activity?callback=%s&guid=ON" % (urllib.quote(callback_url))

    return result
    #}}}

def make_request_finaldata(sessionid, feed_data):
    """#{{{ make_request_finaldata: 生成request最终数据
    args:
        data:    ---    arg
    returns:
        0    ---
    """
    result = {}
    result['message'] = feed_data.get('message', '')
    if feed_data.get('image'):
        imageUrl = settings.MEDIA_URL+ feed_data['image']
        result['image'] = urllib.quote(imageUrl) + ',image/jpeg'
    result['description'] = feed_data['opt_params'].get('description', '')
    result['mobile_url'] = feed_data['opt_params'].get('mobile_url', '')
    result['url'] = feed_data['opt_params'].get('url', '')
    callback_url = settings.BASEURL + '/m/common_feed_callback/?sessionid=%s&ft=%s&%s'\
                                        % (
                                            sessionid,
                                            feed_data['opt_callback'].get('ft','None'),
                                            feed_data['opt_callback'].get('mb_callback_url','')
                                          )
    result['post_url'] = "invite:friends?callback=%s&guid=ON" % (urllib.quote(callback_url))

    return result
    #}}}

def make_request_finaldata2(sessionid, feed_data):
    """#{{{ make_request_finaldata: 生成request最终数据
    args:
        data:    ---    arg
    returns:
        0    ---
    """
    result = {}
    result['message'] = feed_data.get('message', '')
    imageUrl = feed_data['opt_params'].get('image', '')
    if imageUrl:
        result['image'] = settings.MEDIA_URL + imageUrl + ',image/gif'
    result['description'] = feed_data['opt_params'].get('description', '')
    result['mobile_url'] = feed_data['opt_params'].get('mobile_url', '')
    result['url'] = feed_data['opt_params'].get('url', '')
    result['target_users'] = ','.join(feed_data['opt_params'].get('target', []))
    callback_url = settings.BASEURL + '/m/common_feed_callback2/?sessionid=%s&ft=%s&real_owner=%s&request_key=%s'\
                                        % (
                                            sessionid,
                                            feed_data['opt_callback'].get('ft','None'),
                                            feed_data['opt_params'].get('real_owner',''),
                                            feed_data['opt_params'].get('request_key',''),
                                          )
    result['post_url'] = "invite:friends?callback=%s&guid=ON" % (urllib.quote(callback_url))

    return result
    #}}}


def voice_template_handler(method,sessionid,message=None):
    """
    围脖模板
    args:
        method      -- str,  发送围脖的类型
        message       -- str,  发送围脖默认显示的内容
    """
    voice = {}
    voice['message'] = message
    voice['vt'] = method
    pc_para = {'vt':method}
    voice['url'] = 'http://mixi.jp/run_appli.pl?id=%s&appParams=%s' % (settings.APP_ID,\
        urllib.quote(json.dumps(pc_para)))
    mb_voice = urllib.quote(settings.MOBILE_BASEURL + '/m/voice_click/?vt=' + method)
    voice['mb_url'] = 'http://ma.mixi.net/%s/?url=%s' % (settings.APP_ID,mb_voice)

    callback_url = settings.BASEURL + '/m/voice_callback/?sessionid=%s&vt=%s' % (sessionid,method)
    voice['callback_url'] = 'update:status?callback=' + urllib.quote(callback_url) + '&guid=ON'
    return voice
    #}}}

def request_share_template_handler2(method, self_name, url_params, feed_template, message=None):
    """#{{{ request_share_template_handler: docstring
    args:
        method             --- str,  发送request_share的类型
        self_name       --- str,  自己的日文名字
        message         --- str,  要显示的文字信息
        image           --- str,  图片地址，从static/images/以下开始
    returns:
        0    ---
    """
    data = {'self': self_name}

    # 当key(title)不存在时，默认返回 ${none_title}
    # 在template替换(title_template.substitute)时抛出KeyError异常，返回None
    title = feed_template.get('title', '${none_title}')
    title_template = string.Template(title)

    description = feed_template.get('description', '')

    # 准备 message
    if message is not None:
        data['message'] = message
    try:
        message = title_template.substitute(data)
    except KeyError:
        print_err()
        return None

    #{{{ 准备点击mb地址
    mb_params = copy.deepcopy(url_params)
    mb_params["ft"] = method
    temp = []
    for item in mb_params.iteritems():
        temp.append(':'.join(item))
    mb_params = {'para':'$$'.join(temp)}
    data['mobile_url_params'] = urllib.quote(urllib.urlencode(mb_params))

    temp_url = settings.MOBILE_BASEURL + '/m/request_click/?'
    mb_url = 'http://ma.mixi.net/%s/?url=%s${mobile_url_params}' % (settings.APP_ID,urllib.quote(temp_url))
    mb_url_template = string.Template(mb_url)
    #}}}
    #{{{ 准备点击pc地址
    url_params["ft"] = method
    url_params["ct"] = 'rsa'
    pc_url_params = json.dumps(url_params)
    data['pc_url_params'] = urllib.quote(pc_url_params)
    pc_url = 'http://mixi.jp/run_appli.pl?id=%s&appParams=${pc_url_params}' % (settings.APP_ID)
    pc_url_template = string.Template(pc_url)
    #}}}
    opt_callback = feed_template.get('opt_callback',{})
    opt_callback['ft'] = method
    opt_callback['pc_callback_url'] = opt_callback['mb_callback_url'] = '&'.join([
                        opt_callback['callback_url'],
                        'ft='          + method,
                        'request_key=' + url_params['request_key'],
                        'real_owner='  + url_params['real_owner'],
                        ])

    try:
        return {
            'message'       : message,
            'opt_callback'  : opt_callback,
            'opt_params'    : {
                'description' : description,
                'image'       : feed_template.get('image', ''),
                'filter_type' : 'mixi.Request.FilterType.BOTH',
                'url'         : pc_url_template.substitute(data),
                'mobile_url'  : mb_url_template.substitute(data),
                'real_owner'  : url_params['real_owner'],
                'request_key' : url_params['request_key'],
            },
        }
    except:
        print_err()
        return None
    #}}}

def request_share_template_handler(method, self_name, url_params=None, message=None):
    """#{{{ request_share_template_handler: docstring
    args:
        method             --- str,  发送request_share的类型
        self_name       --- str,  自己的日文名字
        message         --- str,  要显示的文字信息
        image           --- str,  图片地址，从static/images/以下开始
    returns:
        0    ---
    """
    from farm_lib.logics import common_config
    if method not in common_config.feed_send:
        return None
    feed_template = copy.deepcopy(common_config.feed_send.get(method, {}))
    data = {'self': self_name}

    # 当key(title)不存在时，默认返回 ${none_title}
    # 在template替换(title_template.substitute)时抛出KeyError异常，返回None
    title = feed_template.get('title', '${none_title}')
    title_template = string.Template(title)

    description = feed_template.get('description', '')

    # 准备 message
    if message is not None:
        data['message'] = message
    try:
        message = title_template.substitute(data)
    except KeyError:
        print_err()
        return None

    #{{{ 准备mb点击地址
    mb_params = copy.deepcopy(url_params)
    mb_params["ft"] = method
    temp = []
    for item in mb_params.iteritems():
        temp.append(':'.join(item))
    mb_params = {'para':'$$'.join(temp)}
    data['mobile_url_params'] = urllib.quote(urllib.urlencode(mb_params))

    temp_url = settings.MOBILE_BASEURL + '/m/common_feed_click/?'
    mb_url = 'http://ma.mixi.net/%s/?url=%s${mobile_url_params}' % (settings.APP_ID,urllib.quote(temp_url))
    mb_url_template = string.Template(mb_url)
    #}}}
    #{{{ 准备pc点击地址
    url_params["ft"] = method
    pc_url_params = json.dumps(url_params)
    data['pc_url_params'] = urllib.quote(pc_url_params)
    pc_url = 'http://mixi.jp/run_appli.pl?id=%s&appParams=${pc_url_params}' % (settings.APP_ID)
    pc_url_template = string.Template(pc_url)
    #}}}

    try:
        opt_callback = feed_template.get('opt_callback',{})
        opt_callback['ft'] = method
        return {
            'message'       : message,
            'opt_callback'  : opt_callback,
            'opt_params'    : {
                'description' : description,
                'image'       : feed_template.get('image'),
                'filter_type' : 'mixi.Request.FilterType.BOTH',
                'url'         : pc_url_template.substitute(data),
                'mobile_url'  : mb_url_template.substitute(data),
            },
        }
    except:
        print_err()
        return None
    #}}}


def feed_template_handler(method, self_name, friend_name=None, message=None,
                          url_params=None):
    """feed模板处理器

    将feed模板中配置的${self}, ${friend}, ${message}替换为实际需要的内容

    Args:
        method: 需要发送feed动作，如task.everyday_login, gift.send_gift等
        self_name: 当前登录用户名称
        friend_name: 交互好友名称
        message: 动态的提示信息，如获得了某某种子等
        url_params: feed url参数，字典类型。约定：key为参数名，value为参数值

    Returns:
        返回处理后的feed信息，类型为字典。如：
        {
            'title': u'x在大转盘中抽奖，获得了xxx奖品，邀请您一起参加抽奖',
            'image': '/images/feed/land_harvest_feed.jpg',
        }
    """
    from farm_lib.logics import common_config
    if method not in common_config.feed_send:
        return None

    feed_template = copy.deepcopy(common_config.feed_send.get(method, {}))

    # 当key(title)不存在时，默认返回 ${none_title}
    # 在template替换(title_template.substitute)时抛出KeyError异常，返回None
    title = feed_template.get('title', '${none_title}')

    title_template = string.Template(title)

    data = {'self': self_name}

    if friend_name is not None:
        data['friend'] = friend_name

    if message is not None:
        data['message'] = message

    if url_params is None:
        url_params = {}

    feed_data = {}

    try:
       feed_data['title'] = title_template.substitute(data)
    except KeyError:
        print_err()
        return None

    # pc_url, mb_url
    if url_params is not None and isinstance(url_params, dict) \
        and 'pc_url' in feed_template and 'mb_url' in feed_template:
        pc_params = copy.deepcopy(url_params)
        if not pc_params.get('method') and feed_template.get('method'):
            pc_params["method"] = feed_template.get('method','')
        #判断是否需要PC的业务处理
        if not feed_template.get('pc_url'):
            pc_params = {}
        url_params["ft"] = method
        #手机版url因参数长度变更修正
        mb_str = ''
        for item in url_params.items():
            mb_str += item[0]
            mb_str += ':'
            mb_str += item[1]
            mb_str += '$$'
        mb_str = mb_str[:-2]
        url_params = {'para':mb_str}

        pc_params["ft"] = method
        pc_url_params = json.dumps(pc_params)

        data['pc_url_params'] = urllib.quote(pc_url_params)
        data['mobile_url_params'] = urllib.quote(urllib.urlencode(url_params))

        pc_url = 'http://mixi.jp/run_appli.pl?id=%s&appParams=${pc_url_params}' % (settings.APP_ID)
        pc_url_template = string.Template(pc_url)

        temp_url = settings.BASEURL + '/m/common_feed_click/?'
        mb_url = 'http://ma.mixi.net/%s/?url=%s${mobile_url_params}' % (settings.APP_ID,urllib.quote(temp_url))
        mb_url_template = string.Template(mb_url)

        try:
            feed_data['pc_url'] = pc_url_template.substitute(data)
            feed_data['mb_url'] = mb_url_template.substitute(data)
        except KeyError:
            print_err()
            return None

    if 'image' in feed_template:
        feed_data['image'] = feed_template.get('image')

    if 'priority' in feed_template:
        feed_data['priority'] = feed_template.get('priority')

    feed_data['opt_callback'] = feed_template.get('opt_callback',{})
    feed_data['opt_callback']['ft'] = method

    return feed_data

def operate_feed_template_handler(method, self_name, friend_name=None, params=None, message=None,
                          url_params=None):
    """操作类feed模板处理器

    将feed模板中配置的${self}, ${friend}, ${message}替换为实际需要的内容

    Args:
        method: 需要发送feed动作，如land.seed等
        self_name: 当前登录用户名称
        friend_name: 交互好友名称
        message: 动态的提示信息，如获得了某某种子等
        url_params: feed url参数，字典类型。约定：key为参数名，字符串类型；value为参数值，字符串类型

    Returns:
        返回处理后的feed信息，类型为字典。如：
        {
            'title': 'x在大转盘中抽奖，获得了xxx奖品，邀请您一起参加抽奖',
            'image': '/images/feed/land_harvest_feed.jpg',
        }
    """
    scene_type = params.get('scene_type', 'farm')
    if scene_type == 'farm':
        good_type = params.get('crop_type')
    else:
        good_type = params.get('type')

    from farm_lib.logics import common_config
    if method not in common_config.feed_send:
        return None

    good_feed_config = common_config.feed_send[method].get(good_type, None)
    if good_feed_config is None:
        return None
    feed_template = copy.deepcopy(good_feed_config)

    # 当key(title)不存在时，默认返回 ${none_title}
    # 在template替换(title_template.substitute)时抛出KeyError异常，返回None
    title = feed_template.get('title', '${none_title}')
    title_template = string.Template(title)

    data = {'self': self_name}

    if friend_name is not None:
        data['friend'] = friend_name

    if message is not None:
        data['message'] = message

    if url_params is None:
        url_params = {}

    feed_data = {}

    try:
        feed_data['title'] = title_template.substitute(data)
    except KeyError:
        print_err()
        return None

    # pc_url, mb_url
    if url_params is not None and isinstance(url_params, dict) \
        and 'pc_url' in feed_template and 'mb_url' in feed_template:
        mb_params = copy.deepcopy(url_params)
        if not feed_template.get('mb_url').strip():
            mb_params = {}
        url_params["ft"] = method
        mb_params["ft"] = method
        #因手机版feed参数长度变更修正
        mb_str = ''
        for item in mb_params.items():
            mb_str += item[0]
            mb_str += ':'
            mb_str += item[1]
            mb_str += '$$'
        mb_str = mb_str[:-2]
        mb_params = {'para':mb_str}

        if not url_params.get("method"):
            url_params["method"] = feed_template.get('method','')
        pc_url_params = json.dumps(url_params)

        data['pc_url_params'] = urllib.quote(pc_url_params)
        data['mobile_url_params'] = urllib.quote(urllib.urlencode(mb_params))

        pc_url = 'http://mixi.jp/run_appli.pl?id=%s&appParams=${pc_url_params}' % (settings.APP_ID)
        pc_url_template = string.Template(pc_url)

        temp_url = settings.MOBILE_BASEURL + '/m/common_feed_click/?'
        mb_url = 'http://ma.mixi.net/%s/?url=%s${mobile_url_params}' % (settings.APP_ID,urllib.quote(temp_url))
        mb_url_template = string.Template(mb_url)

        try:
            feed_data['pc_url'] = pc_url_template.substitute(data)
            feed_data['mb_url'] = mb_url_template.substitute(data)
        except KeyError:
            print_err()
            return None

    if 'image' in feed_template:
        feed_data['image'] = feed_template.get('image')

    if 'priority' in feed_template:
        feed_data['priority'] = feed_template.get('priority')

    feed_data['opt_callback'] = feed_template.get('opt_callback',{})
    feed_data['opt_callback']['ft'] = method

    return feed_data

def debug_output(func):
    """#{{{ debug_output: 装饰器，将函数用try:...except:print_err()括起
                起到在测试服务器上时能讲错误打印到rekoo.err的作用
    args:
        func:    ---    arg
    returns:
        0    ---
    """
    def debug(*args, **kwargs):
        if settings.DEBUG:
            try:
                return func(*args, **kwargs)
            except:
                print_err()
        else:
            return func(*args, **kwargs)
    return debug
    #}}}

def float_calc(s):
    """#{{{ float_cal: 对浮点数进行靠谱计算
    args:
        s:    ---    arg
    returns:
        0    ---
    """
    for i in ['+','-','*','/']:
        s = s.replace(i, '))'+i+'decimal.Decimal(str(')
    s = 'float(decimal.Decimal(str('+s+')))'
    return s
    #}}}


def send_udp(server, data, is_dumped=True):
    udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if is_dumped:
        data = pickle.dumps(data)
    udp_client.sendto(data, server)

def _parse_backend_uri(backend_uri):
    """
    Converts the "backend_uri" into a cache scheme ('db', 'memcached', etc), a
    host and any extra params that are required for the backend. Returns a
    (scheme, host, params) tuple.
    """
    if backend_uri.find(':') == -1:
        raise Error, "Backend URI must start with scheme://"
    scheme, rest = backend_uri.split(':', 1)
    if not rest.startswith('//'):
        raise Error, "Backend URI must start with scheme://"

    host = rest[2:]
    qpos = rest.find('?')
    if qpos != -1:
        params = dict(parse_qsl(rest[qpos+1:]))
        host = rest[2:qpos]
    else:
        params = {}
    if host.endswith('/'):
        host = host[:-1]

    return scheme, host, params