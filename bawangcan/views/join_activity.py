# encoding: utf-8
"""
@version: ??
@author: lizheao
@contact: lizheao940510@gmail.com
@software: PyCharm
@file: join_activity.py
@time: 11:08
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
from django.http import HttpResponse
from django.http import request as request1
from django.views.decorators.csrf import csrf_exempt
from bawangcan.models import User
from bawangcan.models import BawangcanActivity
from bawangcan.models import BawangcanStatus
from bawangcan.models import BawangcanRecord
from bawangcan.utils.Others import RequestCheck
from bawangcan.utils.Others import ConvertTime
import datetime
import hashlib


@csrf_exempt
@RequestCheck.check_key
@RequestCheck.sql_check
def join_activity(request: request1):
    user_id = request.body['user_id']
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
                                                                                 request.body['activity_type'],
                                                                                 activity_id_hash.hexdigest()))
            BawangcanStatus.objects.raw(
                "insert into bawangcan_bawangcanstatus (status_activity_id,status_start_time,"
                "status_count,status_status,status_type) values({}.{}.{}.{}.{})".format(
                    activity_id_hash.hexdigest(), time_map, 1, 0, request.body['activity_type']))
            BawangcanRecord.objects.raw(
                "insert into bawangcan_bawangcanrecord (record_activity_id,"
                "record_create_time,record_user_id) VALUES ({},{},{})".format(
                    activity_id_hash.hexdigest(), time_map, request.body['user_id']))
        else:
            time_map = ConvertTime.str_to_num(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            if request.body['activity_id'] == 1 and (activity_object.status_count + 1) == 200:
                BawangcanStatus.objects.raw("update set status_time={},set status_count=200,status_status=1 where "
                                            "status_activity_id=".format(time_map))
            elif request.body['activity_id'] == 0 and (activity_object.status_count + 1) == 20:
                BawangcanStatus.objects.raw("update set status_time={},set status_count=200,status_status=1 where "
                                            "status_activity_id=".format(time_map))
            else:
                BawangcanStatus.objects.raw("update set status_count={} where "
                                            "status_activity_id=".format(activity_object.status_count + 1))
            BawangcanRecord.objects.raw(
                "insert into bawangcan_bawangcanrecord (record_activity_id,record_create_time,record_user_id)"
                " VALUES({},{},{})".format(
                    activity_object.activity_id, time_map, request.body['user_id']))
        User.objects.raw(
            'update bawangcan_user set user_money={} where user_id={}'.format(user_money, request.body['user_id']))
    except Exception as e:
        pass
    else:
        User.objects.raw('Commit Transaction')
        return