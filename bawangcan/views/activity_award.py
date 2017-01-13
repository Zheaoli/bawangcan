# encoding: utf-8
"""
@version: ??
@author: lizheao
@contact: lizheao940510@gmail.com
@software: PyCharm
@file: activity_award.py
@time: 21:50
"""
import json

from django.http import HttpResponse
from django.http import request as request1
from django.views.decorators.csrf import csrf_exempt

from bawangcan.models import BawangcanAward
from bawangcan.utils.Others import RequestCheck


@csrf_exempt
@RequestCheck.check_key('user_id')
@RequestCheck.sql_check
def activity(request: request1):
    body_temp = json.loads(bytes.decode(request.body))
    try:
        result_temp = []
        for p in BawangcanAward.objects.raw(
                "select a.award_user_id,a.award_time,a.award_activity_id,b.activity_id,b.activity_type "
                "from bawangcan_bawangcanaward as a left OUTER JOIN bawangcan_bawangcanactivity as b "
                "where a.award_user_id = '{}' and a.award_activity_id=b.activity_id".format(
                    body_temp['user_id'])):
            temp_dict = {'award_time': p.award_time, 'award_type': p.activity_type}
            result_temp.append(temp_dict)
        return HttpResponse(json.dumps({'code': 0000, 'msg': '查询成功', 'data': result_temp}))
    except Exception as e:
        return HttpResponse(json.dumps({'code': 1001, 'msg': '查询失败'}))
