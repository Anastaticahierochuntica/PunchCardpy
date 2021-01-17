# -*- coding: UTF-8 -*-
import datetime

import mysql.connector

from punchcardpy.entity import People
from punchcardpy.my_utils import read_json_file


def get_mysql_connect():
    mysql_config = read_json_file('../bin/data/mysql_config.json')

    connect = mysql.connector.connect(
        host=mysql_config["host"],  # 数据库主机地址
        user=mysql_config["user"],  # 数据库用户名
        passwd=mysql_config["passwd"],  # 数据库密码
        database=mysql_config["database"]  # 要连接的数据库
    )
    return connect


def get_mysql_peoples():
    connect = get_mysql_connect()
    # 获取数据库操作游标
    myCursor = connect.cursor()
    user_list = []
    try:
        # 执行sql语句
        myCursor.execute("select * from infor")
        results = myCursor.fetchall()
        columns = [column[0] for column in myCursor.description]
        for row in results:
            student = People(dict(zip(columns, row)))
            if student.status == "1":
                user_list.append(student)
            else:
                continue
    except Exception as e:
        print(e)
    myCursor.close()
    connect.close()
    return user_list


def void_operation_mysql(sql, var):
    connect = get_mysql_connect()
    myCursor = connect.cursor()
    try:
        myCursor.execute(sql, var)
        connect.commit()
    except Exception as e:
        connect.rollback()
        print(e)
    myCursor.close()
    connect.close()


def upload_log(user, results):
    void_operation_mysql('INSERT INTO `punchcard`.`pclog`'
                         '(`dateid`, `date`, `email`, `number`, `pcstatus`, `status`) VALUES '
                         '(%s, %s, %s, %s, %s, %s)',
                         (datetime.datetime.now().strftime("%Y%m%d"),
                          datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                          user.email, user.number, results['pcstatus'], results['status']))
