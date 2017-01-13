## 饿了么霸王餐模拟

这道题是 v2ex 上看到的一个饿了么的面试题。我试了试

目前将其抽象为这样几个端口

第一 user_login 用户登录

第二 join_activity 用户参与霸王餐活动

第三 heart_beat 定时更新key

第四 activity_record 获取当前活动状态

第五 activity_record 获取用户中奖状态

## 缺陷

第一，数据库设计直接暴力出奇迹=。=没有考虑更多因素

第二，暂时没有考虑分布式数据库中的事务处理

第三，没有良好的缓存层设计，频繁对数据库操作

第四，没有设计日志系统

第五，join_activity 没有编写单元测试（实际上是我不知道在带事物的情况下，单元测试怎样去构造 Test Case）