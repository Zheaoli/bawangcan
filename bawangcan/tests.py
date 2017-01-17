import hashlib
import json

from django.test import Client
from django.test import TestCase
from django.test.client import RequestFactory

from bawangcan.views import join_activity
from bawangcan.views import user_login


# Create your tests here.
class UserLoginTest(TestCase):
    def test_none_user(self):
        pwd_has = hashlib.md5()
        pwd_has.update(str.encode("z14273550489"))
        factory = RequestFactory()
        c = Client()
        request = factory.post("/api/login/",
                               data=json.dumps({"user_email": "625926979@qq.com213", "user_name": "lizheao",
                                                "password": pwd_has.hexdigest(), "time_map": 12345}),
                               content_type="application/json")
        response = user_login.user_login(request)
        self.assertEqual(200, response.status_code)
        # self.assertEqual("application/json", response.content_type)
        self.assertEqual(str.encode(json.dumps({"code": 10302, "msg": "用户不存在"})), response.content)

    def test_password_error(self):
        pwd_has = hashlib.md5()
        pwd_has.update(str.encode("z14273550489"))
        factory = RequestFactory()
        request = factory.post("/api/login/", data=json.dumps({"user_email": "625926979@qq.com", "user_name": "lizheao",
                                                               "password": '12343', "time_map": 12345}),
                               content_type="application/json")
        response = user_login.user_login(request)
        self.assertEqual(200, response.status_code)
        self.assertEqual(10303, json.loads(bytes.decode(response.content))['code'])

    def test_login_success(self):
        pwd_has = hashlib.md5()
        pwd_has1 = hashlib.md5()
        pwd_has.update(str.encode("z14273550489"))
        pwd_has1.update(str.encode("{}_{}_{}".format("lizheao", "625926979@qq.com", pwd_has.hexdigest())))
        factory = RequestFactory()
        request = factory.post("/api/login/", data=json.dumps({"user_email": "625926979@qq.com", "user_name": "lizheao",
                                                               "password": pwd_has.hexdigest(), "time_map": 12345}),
                               content_type="application/json")
        response = user_login.user_login(request)
        self.assertEqual(200, response.status_code)
        self.assertEqual(0000, json.loads(bytes.decode(response.content))['code'])
        print(json.loads(bytes.decode(response.content))['key'], json.loads(bytes.decode(response.content))['user_id'])


        # b68025aa098828f60142525532a084c4


class JoinTest(TestCase):
    def test_join(self):
        pwd_has = hashlib.md5()
        pwd_has1 = hashlib.md5()
        pwd_has.update(str.encode("z14273550489"))
        pwd_has1.update(str.encode("{}_{}_{}".format("lizheao", "625926979@qq.com", pwd_has.hexdigest())))
        print("李者璈：{}".format(pwd_has1.hexdigest()))
        factory = RequestFactory()
        request = factory.post("/api/login/",
                               data=json.dumps({"key": "b68025aa098828f60142525532a084c4", "user_id": "abcsafdsasdfas",
                                                "activity_id": 0, "time_map": 12345, "email": "625926979@qq.com"}),
                               content_type="application/json")

        response = join_activity.join_activity(request)
        self.assertEqual(200, response.status_code)
        self.assertEqual(0000, json.loads(bytes.decode(response.content))['code'])
