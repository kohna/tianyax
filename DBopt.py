# -*- coding: UTF-8     -*-
# -*- author: kohna     -*-
# -*- date  : 2016-3-1 -*-
# -*- time  : 11:32     -*-

import MySQLdb


class DBopt:
    def __init__(self, dbname):
        try:
            self.conn = MySQLdb.connect(
                host="192.168.1.108",  # 数据库地址
                port=3306,  # 数据库端口
                user="root",  # 数据库用户
                passwd="11.",  # 数据库密码
                db=dbname,  # 数据库名
                charset="utf8")  # 数据库编码
        except MySQLdb.Error, e:
            print "MySQLdb connect error by %s " % e
            return

        self.cur = self.conn.cursor()  # 获取数据库指针
        self.sql = ''

    def sqlexe(self):
        try:
            self.cur.execute(self.sql)  # 执行SQL
            self.conn.commit()  # 提交操作
        except MySQLdb.Error, e:
            print "MySQLdb SQL execute error by %s " % e
        return 0

    def dbclose(self):
        self.conn.close()  # 关闭数据库
