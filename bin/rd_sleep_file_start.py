# -*- coding: UTF-8 -*-
import os
import sys
import logging
from apscheduler.schedulers.blocking import BlockingScheduler

BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
# __file__获取执行文件相对路径，整行为取上一级的上一级的上一级目录
sys.path.append(BASE_DIR)

from punchcardpy.main import auto_rd_sleep_pc_file

# 定时任务
# 程序起点
# 随机分布打卡
if __name__ == "__main__":
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"

    logging.basicConfig(filename="../log/run_rd.log", level=logging.WARNING, format=LOG_FORMAT,
                        datefmt=DATE_FORMAT)
    sched = BlockingScheduler()
    sched.add_job(auto_rd_sleep_pc_file, 'cron',
                  day_of_week='0-6', hour=6, minute=30, args=["../punchcardpy/data/peoples.json"])
    sched.start()
