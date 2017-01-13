# encoding: utf-8
"""
@version: ??
@author: lizheao
@contact: lizheao940510@gmail.com
@software: PyCharm
@file: heart_beat.py
@time: 16:11
"""

import datetime
import hashlib
import json

from django.http import HttpResponse
from django.http import request as request1
from django.views.decorators.csrf import csrf_exempt

from bawangcan.utils.DataBase import RedisBase
from bawangcan.utils.Others import ConvertTime
from bawangcan.utils.Others import RequestCheck
from conf.MyRedis import *


@csrf_exempt
@RequestCheck.check_key('user_id')
def heart_beat(request: request1):
    body_temp = json.dumps(request.body)
    key_client = hashlib.md5()
    key_client.update(str.encode('{}_{}'.format(body_temp['user_id'], str(
        ConvertTime.str_to_num(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))))))
    redis_client = RedisBase.RedisBase(database=db, host=host, port=port)
    redis_client.connection.set(body_temp['user_id'], key_client.hexdigest())
    redis_client.connection.expire(body_temp['user_id'], 16000)
    return HttpResponse(json.dumps({"code": 0000, "key": key_client.hexdigest(), "msg": "请求成功"}),
                        content_type="application/json")
