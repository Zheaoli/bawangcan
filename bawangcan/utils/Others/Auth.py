# encoding: utf-8
"""
@version: ??
@author: lizheao
@contact: lizheao940510@gmail.com
@software: PyCharm
@file: Auth.py
@time: 21:05
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
from bawangcan.models import User
from bawangcan.utils.DataBase import RedisBase
import hashlib
from conf.MyRedis import *
from .ConvertTime import str_to_num
import datetime


class UserAuth(object):
    @staticmethod
    def auth(user: dict):
        try:
            usertable = User.objects.get(user_email=user['email'])
        except:
            return 10302, '用户不存在'
        pwd = hashlib.md5()
        pwd.update(str.encode("{}_{}_{}".format(user['name'], user['email'], user['password'])))
        if usertable.user_password == pwd.hexdigest():
            key_client = hashlib.md5()
            key_client.update(str.encode('{}_{}'.format(usertable.user_id, str(
                str_to_num(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))))))
            redis_client = RedisBase.RedisBase(database=db, host=host, port=port)
            redis_client.connection.set(usertable.user_id, key_client.hexdigest())
            redis_client.connection.expire(time=10000, name=usertable.user_id)
            return 0000, key_client.hexdigest(), usertable.user_id
        else:
            return 10303, '密码错误',None
