# encoding: utf-8
"""
@version: ??
@author: lizheao
@contact: lizheao940510@gmail.com
@software: PyCharm
@file: RequestCheck.py
@time: 21:18
"""
#                       _oo0oo_
#                      o8888888o
#                      88" . "88
#                      (| -_- |)
#                      0\  =  /0
#                    ___/`---'\___
#                  .' \\|     |// '.
#                 / \\|||  :  |||// \
#                / _||||| -:- |||||- \
#               |   | \\\  -  /// |   |
#               | \_|  ''\---/''  |_/ |
#               \  .-\__  '-'  ___/-. /
#             ___'. .'  /--.--\  `. .'___
#          ."" '<  `.___\_<|>_/___.' >' "".
#         | | :  `- \`.;`\ _ /`;.`/ - ` : | |
#         \  \ `_.   \_ __\ /__ _/   .-` /  /
#     =====`-.____`.___ \_____/___.-`___.-'=====
#                       `=---='
#
#
#     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#               佛祖保佑         永无BUG
from bawangcan.utils.DataBase import RedisBase
from conf.MyRedis import *
from functools import wraps
from django.http import HttpResponse
import json
from django.http import request as request1


def check_key(f):
    @wraps(f)
    def wrap(request: request1, *args, **kwargs):
        re = {}
        if request.method == "POST":
            temp_dict = json.loads(bytes.decode(request.body))
            if 'key' in temp_dict and 'user_id' in temp_dict:
                redis_client = RedisBase.RedisBase(host=host, port=port, database=db)
                temp_check = redis_client.connection.get(temp_dict['email'].strip())
                if temp_check is None:
                    re['code'] = 56789
                    re['msg'] = 'key已经失效，请重新登陆'
                    return HttpResponse(json.dumps(re), content_type="application/json")
                elif temp_dict['key'] == bytes.decode(temp_check):
                    return f(request, *args, **kwargs)
            else:
                re['code'] = 12345
                re['msg'] = '请带上 email 和 user_id'
                return HttpResponse(json.dumps(re), content_type="application/json")

        else:
            re['code'] = 23333
            re['msg'] = "哎呀呀呀，请用 POST"
            return HttpResponse(json.dumps(re), content_type="application/json")

    return wrap


def sql_check(func):
    @wraps(func)
    def wrap(request: request1, *args, **kwargs):
        func(request1, *args, **kwargs)

    return wrap
