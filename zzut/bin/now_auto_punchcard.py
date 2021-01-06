# -*- coding: UTF-8 -*- 

# 直接打卡

import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
# __file__获取执行文件相对路径，整行为取上一级的上一级目录
sys.path.append(BASE_DIR)

from plugin.zzut.zzut_punchcard import auto_add_zzut_values


# 基础数据打卡，数据路径为/zzut/data/name_table_values.json
auto_add_zzut_values(BASE_DIR+"/zzut/data/name_table_values.json")
