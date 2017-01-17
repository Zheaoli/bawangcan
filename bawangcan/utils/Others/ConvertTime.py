# encoding: utf-8
"""
@version: ??
@author: lizheao
@contact: lizheao940510@gmail.com
@software: PyCharm
@file: ConvertTime.py
@time: 21:10
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
import re
import time


def str_to_num(time_str: object) -> object:
    # type: (object) -> object
    try:
        if re.match("\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", time_str):
            num_time = time.strptime(time_str, '%Y-%m-%d %H:%M:%S')
            num = int(time.mktime(num_time) * 1000)
            return num
        else:
            print("%s is error code form !", time_str)
    except:
        # log.error("str_to_num convert error !")
        return ""