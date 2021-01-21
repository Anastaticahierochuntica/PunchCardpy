#!/bin/bash

if [ ! -d ../log ]; then
  mkdir ../log
fi

echo "1. 开启文件快速打卡模式"
echo "2. 开启文件随机分布打卡模式"
echo "3. 开启配合WEB随机分布打卡模式"
echo "4. 以上全部开启"
echo "5. 立即打卡一次"
echo "6. 开启邮件报告提示"
# shellcheck disable=SC2162
read -p "选择需要的模式：" pattern
project_path=$(pwd)
case $pattern in
1)
  # shellcheck disable=SC2009
  ps -aux | grep "speed_file_start." | grep -v grep | awk '{print "kill -9 "$2}' | sh
  nohup python3 "${project_path}"/speed_file_start.py >>../log/runtime.log 2>>../log/runtime.log &
  echo "文件快速打卡模式已开启"
  ;;
2)
  # shellcheck disable=SC2009
  ps -aux | grep "rd_sleep_file_start" | grep -v grep | awk '{print "kill -9 "$2}' | sh
  nohup python3 "${project_path}"/rd_sleep_file_start.py >>../log/runtime.log 2>>../log/runtime.log &
  echo "文件随机分布打卡模式已开启"
  ;;
3)
  # shellcheck disable=SC2009
  ps -aux | grep "web_rd_sleep_start.py" | grep -v grep | awk '{print "kill -9 "$2}' | sh
  nohup python3 "${project_path}"/web_rd_sleep_start.py >>../log/runtime.log 2>>../log/runtime.log &
  echo "配合WEB随机分布打卡模式已开启"
  ;;
4)
  # shellcheck disable=SC2009
  ps -aux | grep "speed_file_start." | grep -v grep | awk '{print "kill -9 "$2}' | sh
  # shellcheck disable=SC2009
  ps -aux | grep "rd_sleep_file_start" | grep -v grep | awk '{print "kill -9 "$2}' | sh
  # shellcheck disable=SC2009
  ps -aux | grep "web_rd_sleep_start" | grep -v grep | awk '{print "kill -9 "$2}' | sh
  nohup python3 "${project_path}"/speed_file_start.py >>../log/runtime.log 2>>../log/runtime.log &
  nohup python3 "${project_path}"/rd_sleep_file_start.py >>../log/runtime.log 2>>../log/runtime.log &
  nohup python3 "${project_path}"/web_rd_sleep_start.py >>../log/runtime.log 2>>../log/runtime.log &
  echo "所有模式已全部开启"
  ;;
5)
  echo "开始打卡"
  nohup python3 "${project_path}"/now_speed_start.py >>../log/runtime.log 2>>../log/runtime.log &
  ;;
6)
  ps -aux | grep "send_mail_report_start" | grep -v grep | awk '{print "kill -9 "$2}' | sh
  nohup python3 "${project_path}"/send_mail_report_start.py >>../log/runtime.log 2>>../log/runtime.log &
  echo "邮件报告提示已开启"
  ;;
esac
