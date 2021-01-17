# -*- coding: UTF-8 -*- 

# 直接打卡

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
# __file__获取执行文件相对路径，整行为取上一级的上一级目录
sys.path.append(BASE_DIR)
from punchcardpy.main import auto_speed_pc_file

# 基础数据打卡，数据路径为/zzut/data/peoples.json
auto_speed_pc_file('../punchcardpy/data/peoples.json')
