# -*- coding: UTF-8 -*-

import random
import os
import sys
import time

from punchcardpy.user import User

BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
# __file__获取执行文件相对路径，整行为取上一级的上一级目录
sys.path.append(BASE_DIR)

from punchcardpy.splicing_data import write_log_file, pc
from punchcardpy.connect_school import get_login_cookie
from punchcardpy.utils import read_json_file


# 读取名单文件随机分配打卡
def auto_rd_sleep_file(file_path):
    name_table_value_json = read_json_file(file_path)

    names_table = []
    # 获取总表
    for values in name_table_value_json['names']:
        names_table.append(User(values))
    auto_rd_sleep_pc_list(names_table)


# 直接使用名单列表随机打卡
def auto_rd_sleep_pc_list(names):
    if len(names) == 0:
        return
    # 打乱顺序
    random.shuffle(names)
    # 理论打卡间隔时间为3600/总人数+浏览器cookie获取时间（大约15-20s），计划分布在一个小时内，加上网络耗时，单个打卡预计20s+3600/总人数
    interval_time = 3600 / len(names)
    if interval_time > 20:
        interval_time = interval_time - 20

    for people in names:
        login_url_cookie = get_login_cookie(people.data["xh"])
        base_heat = [36.5, 36.5, 36.5]
        for i in range(0, 3):
            base_heat[i] += random.choice([0.3, 0.2, 0.1, 0, -0.1])
        results = pc(people, cookie=login_url_cookie, animal_heat=base_heat)

        write_log_file(number=people.number, results=results)
        time.sleep(interval_time)
