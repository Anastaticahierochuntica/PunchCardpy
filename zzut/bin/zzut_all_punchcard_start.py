# -*- coding: UTF-8 -*-
import os
import sys
from apscheduler.schedulers.blocking import BlockingScheduler
BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
# __file__获取执行文件相对路径，整行为取上一级的上一级的上一级目录
sys.path.append(BASE_DIR)

from plugin.zzut.zzut_punchcard import report_mail
from plugin.zzut.zzut_punchcard import auto_add_zzut_full_values

# 定时任务
# 程序起点
# 全变量打卡
if __name__ == "__main__":
    sched = BlockingScheduler()
    sched.add_job(auto_add_zzut_full_values, 'cron',
                day_of_week='0-6', hour=6, minute=30, args=[BASE_DIR+"/zzut/data/name_table_values.json"])
    sched.add_job(report_mail, 'cron', day_of_week='0-6', hour=9, minute=0)
    sched.start()