# -*- coding: UTF-8     -*-
# -*- author: kohna     -*-
# -*- date  : 2016-2-29 -*-
# -*- time  : 14:27     -*-

"""
    Get TianYa data.
    http://www.tianya.cn/
"""

import requests  # 导入模块
import ConfigParser
from lxml import html
from time import sleep
from DBopt import DBopt
from threading import Thread
from multiprocessing import Process

#   COMMON SET start
see = requests.session()    # 初始化 session对象
see.max_redirects = 500 #  设置最大重定向
hea = {"Connection": "keep-alive", "User-Agent": "TianYa-X Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
see.headers = hea   #  设置header
ulis0 = []      # 
ulis1 = []
ulis2 = []
ulis3 = []
udic = {"1": ulis0, "2": ulis1, "3": ulis2, "4": ulis3}   #  
HOSTX = "http://www.tianya.cn"    #  设置HOST
HOST = "http://www.tianya.cn/"
FANU = HOSTX + "/api/tw?"
DB = "tianyax"    #  设置数据库名


def getcomm(uid, com, cotex, url):  # 获取评论内容
    print "uid", uid, "Get comm info."
    db = DBopt(DB)      # 初始化数据库操作对象
    cell = com.xpath("//div[@class='articlecomments-cell']")        #  获取xpath值。“”内的内容是XPATH语句
    if len(cell):
        for ix in cell:
            cousr = ix.xpath("div/a[@class='replyName fb']/text()")[0]  # 回复人
            coblg = ix.xpath("div/a[@class='replyName fb']/@href")[0]  # 文章地址
            cocon = "".join(ix.xpath("div[@class='comments-content']//text()"))  # 回复内容
            cotim = ix.xpath("div/div/span/text()")[0]
            cousr = cousr.replace("'", "\'")
            cocon = cocon.replace("'", "\'")        # 处理引号
            db.sql = "INSERT INTO comminfo(uid,cousr,coblg,courl,cocon,cotex,cotim) VALUES (" + str(
                uid) + ",'" + cousr + "','" + coblg + "','" + url + "','" + cocon + "','" + cotex + "','" + cotim + "')"
            db.sqlexe()     # 执行SQL
        db.dbclose()    # 关闭数据库操作


def gettextcontent(uid, url):  # 获取文章内容
    print "uid:", uid, "Get text content"
    temp = see.get(url)     # GET 操作
    if temp.status_code == 404 or temp.status_code == 500:      # 剔除失败的页面
        return 0
    temp.close()    # 关闭连接
    xtem = html.document_fromstring(temp.content)       # 处理文档
    txtid = url.split("-")[1]   # 获取文章id
    txtit = ""
    txtim = ""
    try:
        txtit = xtem.xpath("//div[@class='article']/h2/a/text()")[0]  # 文章标题    
        txtim = xtem.xpath("//span[@class='pos-right gray6']/text()")[0]  # 时间
    except IndexError, e:
        pass
    txcon = xtem.xpath("//div[@class='article-summary articletext']//text()")  # 文章内容
    commi = xtem.xpath("//div[@class='articlecomments-list']")
    txcon = "".join(txcon)      # 把list转为str
    txcon = txcon.replace("'", "\'")
    db = DBopt(DB)
    db.sql = "INSERT INTO textinfo(uid,tid,txtit,txcon,txurl,txtim) VALUES (" + str(uid) + ",'" + str(txtid) + "','" + txtit + "','" + txcon + "','" + url + "','" + txtim + "')"
    db.sqlexe()
    db.dbclose()
    getcomm(uid, commi[0], txtit, url)  #  获取评论结果


def gettextinfo(uid, urls):  # 解析文章地址
    ulen = len(urls)        # 
    for num in xrange(ulen / 2):        #  分割URL
        url = urls[num]         
        gettextcontent(uid, url)        # 获取正序URL结果

        urx = urls[ulen - num - 1]      #  逆序URL
        gettextcontent(uid, urx)        #获取逆序URL结果


def gettext(uid, pages, url):  # 获取文章列表
    print "uid: ", uid, " Get text info"
    for page in xrange(1, pages + 1):       # 文章页面
        urx = url[:-7] + str(page) + ".shtml"       #生成URL
        temp = see.get(urx)
        if temp.status_code == 404 or temp.status_code == 500:  # 剔除失败的页面
            return 0
        temp.close()    
        xtem = html.document_fromstring(temp.content)       # 处理文档
        urls = xtem.xpath("//div[@class='article']/h2/a/@href")
        gettextinfo(uid, urls)      # 获取文章信息


def getblog(uid, url):  # 获取博客信息
    print "uid:", uid, "Get Blog info."
    temp = requests.get(url)
    if temp.status_code == 404 or temp.status_code == 500:
        return 0
    temp.close()
    xtem = html.document_fromstring(temp.content)
    bonam = ""  # 博客名字
    bosig = ""  # 博客签名，可能没有
    try:
        bonam = xtem.xpath("//h1/a/text()")[0]      # 获取博客名字
        bosig = xtem.xpath("//div[@class='blogsign']/text()")[0]    # 获取博客签名，一样是XPATH语句
    except IndexError, e:       # 捕获引索错误
        pass
    bovis = xtem.xpath("//em[@id='AllVisitCounter']/text()")[0] # 获取访问人数
    xtfts = xtem.xpath("//li[@class='statisticsItem']/text()")  
    bonum = xtem.xpath("//li[@class='current']/span/text()")[0][1:-1]   

    pages = int(bonum) / 18 + 1
    botim = xtfts[-2][5:]
    db = DBopt(DB)
    db.sql = "INSERT INTO bloginfo(uid,bonam,bourl,bosig,bovis,botim,bonum) VALUES (" + str(uid) + ",'" + bonam + "','" + url + "','" + bosig + "'," + str(bovis) + ",'" + botim + "'," + str(
        bonum) + ")"
    db.sqlexe()
    db.dbclose()
    pages = int(pages) + 1
    gettext(uid, pages, url)    #处理文章


def gfi(uid, url):      #处理关注人情况
    tem = see.get(url)
    if tem.status_code == 404 or tem.status_code == 500:
        return 0
    tem.close()
    xte = tem.json()
    uli = xte["data"]["user"]       # 处理JSON结果
    db = DBopt(DB)
    for ix in uli:
        fonm = ix["name"]   # 获取名字
        foid = ix["id"] #获取ID
        four = HOST + str(uid)      #生成URL 
        db.sql = "INSERT INTO follinfo(uid,fid,fonam,fourl) VALUES (" + str(uid) + "," + str(foid) + ",'" + fonm + "','" + four + "')"
        db.sqlexe()
        sleep(1)
    db.dbclose()


def getfollinfo(userid, total):
    if total % 28 > 0:
        pages = total / 28 + 2      # 处理页数
    else:
        pages = total / 28
    for num in xrange(1, pages / 2):
        pra = "method=following.ice.select&params.userId=" + userid + "&params.pageNo=" + str(num) + "&params.pageSize=28"  #生成POST的参数
        url = FANU + pra
        gfi(userid, url)

        nux = pages - num
        pra = "method=following.ice.select&params.userId=" + userid + "&params.pageNo=" + str(nux) + "&params.pageSize=28"
        url = FANU + pra
        gfi(userid, url)


def getfoll(uid):
    print "uid:", uid, "Get follow info"
    uid = str(uid)
    pram = "method=following.ice.select&params.userId=" + uid + "&params.pageNo=1&params.pageSize=28"
    folsu = FANU + pram   # 一样是参数
    temp = see.get(folsu)
    if temp.status_code == 404 or temp.status_code == 500:
        return 0
    temp.close()
    xtem = temp.json()
    total = xtem["data"]["total"]
    if total < 28:
        gfi(uid, folsu)
    else:
        getfollinfo(uid, total)


def gfx(uid, url):
    tem = see.get(url)
    if tem.status_code == 404 or tem.status_code == 500:
        return 0
    tem.close()
    xte = tem.json()
    uli = xte["data"]["user"]
    db = DBopt(DB)
    for ix in uli:
        fanm = ix["name"]
        faid = ix["id"]
        four = HOST + str(uid)
        db.sql = "INSERT INTO fansinfo(uid,aid,fanam,faurl) VALUES (" + str(uid) + "," + str(faid) + ",'" + fanm + "','" + four + "')"
        db.sqlexe()
        sleep(1)
    db.dbclose()


def getfansinfo(userid, total):
    if total % 28 > 0:
        pages = total / 28 + 2
    else:
        pages = total / 28
    for num in xrange(1, pages / 2):
        pra = "method=follower.ice.select&params.userId=" + userid + "&params.pageNo=" + str(num) + "&params.pageSize=28"
        url = FANU + pra
        gfx(userid, url)

        nux = pages - num
        pra = "method=follower.ice.select&params.userId=" + userid + "&params.pageNo=" + str(nux) + "&params.pageSize=28"
        url = FANU + pra
        gfx(userid, url)
        sleep(2)


def getfans(uid):
    print "uid:", uid, " Get fans info."
    uid = str(uid)
    pram = "method=follower.ice.select&params.userId=" + uid + "&params.pageNo=1&params.pageSize=28"
    fansu = FANU + pram
    temp = see.get(fansu)
    if temp.status_code == 404 or temp.status_code == 500:
        return 0
    temp.close()
    xtem = temp.json()
    total = xtem["data"]["total"]
    if total < 28:
        gfx(uid, fansu)
    else:
        getfansinfo(uid, total)


def getuserinfo(url, userid):
    temp = see.get(url)
    if temp.status_code == 404 or temp.status_code == 500:
        return 0
    temp.close()
    xtem = html.document_fromstring(temp.content)
    if "您访问的用户不存在！" in temp.content:  # 用户不存在
        return 0
    usnam = ""
    try:
        usnam = xtem.xpath("//div[@class='portrait']/h2/a[1]/text()")[0]  # 博主姓名
    except IndexError, e:
        pass
    usurl = url  # 博主地址
    xtfaf = xtem.xpath("//div[@class='relate-link']//a")
    xinfo = xtem.xpath("//div[@class='userinfo']/p/text()")
    blogs = xtem.xpath("//div[@class='home-module module-userblog']/div[1]/span/a/@href")
    if blogs:  # 如果有博客
        sleep(5)
        hend = requests.get(blogs[0]).apparent_encoding # 判断是否是旧版本的博客
        if hend is "GB2312":        #通过编码判断
            return 0
        usfol = xtfaf[0].xpath("text()")[0]  # 关注数量
        usfan = xtfaf[1].xpath("text()")[0]  # 粉丝数量
        uslon = xinfo[-3]  # 登录次数
        uslal = xinfo[-2]  # 最新登录
        usreg = xinfo[-1]  # 注册时间
        db = DBopt(DB)
        db.sql = "INSERT INTO userinfo(uid,usnam,usurl,usfan,usfol,uslon,uslal,usreg) VALUES (" + str(
            userid) + ",'" + usnam + "','" + usurl + "'," + usfan + "," + usfol + "," + uslon + ",'" + uslal + "','" + usreg + "')"
        db.sqlexe()
        db.dbclose()

        gbg = Thread(target=getblog, args=(userid, blogs[0],))      # 线程处理博客
        gbg.start() # 线程开始
        gbg.join()

        if int(usfan):
            gfs = Thread(target=getfans, args=(userid,))  # 粉丝抓取
            gfs.start()
            gfs.join()

        if int(usfol):  # 是否有关注
            gfo = Thread(target=getfoll, args=(userid,))  # 关注抓取
            gfo.start()
            gfo.join()


def getuser(uid):
    url = HOST + str(uid)
    getuserinfo(url, uid)


if __name__ == "__main__":
    cpar = ConfigParser.ConfigParser()      # 初始化配置处理对象
    cpar.read("x.conf")     #载入配置文件
    last = cpar.getint("conf", "last")  # 获取last配置
    zlas = 0
    for irl in xrange(last, 1009730, 4):
        if zlas == 1000:        # 1000个后休息70s
            print "sleep....................."
            sleep(70)
            zlas = 0    
        Process(target=getuser, args=(irl,)).start()    # 通过进程处理每个用户，生成进程并开始。
        Process(target=getuser, args=(irl + 1,)).start()
        Process(target=getuser, args=(irl + 2,)).start()
        Process(target=getuser, args=(irl + 3,)).start()
        cpar.set("conf", "last", irl + 4)       # 把未处理的的写入配置
        cpar.write(open("x.conf", "w"))         # 写入操作
        zlas += 1       # 次数加一
        sleep(2)        
