# -*- coding: UTF-8 -*-

import random
import time

from punchcardpy.original_data import get_mysql_peoples, upload_log
from punchcardpy.entity import People
from punchcardpy.splicing_data import pc
from punchcardpy.connect_school import get_login_cookie, refresh_cookie
from punchcardpy.my_utils import read_json_file


# 读取名单文件随机分配打卡
def auto_rd_sleep_pc_file(file_path):
    peoples_json_file = read_json_file(file_path)

    peoples = []
    # 获取总表
    for people in peoples_json_file['names']:
        peoples.append(People(people))
    auto_rd_sleep_pc_list(peoples)


# 直接使用名单列表随机打卡
def auto_rd_sleep_pc_list(peoples):
    if len(peoples) == 0:
        return
    # 打乱顺序
    random.shuffle(peoples)
    # 理论打卡间隔时间为3600/总人数+浏览器cookie获取时间（大约15-20s），计划分布在一个小时内，加上网络耗时，单个打卡预计20s+3600/总人数
    interval_time = 3600 / len(peoples)
    if interval_time > 20:
        interval_time = interval_time - 20

    for people in peoples:
        login_url_cookie = get_login_cookie(people.number)
        base_heat = [36.5, 36.5, 36.5]
        for i in range(0, 3):
            base_heat[i] += random.choice([0.3, 0.2, 0.1, 0, -0.1])
        results = pc(people, cookie=login_url_cookie, animal_heat=base_heat)
        if 'code' in results:
            if results['code'] != "1":
                # 有几率是已经打过卡造成的异常，但以防万一，重新获取专属cookie打卡一次
                login_url_cookie = get_login_cookie(people.number)
                results = pc(student=people, cookie=login_url_cookie)
        upload_log(people, analyse_status(results=results))
        time.sleep(interval_time)


# 自动 网页 随机 停顿 打卡
def auto_web_rd_sleep_pc():
    auto_rd_sleep_pc_list(get_mysql_peoples())


# 直接使用名单列表快速打卡
def auto_speed_pc_list(peoples):
    login_url_cookie = ''
    # 循环执行打卡
    for people in peoples:

        if login_url_cookie == '':
            # 获取的是当前帐号的专属cookie
            login_url_cookie = get_login_cookie(people.number)
        else:
            # 如果不为空，刷新cookie所有权
            refresh_cookie(login_url_number=people.number, cookie=login_url_cookie)

        results = pc(student=people, cookie=login_url_cookie)
        if 'code' in results:
            if results['code'] != "1":
                # 有几率是已经打过卡造成的异常，但以防万一，重新获取专属cookie打卡一次
                login_url_cookie = get_login_cookie(people.number)
                results = pc(student=people, cookie=login_url_cookie)
        upload_log(people, analyse_status(results=results))


# 自动 快速 打卡 文件
def auto_speed_pc_file(file_path):
    peoples_json_file = read_json_file(file_path)

    peoples = []
    # 获取总表
    for people in peoples_json_file['names']:
        peoples.append(People(people))
    auto_speed_pc_list(peoples)


# 自动 网页 随机 快速 打卡
def auto_web_speed_pc():
    auto_speed_pc_list(get_mysql_peoples())


def analyse_status(results):
    if 'code' in results:
        if results['code'] == "-1":
            if results['message'] == "此时间已经填报！":
                return {'pcstatus': '1', 'status': "此时间已经填报！"}
            else:
                return {'pcstatus': '-1', 'status': results['message']}
        elif results['code'] == "1":
            return {'pcstatus': '1', 'status': "填报完成"}
        else:
            return {'pcstatus': '-1', 'status': results['message']}
    else:
        return {'pcstatus': '-1', 'status': "填报失败"}
