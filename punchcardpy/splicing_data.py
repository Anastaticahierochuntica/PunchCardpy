# -*- coding: UTF-8 -*-

import random

from punchcardpy.connect_school import send_request


#
# address当前位置名称
# class_and_grade 班级名称
# current_position_number 当前位置行政编码，不是邮编
# number 学号
# academy 学院
# animal_heat 体温元组
def pc(student, animal_heat=None):
    """
    打卡
    :param student: 打卡对象
    :param animal_heat: 体温
    :return: 返回码
    """
    # 目前已知的url提交链接
    if animal_heat is None:
        animal_heat = [i + random.choice([0.3, 0.2, 0.1, 0, -0.1]) for i in [36.5, 36.5, 36.5]]
    # 数据条
    values = {"xy": 0, "mqjcs": "", "dysj": "", "counts": "", "jzqksm": "", "yc": "", "zmd": 0, "ycztArray": [],
              "yhsf": "", "id": "", "sfkyfx": "", "dqwz": student.addressnumber, "yy": "", "bjh": "", "qt": "",
              "wtb": "", "sfyc": "1", "zc": "", "ssnj": "", "selectedArea": student.addressnumber, "zj": 0, "zk": 0,
              "yczzArray": [], "dwh": "", "xbmc": "", "zwtw": animal_heat[1], "drtw": animal_heat[2], "xgsj": "",
              "shgh": "", "bh": "", "dwmc": "", "ny": 0, "dqwzmc": student.address, "fbrq": "", "bz": "", "shsj": "",
              "gd": 0, "sq": 0, "sfycmc": "", "shjg": "", "kfrq": "", "tb": "", "bjmc": student.clazz,
              "xh": student.number,
              "yczz": "", "szdwmc": student.academy, "tbsj": "", "xm": student.name, "yddh": "", "zxhj": 0, "hb": 0,
              "xwtw": animal_heat[0], "fdyxm": "", "yczt": "", "fyq": 0}
    # 请求头原型,可根据自己实际自行添加键值对{'Cookie': '', 'Accept-Encoding': '', 'Content-Type': ''}

    return send_request(data=values)


# value是完整的数据条，数据条有个id，那是指定哪一条数据的关键
def modify_pc(data):
    return send_request(data=data)
