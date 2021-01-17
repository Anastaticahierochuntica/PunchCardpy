# -*- coding: UTF-8 -*-

import json
from fake_useragent import UserAgent
import urllib.request
from datetime import datetime
import os
import sys

from punchcardpy.information import add_record

BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
# __file__获取执行文件相对路径，整行为取上一级的上一级目录
sys.path.append(BASE_DIR)

from punchcardpy.connect_school import refresh_cookie, get_login_cookie, get_cookies
from punchcardpy.utils import read_json_file


# address当前位置名称
# class_and_grade 班级名称
# current_position_number 当前位置行政编码，不是邮编
# number 学号
# academy 学院
# animal_heat 体温元组


def add_zzut_values(address, class_and_grade, number, academy, current_position_number, name, cookie='',
                    animal_heat=['36.4', '36.8', '36.2']):
    # 目前已知的url提交链接
    url = 'http://sjgl.zzut.edu.cn/gx/gxxs/jkzk/saveOrEdit.json'

    # 目前已知的部分数据串，不同班级或许有不同，内部包含大量数据，自行填写,最好将实际数据直接替换
    values = {"xy": 0, "mqjcs": "", "dysj": "", "counts": "", "jzqksm": "", "yc": "", "zmd": 0, "ycztArray": [],
              "yhsf": "", "id": "", "sfkyfx": "", "dqwz": current_position_number, "yy": "", "bjh": "", "qt": "",
              "wtb": "", "sfyc": "1", "zc": "", "ssnj": "", "selectedArea": current_position_number, "zj": 0, "zk": 0,
              "yczzArray": [], "dwh": "", "xbmc": "", "zwtw": animal_heat[1], "drtw": animal_heat[2], "xgsj": "",
              "shgh": "", "bh": "", "dwmc": "", "ny": 0, "dqwzmc": address, "fbrq": "", "bz": "", "shsj": "", "gd": 0,
              "sq": 0, "sfycmc": "", "shjg": "", "kfrq": "", "tb": "", "bjmc": class_and_grade, "xh": number,
              "yczz": "", "szdwmc": academy, "tbsj": "", "xm": name, "yddh": "", "zxhj": 0, "hb": 0,
              "xwtw": animal_heat[0], "fdyxm": "", "yczt": "", "fyq": 0}

    if cookie == '':
        # 页面cookie来源连接
        login_url = 'http://sjgl.zzut.edu.cn/vue/qyweixin/main?userAccount=' + \
                    values['xh'] + '&agentId=1000060'
        cookie = get_cookies(login_url)
    # 请求头原型,可根据自己实际自行添加键值对{'Cookie': '', 'Accept-Encoding': '', 'Content-Type': '','User-Agent': ua.random,
    # 'Referer': ''} User-Agent伪装浏览器类型，默认随机 Referer防盗链参数，用于声明是从哪个页面转到这里的
    headers = {'Cookie': cookie, 'Accept-Encoding': 'gzip', 'Content-Type': 'application/json;charset=UTF-8',
               'Referer': 'http://sjgl.zzut.edu.cn/vue/qyweixin/gx/gxxs/jkbg/jkbgMain/jkbgList'}
    return add_record(url=url, headers=headers, data=values)


# 修改功能有，但绝壁不能乱给，改错了全完犊子
# value是完整的数据条，别想着乱搞，数据条有个id，那是指定哪一条数据的关键
def modify_zzut_full_values(cookie, **data):
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


# 打印日志
def write_log_file(number, results):
    if not os.path.exists(BASE_DIR + '/zzut/log'):
        os.makedirs(BASE_DIR + '/zzut/log')
    elif not os.path.isdir(BASE_DIR + '/zzut/log'):
        os.remove(BASE_DIR + '/zzut/log')
        os.makedirs(BASE_DIR + '/zzut/log')

    # 以追加形式打开日志文件
    log_file = open(BASE_DIR + '/zzut/log/punchcard.log',
                    'a', encoding='UTF-8')
    log_file.write(number + '\t')
    log_file.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\t')
    log_file.write(analyse_status(results=results))
    log_file.write('\n')
    log_file.close()


def analyse_status(results):
    if 'code' in results:
        if results['code'] == "-1":
            if results['message'] == "此时间已经填报！":
                return "此时间已经填报！"
            else:
                return "填报失败"
        elif results['code'] == "1":
            return "填报完成"
        else:
            return "填报失败异常"
    else:
        return "填报失败"


def auto_add_zzut_values(file_path):
    name_table_value_json = read_json_file(file_path)

    login_url_cookie = ''
    # 循环执行打卡
    for values in name_table_value_json['names']:

        if login_url_cookie == '':
            # 获取的是当前帐号的专属cookie
            login_url_cookie = get_login_cookie(values["xh"])
        else:
            # 如果不为空，刷新cookie所有权
            refresh_cookie(
                login_url_number=values["xh"], cookie=login_url_cookie)

        results = add_zzut_values(address=values["dqwzmc"], class_and_grade=values["bjmc"], number=values["xh"],
                                  academy=values["szdwmc"], current_position_number=values["dqwz"], name=values["xm"],
                                  cookie=login_url_cookie)
        if 'code' in results:
            if results['code'] != "1":
                # 有几率是已经打过卡造成的异常，但以防万一，重新获取专属cookie打卡一次
                login_url_cookie = get_login_cookie(values["xh"])
                results = add_zzut_values(address=values["dqwzmc"], class_and_grade=values["bjmc"], number=values["xh"],
                                          academy=values["szdwmc"], current_position_number=values["dqwz"],
                                          name=values["xm"], cookie=login_url_cookie)
        write_log_file(number=values["xh"], results=results)