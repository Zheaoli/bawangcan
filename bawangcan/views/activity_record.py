# encoding: utf-8
"""
@version: ??
@author: lizheao
@contact: lizheao940510@gmail.com
@software: PyCharm
@file: activity_record.py
@time: 16:39
"""
import json

from django.db import connection
from django.http import HttpResponse
from django.http import request as request1
from django.views.decorators.csrf import csrf_exempt

from bawangcan.utils.DataBase import NamedTupleFetch
from bawangcan.utils.Others import RequestCheck


@csrf_exempt
@RequestCheck.check_key('activity_id')
@RequestCheck.sql_check
def activity(request: request1):
    body_temp = json.loads(bytes.decode(request.body))
    try:
        templist = []
        with connection.cursor() as cursor:
            cursor.execute("select MAX(activity_time),activity_id,activity_type from bawangcan_bawangcanactivity"
                           " where activity_type={} ORDER BY activity_time LIMIT 1".format(
                body_temp['activity_id']))
            activity_object = NamedTupleFetch.namedtuplefetchone(cursor=cursor)
            if activity_object is not None:
                cursor.execute("select * from bawangcan_bawangcanrecord where record_activity_id='{}'".format(
                    activity_object.activity_id))
                temp_result = NamedTupleFetch.namedtuplefetchall(cursor=cursor)
                for p in temp_result:
                    tempdict = {'join_time': p.record_create_time, 'user': p.record_user_id}
                    templist.append(tempdict)
        return HttpResponse(json.dumps({'code': 0000, 'msg': '成功', 'data': templist}))
    except Exception as e:
        return HttpResponse(json.dumps({'code': 1001, 'msg': '请求失败，请重新获取'}))
