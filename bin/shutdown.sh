#!/bin/bash

echo "1. 关闭快速打卡模式"
echo "2. 关闭随机分布打卡模式"
echo "3. 关闭配合WEB随机分布打卡模式"
echo "4. 关闭邮件报告提示"
echo "5. 关闭配合WEB快速随机分布打卡模式"
echo "6. 全部关闭"
# shellcheck disable=SC2162
read -p "选择需要关闭的模式：" pattern

case $pattern in
1)
  # shellcheck disable=SC2009
  ps -aux | grep "speed_file_start." | grep -v grep | awk '{print "kill -9 "$2}' | sh
  echo "快速打卡模式已关闭"
  ;;
2)
  # shellcheck disable=SC2009
  ps -aux | grep "rd_sleep_file_start" | grep -v grep | awk '{print "kill -9 "$2}' | sh
  echo "随机分布打卡模式已关闭"
  ;;
3)
  # shellcheck disable=SC2009
  ps -aux | grep "web_rd_sleep_start.py" | grep -v grep | awk '{print "kill -9 "$2}' | sh
  echo "配合WEB随机分布打卡模式已关闭"
  ;;
4)
  # shellcheck disable=SC2009
  ps -aux | grep "send_mail_report_start." | grep -v grep | awk '{print "kill -9 "$2}' | sh
  echo "邮件报告提示已关闭"
  ;;
5)
  ps -aux | grep "web_rd_speed_start." | grep -v grep | awk '{print "kill -9 "$2}' | sh
  echo "配合WEB快速随机分布打卡模式已关闭"
  ;;
6)
  # shellcheck disable=SC2009
  ps -aux | grep "send_mail_report_start." | grep -v grep | awk '{print "kill -9 "$2}' | sh
  # shellcheck disable=SC2009
  ps -aux | grep "speed_file_start." | grep -v grep | awk '{print "kill -9 "$2}' | sh
  # shellcheck disable=SC2009
  ps -aux | grep "rd_sleep_file_start" | grep -v grep | awk '{print "kill -9 "$2}' | sh
  # shellcheck disable=SC2009
  ps -aux | grep "web_rd_sleep_start.py" | grep -v grep | awk '{print "kill -9 "$2}' | sh
  echo "所有模式已全部关闭"
  ;;
esac
