# -*- coding: UTF-8 -*-
import os
import sys
import logging
from apscheduler.schedulers.blocking import BlockingScheduler

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# __file__获取执行文件相对路径，整行为取上一级的上一级的上一级目录
sys.path.append(BASE_DIR)

from punchcardpy.main import send_pc_table_mail

# 定时任务
# 程序起点
# 发送打卡报告
if __name__ == "__main__":
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
    logging.basicConfig(filename="../log/send_mail.log", level=logging.INFO, format=LOG_FORMAT,
                        datefmt=DATE_FORMAT)
    sched = BlockingScheduler()
    sched.add_job(send_pc_table_mail, 'cron',
                  day_of_week='0-6', hour=9, minute=0, args=["./data/mail_config.json"])
    sched.start()
