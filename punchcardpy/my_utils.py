import datetime
import json
import smtplib
from email.mime.text import MIMEText
import logging


def send_mail(server, user, passwd, content, subject, to_user):
    """
    :param server: 定义服务
    :param user: 账号
    :param passwd: 密码或者授权码
    :param content: 内容
    :param subject: 设置主题
    :param to_user: 收件人
    :return: 无
    """
    message = MIMEText(content, "HTML")
    message["subject"] = subject
    message["From"] = user
    message["To"] = to_user
    try:
        smtp_email = smtplib.SMTP_SSL(server, 465)  # 定义邮箱服务器
        smtp_email.login(user=user, password=passwd)  # 登陆邮箱
        smtp_email.sendmail(from_addr=user, to_addrs=to_user,
                            msg=message.as_string())  # 发送
        smtp_email.quit()  # 断开退出邮箱
    except Exception as e:
        logging.warning("邮件发送失败")
        logging.warning(e)


def send_mail_use_config(mail_config_path, content):
    mail_config = read_json_file(mail_config_path)
    send_mail(mail_config['server'], mail_config['user'], mail_config['passwd'], content,
              mail_config['subject'],
              mail_config['to_user'])


def read_json_file(file_path):
    """
    读取json文件
    :param file_path: 文件路径
    :return: 无
    """
    json_file = open(file_path, "r", encoding='UTF-8')
    results_json = json.load(json_file)
    json_file.close()
    return results_json


def read_str_file(file_path):
    """
    读取文本文件
    :param file_path: 文件路径
    :return: 无
    """
    str_file = open(file_path, "r", encoding='UTF-8')
    str_file_str = ""
    for line in str_file:
        str_file_str = str_file_str + line
    str_file.close()
    return str_file_str


def dingding_out_date(filepath):
    """
    获取钉钉打卡链接
    :param filepath: 输出路径
    :return: 无
    """
    head_url = 'https://swform.dingtalk.com/index.htm?web_wnd=general&width=960&height=640#/queWrite' \
               '/dingf90d9c8ff20d2e0024f2f5cc6abecb85/PROC-7BFCA226-6685-4C57-871C-65A4FBC4C14E' \
               '/3c07a6244c62201975545e330c41a98d?bizType=0&loopDate= '
    # 2020-11-19
    date_base_tag = 16057404
    date_base = datetime.datetime(2020, 11, 19)
    tail_url = '00000&writeSource=8'
    date_nowaday = datetime.datetime.now()

    file = open(filepath, 'w+')
    for i in range(0, 30):
        file.write(head_url + str(((date_nowaday - date_base).days + i)
                                  * 864 + date_base_tag) + tail_url)
        file.write('\n')
    file.close()
