# -*- coding: UTF-8 -*-

import json
from fake_useragent import UserAgent
import urllib.request

from punchcardpy.connect_school import get_url_cookies, add_record


# 打卡
# address当前位置名称
# class_and_grade 班级名称
# current_position_number 当前位置行政编码，不是邮编
# number 学号
# academy 学院
# animal_heat 体温元组
def pc(student, cookie='', animal_heat=['36.4', '36.8', '36.2']):
    # 目前已知的url提交链接
    url = 'http://sjgl.zzut.edu.cn/gx/gxxs/jkzk/saveOrEdit.json'

    # 目前已知的部分数据串，不同班级或许有不同，内部包含大量数据，自行填写,最好将实际数据直接替换
    values = {"xy": 0, "mqjcs": "", "dysj": "", "counts": "", "jzqksm": "", "yc": "", "zmd": 0, "ycztArray": [],
              "yhsf": "", "id": "", "sfkyfx": "", "dqwz": student.addressnumber, "yy": "", "bjh": "", "qt": "",
              "wtb": "", "sfyc": "1", "zc": "", "ssnj": "", "selectedArea": student.addressnumber, "zj": 0, "zk": 0,
              "yczzArray": [], "dwh": "", "xbmc": "", "zwtw": animal_heat[1], "drtw": animal_heat[2], "xgsj": "",
              "shgh": "", "bh": "", "dwmc": "", "ny": 0, "dqwzmc": student.address, "fbrq": "", "bz": "", "shsj": "",
              "gd": 0, "sq": 0, "sfycmc": "", "shjg": "", "kfrq": "", "tb": "", "bjmc": student.clazz,
              "xh": student.number,
              "yczz": "", "szdwmc": student.academy, "tbsj": "", "xm": student.name, "yddh": "", "zxhj": 0, "hb": 0,
              "xwtw": animal_heat[0], "fdyxm": "", "yczt": "", "fyq": 0}

    if cookie == '':
        # 页面cookie来源连接
        login_url = 'http://sjgl.zzut.edu.cn/vue/qyweixin/main?userAccount=' + \
                    values['xh'] + '&agentId=1000060'
        cookie = get_url_cookies(login_url)
    # 请求头原型,可根据自己实际自行添加键值对{'Cookie': '', 'Accept-Encoding': '', 'Content-Type': '','User-Agent': ua.random,
    # 'Referer': ''} User-Agent伪装浏览器类型，默认随机 Referer防盗链参数，用于声明是从哪个页面转到这里的
    headers = {'Cookie': cookie, 'Accept-Encoding': 'gzip', 'Content-Type': 'application/json;charset=UTF-8',
               'Referer': 'http://sjgl.zzut.edu.cn/vue/qyweixin/gx/gxxs/jkbg/jkbgMain/jkbgList'}
    return add_record(url=url, headers=headers, data=values)


# 修改功能有，但绝壁不能乱给，改错了全完犊子
# value是完整的数据条，别想着乱搞，数据条有个id，那是指定哪一条数据的关键
def modify_pc(cookie, **data):
    # 伪装成浏览器
    ua = UserAgent()
    url = 'http://sjgl.zzut.edu.cn/gx/gxxs/jkzk/saveOrEdit.json'

    # 设置请求头 告诉服务器请求携带的是json格式的数据
    # Referer防盗链参数，用于声明是从哪个页面转到这里的
    headers = {'Cookie': cookie, 'Accept-Encoding': 'gzip', 'Content-Type': 'application/json;charset=UTF-8',
               'User-Agent': ua.random,
               'Referer': 'http://sjgl.zzut.edu.cn/vue/qyweixin/gx/gxxs/jkbg/jkbgFrom?id='}

    values = data['data']

    headers['Referer'] = headers['Referer'] + values['id']

    request = urllib.request.Request(url=url, headers=headers, data=json.dumps(
        values).encode(encoding='UTF8'))  # 需要通过encode设置编码 要不会报错

    response = urllib.request.urlopen(request)  # 发送请求

    logInfo = response.read().decode()  # 读取对象 将返回的二进制数据转成string类型
    return_code = json.loads(logInfo)
    return return_code
