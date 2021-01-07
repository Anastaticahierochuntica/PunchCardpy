# -*- coding: UTF-8 -*-

import json
from datetime import datetime
import logging
import os
import sys
import mysql.connector
BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
# __file__获取执行文件相对路径，整行为取上一级的上一级目录
sys.path.append(BASE_DIR)
from plugin.zzut.zzut_rd_pubchcard import auto_rd_add_zzut_values


from plugin.universal.read_json_file import read_json_file
def auto_web_rd_add_zzut_values():
    mysql_infor = read_json_file(BASE_DIR+"/zzut/data/mysql_infor.json")

    connect = mysql.connector.connect(
        host=mysql_infor["host"],       # 数据库主机地址
        user=mysql_infor["user"],            # 数据库用户名
        passwd=mysql_infor["passwd"],          # 数据库密码
        database=mysql_infor["database"]         # 要连接的数据库
    )

    # 获取数据库操作游标
    myCursor = connect.cursor()
    user_infors = {"names": []}
    user_list = []
    school_user_infor = []
    try:
        # 执行sql语句
        myCursor.execute("select * from infor")
        results = myCursor.fetchall()
        columns = [column[0] for column in myCursor.description]
        for row in results:
            user_list.append(dict(zip(columns, row)))

        for user in user_list:
            if user['status'] == "-1":
                continue

            school_user_infor.append(
                {"dqwzmc": str(user['province'])+str(user['city'])+str(user['country']),
                 "bjmc": user['clazz'], "xh": user['number'],
                 "szdwmc": user['academy'],
                 "dqwz": user['addressnumber'],
                    "xm": user['name']})
        user_infors['names'] = school_user_infor
        with open(BASE_DIR+"/zzut/data/temp_user_list.json", "w", encoding='utf-8') as fp:
            fp.write(json.dumps(user_infors, indent=4,
                                sort_keys=True, ensure_ascii=False))
            fp.close()
        auto_rd_add_zzut_values(BASE_DIR+"/zzut/data/temp_user_list.json")
        if os.path.exists(BASE_DIR+"/zzut/data/temp_user_list.json"):
            os.remove(BASE_DIR+"/zzut/data/temp_user_list.json")
    except Exception as e:
        logging.ERROR(e)
        print(e)

    connect.close()
