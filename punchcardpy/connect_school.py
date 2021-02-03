# -*- coding: UTF-8 -*-

import logging
import urllib
from http import cookiejar
from urllib import request

import time
import json

from pip._vendor import requests


def get_cookie(url, headers, data):
    while True:
        try:
            # 声明一个CookieJar对象实例来保存cookie
            cookie = cookiejar.CookieJar()
            # 利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
            handler = request.HTTPCookieProcessor(cookie)
            # 通过CookieHandler创建opener
            opener = request.build_opener(handler)
            my_request = request.Request(
                url, headers=headers, data=json.dumps(data).encode("utf-8"))
            # 此处的open方法打开网页
            response = opener.open(my_request)
            # 打印cookie信息
            cookies_dist = requests.utils.dict_from_cookiejar(cookie)
            return 'SESSION=' + cookies_dist['SESSION']
        except Exception as identifier:
            logging.warning("{0}  获取cookie出错".format(data['xh']))
            logging.warning(identifier)
            time.sleep(5 * 60)


def get_login_cookie(login_url_number):
    # 初始化程序
    weiXinJsSdkApiAuthorize_json = {
        "url": 'http://sjgl.zzut.edu.cn/vue/qyweixin/main?userAccount=' + login_url_number + '&agentId=1000060'}
    headers = {'Content-Type': 'application/json;charset=UTF-8'}
    weiXinJsSdkApiAuthorize_request = urllib.request.Request(
        url='http://sjgl.zzut.edu.cn/mobile/weiXinJsSdkApiAuthorize.json', headers=headers,
        data=json.dumps(weiXinJsSdkApiAuthorize_json).encode(encoding='utf-8'))
    urllib.request.urlopen(weiXinJsSdkApiAuthorize_request)  # 发送请求
    # 设置用户负载
    data = {"userAccount": "{0}".format(login_url_number)}
    return get_cookie('http://sjgl.zzut.edu.cn/mobile/setUserInfo.json', headers=headers, data=data)


# 用于添加当前时间点的打卡记录的
def send_request(data):
    try:
        url = 'http://sjgl.zzut.edu.cn/gx/gxxs/jkzk/saveOrEdit.json'
        headers = {'Cookie': get_login_cookie(data['xh']), 'Accept-Encoding': 'gzip',
                   'Content-Type': 'application/json;charset=UTF-8'}
        req = urllib.request.Request(url=url, headers=headers, data=json.dumps(
            data).encode(encoding='UTF8'))  # 需要通过encode设置编码 要不会报错
        response = request.urlopen(req)  # 发送请求

        logInfo = response.read().decode()  # 读取对象 将返回的二进制数据转成string类型

        return_code = json.loads(logInfo)
        return return_code
    except Exception as identifier:
        print(identifier)
        logging.warning("{0}  请求出错".format(data['xh']))
        time.sleep(5 * 60)

# 将用户信息设置为官方信息，web端已经设定过，可不再调用；使用文件信息时推荐调用
def setUserBase(people):
    try:
        url = 'http://sjgl.zzut.edu.cn/gxxs/xsjbxx101/getByXsxx.json'
        data = {"xhId": "{0}".format(people.number)}
        headers = {'Cookie': get_login_cookie(people.number), 'Accept-Encoding': 'gzip',
                   'Content-Type': 'application/json;charset=UTF-8'}
        req = urllib.request.Request(url=url, headers=headers, data=json.dumps(
            data).encode(encoding='UTF8'))  # 需要通过encode设置编码 要不会报错
        response = request.urlopen(req)  # 发送请求

        logInfo = response.read().decode()  # 读取对象 将返回的二进制数据转成string类型

        return_code = json.loads(logInfo)
        people.academy = return_code['dwmc']
        people.clazz = return_code['bjmc']
        people.name = return_code['xm']
    except Exception as identifier:
        print(identifier)
        logging.warning("{0}  设置基础信息请求出错".format(people.number))
        time.sleep(60)
