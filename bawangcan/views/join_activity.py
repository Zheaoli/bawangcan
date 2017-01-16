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

from django.db import connection
from django.http import HttpResponse
from django.http import request as request1
from django.views.decorators.csrf import csrf_exempt

from bawangcan.models import BawangcanStatus
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
    with connection.cursor() as cursor:
        try:
            cursor.execute("set autocommit=0")
            cursor.execute("Begin Transaction")
            user_object = None
            temp_flag = cursor.execute(
                "update bawangcan_user set user_money=user_money-1 where user_id={} and user_money > 1".format(user_id))
            if temp_flag == 0:
                raise ValueError("余额错误")
            activity_flag = None
            if body_temp['activity_id'] == 0:
                for p in BawangcanStatus.objects.raw(
                        "SELECT * FROM bawangcan_bawangcanstatus"
                        " WHERE status_type=0 AND status_count<20 AND status_status=0 FOR UPDATE "):
                    activity_flag = p
            else:
                for p in BawangcanStatus.objects.raw(
                        "SELECT * FROM bawangcan_bawangcanstatus "
                        "WHERE status_type=1 AND status_count<200 AND status_status=0 FOR UPDATE "):
                    activity_flag = p
            if activity_flag is None:
                activity_id_hash = hashlib.sha1()
                activity_id_hash.update(str.encode("{}_{}".format(user_object.user_id, str(
                    ConvertTime.str_to_num(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))))))
                time_map = ConvertTime.str_to_num(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                cursor.execute("insert into bawangcan_bawangcanactivity (activity_time,activity_type,"
                               "activity_id) values({},{},{})".format(time_map,
                                                                      body_temp['activity_type'],
                                                                      activity_id_hash.hexdigest()))
                cursor.execute(
                    "insert into bawangcan_bawangcanstatus (status_activity_id,status_start_time,"
                    "status_count,status_status,status_type) values({}.{}.{}.{}.{})".format(
                        activity_id_hash.hexdigest(), time_map, 1, 0, body_temp['activity_type']))
                cursor.execute(
                    "insert into bawangcan_bawangcanrecord (record_activity_id,"
                    "record_create_time,record_user_id) VALUES ({},{},{})".format(
                        activity_id_hash.hexdigest(), time_map, body_temp['user_id']))
            else:
                time_map = ConvertTime.str_to_num(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                if body_temp['activity_id'] == 1 and (activity_flag.status_count + 1) == 200:
                    cursor.execute("update set status_end_time={},status_count=200,status_status=1 where "
                                   "status_activity_id=".format(time_map))
                elif body_temp['activity_id'] == 0 and (activity_flag.status_count + 1) == 20:
                    cursor.execute("update set status_end_time={},status_count=200,status_status=1 where "
                                   "status_activity_id=".format(time_map))
                else:
                    cursor.execute("update set status_count={} where "
                                   "status_activity_id=".format(activity_flag.status_count + 1))
                cursor.execute(
                    "insert into bawangcan_bawangcanrecord (record_activity_id,record_create_time,record_user_id)"
                    " VALUES({},{},{})".format(
                        activity_flag.activity_id, time_map, body_temp['user_id']))
        except Exception as e:
            cursor.execute("ROLLBACK Transaction")
            return HttpResponse(json.dumps({'code': 1001, 'msg': '活动参加失败'}))
        else:
            cursor.execute('Commit Transaction')
            return HttpResponse(json.dumps({'code': 0000, 'msg': '成功'}))
        finally:
            cursor.execute("set autocommit=1")
