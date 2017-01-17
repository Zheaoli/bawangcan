# encoding: utf-8
"""
@version: ??
@author: lizheao
@contact: lizheao940510@gmail.com
@software: PyCharm
@file: urls.py
@time: 11:00
"""
from django.conf.urls import url

from .views import activity_record
from .views import heart_beat
from .views import join_activity
from .views import user_login

urlpatterns = [
    url(r'^join_activity/', join_activity.join_activity),
    url(r'^heart_beat/', heart_beat.heart_beat),
    url(r'^activity_record/', activity_record.activity),
    url(r'^login/', user_login.user_login)
]
