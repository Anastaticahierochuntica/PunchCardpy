# -*- coding: UTF-8 -*-

import random
import time

from punchcardpy.original_data import get_mysql_peoples, upload_log, get_mysql_logs
from punchcardpy.entity import People
from punchcardpy.splicing_data import pc
from punchcardpy.my_utils import read_json_file, send_mail_use_config


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
        results = pc(people)
        if 'code' in results:
            if results['code'] != "1":
                # 有几率是已经打过卡造成的异常，但以防万一，重新打卡一次
                results = pc(student=people)
        upload_log(people, analyse_status(results=results))
        time.sleep(interval_time)


# 自动 网页 随机 停顿 打卡
def auto_web_rd_sleep_pc():
    auto_rd_sleep_pc_list(get_mysql_peoples())


# 直接使用名单列表快速打卡
def auto_speed_pc_list(peoples):
    # 循环执行打卡
    for people in peoples:
        results = pc(student=people)
        if 'code' in results:
            if results['code'] != "1":
                # 有几率是已经打过卡造成的异常，但以防万一，重新打卡一次
                results = pc(student=people)
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
                return {'pcstatuscode': '1', 'pcstatusmsg': "此时间已经填报！"}
            else:
                return {'pcstatuscode': '-1', 'pcstatusmsg': results['message']}
        elif results['code'] == "1":
            return {'pcstatuscode': '1', 'pcstatusmsg': "填报完成"}
        else:
            return {'pcstatuscode': '-1', 'pcstatusmsg': results['message']}
    else:
        return {'pcstatuscode': '-1', 'pcstatusmsg': "填报失败"}


def send_pc_table_mail(mail_config_path):
    mail_config = read_json_file(mail_config_path)
    table_css = mail_config['content_css']
    table_head = "<table id=\"customers\"><tr><th>打卡学号</th><th>打卡邮箱</th><th>打卡时间</th><th>打卡状态</th><th>打卡返回信息</th></tr>"
    table_content = ''
    table_tail = "</table>"
    for single_log in get_mysql_logs():
        table_content += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
            single_log.people.number, single_log.people.email, single_log.date, single_log.pcstatuscode,
            single_log.pcstatusmsg)
    send_mail_use_config(mail_config_path, table_css + table_head + table_content + table_tail)
