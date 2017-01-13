# encoding: utf-8
"""
@version: ??
@author: lizheao
@contact: lizheao940510@gmail.com
@software: PyCharm
@file: join_activity.py
@time: 11:08
"""
import datetime
import hashlib
import json

from django.http import HttpResponse
from django.http import request as request1
from django.views.decorators.csrf import csrf_exempt

from bawangcan.models import BawangcanActivity
from bawangcan.models import BawangcanRecord
from bawangcan.models import BawangcanStatus
from bawangcan.models import User
from bawangcan.utils.Others import ConvertTime
from bawangcan.utils.Others import RequestCheck


@csrf_exempt
@RequestCheck.check_key('user_id')
@RequestCheck.sql_check
def join_activity(request: request1):
    """

    :param request:
    :return:
    """
    body_temp = json.loads(bytes.decode(request.body))
    user_id = body_temp['user_id']
    try:
        User.objects.raw("set autocommit=0")
        User.objects.raw("Begin Transaction")
        user_object = None
        for j in User.objects.raw("select * from bawangcan_user where user_id={}".format(user_id)):
            user_object = j
        user_money = user_object.user_money - 1
        activity_object = None
        for p in BawangcanStatus.objects.raw(
                "SELECT * FROM bawangcan_bawangcanstatus WHERE status_type=0 AND status_count<20 AND status_status=0"):
            activity_object = p
        if activity_object is None:
            activity_id_hash = hashlib.sha1()
            activity_id_hash.update(str.encode("{}_{}".format(user_object.user_id, str(
                ConvertTime.str_to_num(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))))))
            time_map = ConvertTime.str_to_num(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            BawangcanActivity.objects.raw("insert into bawangcan_bawangcanactivity (activity_time,activity_type,"
                                          "activity_id) values({},{},{})".format(time_map,
                                                                                 body_temp['activity_type'],
                                                                                 activity_id_hash.hexdigest()))
            BawangcanStatus.objects.raw(
                "insert into bawangcan_bawangcanstatus (status_activity_id,status_start_time,"
                "status_count,status_status,status_type) values({}.{}.{}.{}.{})".format(
                    activity_id_hash.hexdigest(), time_map, 1, 0, body_temp['activity_type']))
            BawangcanRecord.objects.raw(
                "insert into bawangcan_bawangcanrecord (record_activity_id,"
                "record_create_time,record_user_id) VALUES ({},{},{})".format(
                    activity_id_hash.hexdigest(), time_map, body_temp['user_id']))
        else:
            time_map = ConvertTime.str_to_num(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            if body_temp['activity_id'] == 1 and (activity_object.status_count + 1) == 200:
                BawangcanStatus.objects.raw("update set status_end_time={},status_count=200,status_status=1 where "
                                            "status_activity_id=".format(time_map))
            elif body_temp['activity_id'] == 0 and (activity_object.status_count + 1) == 20:
                BawangcanStatus.objects.raw("update set status_end_time={},status_count=200,status_status=1 where "
                                            "status_activity_id=".format(time_map))
            else:
                BawangcanStatus.objects.raw("update set status_count={} where "
                                            "status_activity_id=".format(activity_object.status_count + 1))
            BawangcanRecord.objects.raw(
                "insert into bawangcan_bawangcanrecord (record_activity_id,record_create_time,record_user_id)"
                " VALUES({},{},{})".format(
                    activity_object.activity_id, time_map, body_temp['user_id']))
        User.objects.raw(
            'update bawangcan_user set user_money={} where user_id={}'.format(user_money, body_temp['user_id']))
    except Exception as e:
        User.objects.raw("ROLLBACK Transaction")
        return HttpResponse(json.dumps({'code': 1001, 'msg': '活动参加失败'}))
    else:
        User.objects.raw('Commit Transaction')
        return HttpResponse(json.dumps({'code': 0000, 'msg': '成功'}))
    finally:
        User.objects.raw("set autocommit=1")
