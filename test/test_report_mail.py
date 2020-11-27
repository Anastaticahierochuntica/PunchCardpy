# -*- coding: UTF-8 -*- 

# 测试发送邮件功能

import os
import sys
from apscheduler.schedulers.blocking import BlockingScheduler
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# __file__获取执行文件相对路径，整行为取上一级的上一级目录
sys.path.append(BASE_DIR)

from plugin.zzut.zzut_punchcard import report_mail


# 数据路径为/zzut/data/mail_user.json
report_mail()