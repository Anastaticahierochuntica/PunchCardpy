# -*- coding: UTF-8 -*-
import os
import sys
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
# __file__获取执行文件相对路径，整行为取上一级的上一级的上一级目录
sys.path.append(BASE_DIR)
from plugin.zzut.zzut_rd_web_punchcard import auto_web_rd_add_zzut_values
from plugin.zzut.zzut_punchcard import report_mail

# 定时任务
# 程序起点
# 配合WEB随机分布打卡
if __name__ == "__main__":
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"

    logging.basicConfig(filename=BASE_DIR+"/zzut/log/run_rd.log",
                        level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)
    sched = BlockingScheduler()
    sched.add_job(auto_web_rd_add_zzut_values, 'cron',
                  day_of_week='0-6', hour=15, minute=19)
    sched.add_job(report_mail, 'cron', day_of_week='0-6', hour=9, minute=0)
    sched.start()
