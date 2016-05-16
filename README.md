## 程序说明
本程序通过requests模块结合lxml模块，抓取天涯中带有博客的帐号信息、博客信息
及该id的关注情况、粉丝情况、文章情况和文章评论情况

## 文件说明
+ main.py  程序入口
+ DBopt.py 数据库操作类
+ x.conf 配置文件
+ README.md 自述文件

## 数据库设计说明

### 博主信息    TABLE (userInfo) PK id
+ 博主id   uid
+ 博主姓名  usnam
+ 博主地址  usurl
+ 粉丝数量  usfan
+ 关注数量  usfol
+ 登录次数  uslon
+ 最新登录  uslal
+ 注册时间  usreg
### 博客信息    TABLE (blogInfo) PK id
+ 博主id   uid
+ 博客名称  bonam
+ 博客地址  bourl
+ 博客签名  bosig
+ 总访问量  bovis
+ 开博时间  botim
+ 博文数量  bonum
### 博文信息    TABLE (textInfo) PK id
+ 博主id    uid
+ 博文ID    tid
+ 博文标题  txtit
+ 博文地址  txurl
+ 博文时间  txtim
+ 博文内容  txcon
### 评论信息    TABLE (commInfo) PK id
+ 博主id      uid
+ 评论人      cousr
+ 评论内容    cocon
+ 评论文章    cotex
+ 评论文章url courl
+ 评论人博客  coblg
+ 评论时间    cotim
### 粉丝列表    TABLE (fansInfo) PK id
+ 博主id   uid
+ 粉丝ID   aid
+ 粉丝姓名  fanam
+ 粉丝地址  faurl
### 关注列表    TABLE (follInfo) PK id
+ 博主id    uid
+ 关注id    fid
+ 关注姓名  fonam
+ 关注地址  fourl

## 程序算法设计说明
### 简单流程:
    1.遍历博主信息
    2.是否开有博客
    3.抓取博客信息
    4.抓取博文信息
    5.抓取评论信息
    6.抓取粉丝信息
    7.抓取关注信息

## 函数/方法说明

### getuser
    用于创建线程，传送博主URL给getuserinfo
### getuserinfo
    判断用户是否存在;
    判断该用户是否存在博客;
    抓取用户的信息;
    创建线程抓取博客(getblog);
    创建线程抓取粉丝(getfans)和关注(getfoll);
### getfans
    构造参数提交粉丝查询;
    解析提交返回结果;
    分析粉丝数量;
### getfansinfo
    获取粉丝情况;
    进一步交给gfx处理
### gfx
    构造SQL存入数据库
    
### getfoll
    构造参数提交关注查询;
    解析提交返回结果;
    分析关注数量;
### getfollinfo
    获取关注情况;
    进一步交给gfi处理
### gfi
    构造SQL存入数据库
    
    
### getblog
    解析博客页面
    获取博客信息并存入数据库
    调用gettext获取文章信息

    
### gettext
    获取文章URL地址列表
    数据交给gettextinfo处理
### gettextinfo
    解析URL地址列表
    数据交给gettextcontent处理
### gettextcontent
    处理地址，获取文章信息
    文章情况存入数据库
    评论部分交给getcomm处理
    
### getcomm
    处理评论部分内容
    数据存入数据库
    

## 错误情况说明(Warning不计)
### MySQLdb SQL execute error
    级别:错误
    频率:中等
    说明:SQL执行错误
    出现:有SQL语句的语句
    影响:中等
    原因:文章或者标题中出现分号（'），导致SQL语句插入错误。
    结果:无法保存数据
 
### Max retries exceeded with url
    级别:错误
    频率:中等
    说明:URL连接错误
    出现:有发起请求的语句
    影响:中等
    原因:程序并发中requests出现的bug
    结果:无法获取请求结果

### IndexError: list index out of range
    级别:错误
    频率:极低
    说明:列表引索超出列表范围
    出现:有xpath方法的语句
    影响:低等
    原因:博客不存在的一些信息(如签名)，导致xpath抓取无返回结果
    结果:无影响
    
### ConnectionError: ('Connection aborted.', error(10054, ''))
    级别:错误
    频率:极低
    说明:连接被终止
    出现:有发起请求的语句
    影响:低等
    原因:天涯反爬机制或者是网络问题
    结果:无法获取请求结果
    
### KeyError: 'user'
    级别:错误
    频率:极低
    说明:无user值
    出现:粉丝抓取或者关注抓取方法
    影响:低等
    原因:POST参数构造有变化
    结果:无法获取粉丝或者关注json的情况(一次)

## 测试环境
+ 平台：windows 8(64)
+ Python：2.7.10
+ 编辑器：Pycharm
+ 编码： UTF-8
+ MYSQL：5.5.40-0+wheezy1
## 测试结果
+ 用时:5小时10分
+ 范围(uid)：1130-50306
+ 错误数: SQL execute error(165),ConnectionError(49),KeyError(11)，IndexError(7)
+ 数据量：108.0MB
    bloginfo:64.0KB
    comminfo:27.5MB
    fansinfo:6.5MB
    follinfo:256.0KB
    textinfo:73.6MB
    userinfo:48.0KB
+ 进程情况：MAX=10











    
    
    
    
