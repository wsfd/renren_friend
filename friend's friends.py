# -*- coding: UTF-8 -*-


import urllib
import http.cookiejar
import re
import urllib.request
from urllib import request
import urllib.parse
import pickle
import random
import time
import socket


timeout = 30
socket.setdefaulttimeout(timeout)
date = time.strftime('%Y-%m-%d',time.localtime(time.time()))

proxy_list=[]
for line in open("下载.txt"):
    line = line.strip('\n')#去掉换行符
    proxy_list.append(line)

def proxyset():
    proxy = random.choice(proxy_list)
    proxy_support = request.ProxyHandler({'http':proxy})
    opener = request.build_opener(proxy_support, request.HTTPHandler)
    request.install_opener(opener)

def login(username, password):
    """log in and return uid"""
    global opener
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
    print("Login successfully")



def getfriends_totalcount(id):
    global totalcount
    print('好友ID:' + id )
    data = {'p': { "fid":id,"pz":"24","type":"WEB_FRIEND","pn":"0"},'requestToken':1357950638,'_rtk' : '1cb1ad08'}
    data =  urllib.parse.urlencode(data).encode('utf-8')
    page = 'http://friend.renren.com/friend/api/getotherfriendsdata'
    req = urllib.request.Request(page,data ,headers = {
        'Connection': 'keep-alive',
        'Host': 'friend.renren.com',
        'Content-Length': '99',
        'Accept':' application/json, text/javascript, */*; q=0.01',
        'Origin':'http://friend.renren.com',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent':' Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'http://friend.renren.com/otherfriends?id=360967112',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'RA-Ver':' 3.0.7',
        'RA-Sid': '655102BF-20150723-085431-c809af-3fa054',
        })
    try:
        oper = opener.open(page, data)
        html = oper.read()
    except:
        print ('连接出现错误，正在解决中...')
        proxyset()
        totalcount = 9999
    else:
        html = html.decode('utf-8', 'ignore')
        total = re.findall(r'"total":(\d{1,6})', html)
        totalcount = total[0]
        print (totalcount)
    return totalcount

def getfriends_friends(id,totalcount):
    dict = {}
    data = {'p': { "fid":id,"pz":totalcount,"type":"WEB_FRIEND","pn":"0"},'requestToken':1357950638,'_rtk' : '1cb1ad08'}
    data =  urllib.parse.urlencode(data).encode('utf-8')
    page = 'http://friend.renren.com/friend/api/getotherfriendsdata'
    req = urllib.request.Request(page,data ,headers = {
        'Connection': 'keep-alive',
        'Host': 'friend.renren.com',
        'Content-Length': '99',
        'Accept':' application/json, text/javascript, */*; q=0.01',
        'Origin':'http://friend.renren.com',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent':' Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'http://friend.renren.com/otherfriends?id=360967112',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'RA-Ver':' 3.0.7',
        'RA-Sid': '655102BF-20150723-085431-c809af-3fa054',
        })
    try:
        oper = opener.open(page, data)
        html = oper.read()
    except:
        print ('连接出现错误，正在解决中...')
        friends_id.append(id)
        proxyset()
    else:
        html = html.decode('utf-8', 'ignore')
        html = html.replace('\n','')
        html = html.encode('utf-8').decode('unicode-escape','replace')
        fid = re.findall(r'"fid":(\d{1,12})', html)
        fname = re.findall(r'"fname":"(.{1,40})","info',html)
        print (len(fid))
        f = "获取好友结束" + str(id)
        for i in range(0, len(fid)):
            a = fid[i]
            try:
                b = fname[i]
            except:
                print ('结束了应该没问题吧')
                print(i)
            #name = name.encode('utf-8').decode('unicode-escape')
            else:
                dict[a] = b
        print (f)
        with open(str(id) + '.txt','wt',encoding='UTF-8') as f:
            print(dict,file=f)
        print ('输出文件结束')
    return dict

username = '523295349@qq.com'
password = 'ws123456789'
login(username, password)

friends_id = []
with open('friends_id.txt', 'r') as f:
    friends_id = f.read()
    friends_id = friends_id.replace('\'','')
    friends_id = friends_id.replace(' ','')
    friends_id = friends_id.split(',')
    for id in friends_id :
        getfriends_totalcount(id)
        getfriends_friends(id,totalcount)



