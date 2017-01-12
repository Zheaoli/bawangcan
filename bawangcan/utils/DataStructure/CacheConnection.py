# encoding: utf-8
"""
@version: ??
@author: lizheao
@contact: lizheao940510@gmail.com
@software: PyCharm
@file: CacheConnection.py
@time: 21:00
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
import weakref


class CacheConnection(type):
    def __init__(self, cls, name, bases, dict):
        __getattribute__o = cls.__getattribute__

        def __getattribute__(self, *args, **kwargs):
            print('__getattribute__:', args, kwargs)
            return __getattribute__o(self, *args, **kwargs)

        cls.__getattribute__ = __getattribute__
        super().__init__(cls, name, bases, dict)
        self.__cache = weakref.WeakValueDictionary()

    def __call__(self, *args, **kwargs):
        if kwargs['database'] in self.__cache:
            return self.__cache[kwargs['database']]
        else:
            obj = super().__call__(*args, **kwargs)
            self.__cache[kwargs['database']] = obj
            return obj


class CacheConnectionInstance(type):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__cache = weakref.WeakValueDictionary()

    def __call__(self, *args, **kwargs):
        if kwargs['instance'] in self.__cache:
            return self.__cache[kwargs['instance']]
        else:
            obj = super().__call__(*args, **kwargs)
            self.__cache[kwargs['instance']] = obj
            return obj
