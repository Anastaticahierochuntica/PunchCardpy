# -*- coding: UTF-8 -*-
import datetime


# 获取钉钉打卡链接
def zzut_dingding_out_date(filepath):
    head_url = 'https://swform.dingtalk.com/index.htm?web_wnd=general&width=960&height=640#/queWrite/dingf90d9c8ff20d2e0024f2f5cc6abecb85/PROC-7BFCA226-6685-4C57-871C-65A4FBC4C14E/3c07a6244c62201975545e330c41a98d?bizType=0&loopDate='
    # 2020-11-19
    date_base_tag = 16057404
    date_base = datetime.datetime(2020, 11, 19)
    tail_url = '00000&writeSource=8'
    date_nowaday = datetime.datetime.now()

    file = open(filepath, 'w+')
    for i in range(0, 30):
        file.write(head_url+str(((date_nowaday-date_base).days+i)
                                * 864+date_base_tag)+tail_url)
        file.write('\n')
    file.close()
