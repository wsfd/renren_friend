#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import http.cookiejar
import re
import urllib.request
from urllib import request
import urllib.parse
import zlib


def login(username, password):
    """log in and return uid"""
    logpage = 'http://www.renren.com/ajaxLogin/login'
    data = {'email': username, 'password': password}
    login_data = urllib.parse.urlencode(data).encode('utf-8')

    cookie = http.cookiejar.CookieJar()  # 声明一个CookieJar对象实例来保存cookie
    handler = urllib.request.HTTPCookieProcessor(cookie)  # 利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
    opener = urllib.request.build_opener(handler)  # 通过handler来构建opener
    request.install_opener(opener)

    res = opener.open(logpage, login_data)
    print("Login now ...")
    html = res.read()
    html = html.decode('utf-8', 'ignore')
    print (html)
    print("Login successfully")


def getfriends():
    global dict1
    dict1 = {}
    url = 'http://friend.renren.com/groupsdata'
    req = urllib.request.Request(url, headers={
        'Host': 'friend.renren.com',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        'Referer': 'http://friend.renren.com/managefriends',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'RA-Ver': '3.0.7',
        'RA-Sid': '655102BF-20150723-085431-c809af-3fa054',
    })

    oper = urllib.request.urlopen(req)
    html = oper.read()
    html = zlib.decompress(html, 16 + zlib.MAX_WBITS)
    html = html.decode('utf-8', 'ignore')
    print (html)
    html = html.replace('\n','')
    fid = re.findall(r'"fid":(\d{4,11})', html)
    fname = re.findall(r'"fname":"(.{5,40})","info',html)
    for i in range(0, len(fid)):
        id = fid[i]
        try:
            name = fname[i]
            name = name.encode('utf-8').decode('unicode-escape')
        except:
            print ("获取本人好友结束")
            break
        else:

            print(id, name)
            dict1[id] = name
    return dict1

username = '523295349@qq.com'
password = 'ws123456789'
login(username, password)
getfriends()
f = len(dict1)
print (f)

del dict1['269084088']

with open('D:/Pycharm/friends_id_dict.txt', 'wt',encoding='UTF-8') as f:
    print(dict1, file=f)