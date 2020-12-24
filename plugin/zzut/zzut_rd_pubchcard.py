# -*- coding: UTF-8 -*-

import random
import json
from fake_useragent import UserAgent
import urllib.request
from datetime import datetime
import os
import sys
import time
from apscheduler.schedulers.blocking import BlockingScheduler
BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
# __file__获取执行文件相对路径，整行为取上一级的上一级目录
sys.path.append(BASE_DIR)

from plugin.zzut.zzut_punchcard import write_log_file, write_temp_report_file, analyse_status, add_zzut_values
from plugin.zzut.cookie import get_login_cookie
from plugin.universal.read_json_file import read_json_file

class Student:
    """
    学生类
    """
    data = {}

    def __init__(self, self_information):
        self.data = self_information


# 随机分配打卡
def auto_rd_add_zzut_values(file_path):

    name_table_value_json = read_json_file(file_path)

    names_table = []
    # 获取总表
    for values in name_table_value_json['names']:
        names_table.append(Student(values))

    if len(names_table) == 0:
        return
    # 打乱顺序
    random.shuffle(names_table)
    # 理论打卡间隔时间为3600/总人数+浏览器cookie获取时间（大约15-20s），计划分布在一个小时内，加上网络耗时，单个打卡预计20s+3600/总人数
    interval_time = 3600/len(names_table)
    if interval_time > 20:
        interval_time = interval_time-20
    # 邮件报告信息头与信息尾
    inform_content_head = "<table id=\"customers\"><tr><th>打卡学号</th><th>打卡时间</th><th>打卡状态</th></tr>"
    inform_content_tail = "</table>"
    for people in names_table:
        login_url_cookie = get_login_cookie(people.data["xh"])
        base_heat = [36.5, 36.5, 36.5]
        for i in range(0, 3):
            base_heat[i] += random.choice([0.3, 0.2, 0.1, 0, -0.1])
        results = add_zzut_values(address=people.data["dqwzmc"], class_and_grade=people.data["bjmc"], number=people.data["xh"],
                                  academy=people.data["szdwmc"], current_position_number=people.data["dqwz"], name=people.data["xm"],
                                  cookie=login_url_cookie, animal_heat=base_heat)
        # 信息内容
        inform_content_head += "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (
            people.data["xh"], datetime.now().strftime("%Y-%m-%d %H:%M:%S"), analyse_status(results=results))
        write_log_file(number=people.data["xh"], results=results)
        time.sleep(interval_time)
    write_temp_report_file(content=inform_content_head+inform_content_tail)
