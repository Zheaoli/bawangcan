# encoding: utf-8
"""
@version: ??
@author: lizheao
@contact: lizheao940510@gmail.com
@software: PyCharm
@file: user_login.py
@time: 11:02
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
from bawangcan.utils.Others import Auth
import json


@csrf_exempt
def user_login(request: request1):
    re = {'code': 9999}
    if request.method == "POST":
        try:
            body_temp = json.loads(bytes.decode(request.body))
            user_email = body_temp['user_email'].strip()
            password = body_temp['password'].strip()
            user_name = body_temp['user_name'].strip()
            time_map = body_temp['time_map']
            if not '@' in user_email and user_name != 'admin':
                raise ValueError("User Name Error")
            if 'HTTP_X_FORWARDED_FOR' in request.META:
                ip = request.META['HTTP_X_FORWARDED_FOR']
            else:
                ip = request.META['REMOTE_ADDR']
        except ValueError as e:
            re['msg'] = '' + str(e)
            return HttpResponse(json.dumps(re), content_type="application/json")
        try:
            code, result, user_id = Auth.UserAuth.auth(
                dict(name=user_name, email=user_email, password=password, timemap=time_map))
            re['code'] = code
            if code == 0000:
                re['msg'] = "登陆成功"
                re['key'] = result
                re['user_id'] = user_id
            else:
                re['msg'] = result
                re['key'] = None
                re['user_id'] = None
            return HttpResponse(json.dumps(re), content_type='application/json')
        except Exception as e:
            print(e)
    else:
        re['code'] = 23333
        re['msg'] = '白痴，用POST'
        re['key'] = None
        return HttpResponse(json.dumps(re), content_type='application/json')
