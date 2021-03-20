# -*- coding: UTF-8 -*-
from punchcardpy.my_utils import send_mail, read_str_file, read_json_file
from punchcardpy.original_data import get_mysql_peoples

"""
群发通知
"""
if __name__ == '__main__':

    file_str = read_str_file("./mail.html")
    mail_infor = read_json_file('./data/report_all_mail.json')
    for people in get_mysql_peoples():
        for i in range(0, 3):
            try:
                send_mail(mail_infor['mails'][i]['server'], mail_infor['mails'][i]['user'],
                          mail_infor['mails'][i]['passwd'], file_str.format(people.number), '企业微信打卡计划通知',
                          people.email)
                break
            except Exception as identifier:
                print(identifier)
                print("{0} {1} 使用{2}通知失败".format(
                    people.name, people.number, mail_infor['mails'][i]['user']))
