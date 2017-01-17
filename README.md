## 饿了么霸王餐模拟

这道题是 v2ex 上看到的一个饿了么的[面试题](https://www.v2ex.com/t/333691)。我试了试

目前将其抽象为这样几个端口

第一 user_login 用户登录

第二 join_activity 用户参与霸王餐活动

第三 heart_beat 定时更新key

第四 activity_record 获取当前活动状态

第五 activity_award 获取用户中奖状态

## 缺陷

第一，数据库设计直接暴力出奇迹=。=没有考虑更多因素

第二，暂时没有考虑分布式数据库中的事务处理

第三，没有良好的缓存层设计，频繁对数据库操作

第四，没有设计日志系统

第五，join_activity 没有编写单元测试（实际上是我不知道在带事务的情况下，单元测试怎样去构造 Test Case）

## 说明

/api/user_login/
~~~Json
{
  "user_email":"625926979@qq.com",//用户邮箱
  "password":"f8d6934a93cb488588067fe165203d32",//用户密码 md5 值
  "user_name":"lizheao",// 用户名
  "time_map":123456789 //unix时间戳
}
~~~
返回
~~~Json
{
  "user_id":用户编号
  "key":"f8d6934a93cb488588067fe165203d32",
  "code":"lizheao",// 状态码
  "msg":123456789 // 额外消息
}
~~~

/api/join_activity/
~~~Json
{
	"key": "47563fdd1a50db6af6004dc2d28116eb",//之前下发的key
	"user_id": "abcsafdsasdfas",//下发的用户id
	"activity_type": 0, //参与的活动类型
	"time_map": 12345, //时间戳
	"email": "625926979@qq.com"//邮箱
	
}
~~~
返回
~~~Json
{
  "code":,// 状态码
  "msg" // 额外消息
}
~~~