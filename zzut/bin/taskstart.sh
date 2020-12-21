# !/bin/bash

if [ ! -d ../log ]; then
    mkdir ../log
fi

echo "1. 开启快速打卡模式"
echo "2. 开启随机分布打卡模式"
echo "3. 开启全变量打卡模式"
echo "4. 以上全部开启"
echo "5. 立即打卡一次"
echo "6. 立即发送报告邮件一次"
read -p "选择需要的模式：" pattern

case $pattern in
1)
    ps -aux | grep "zzut_speed_punchcard_start" | grep -v grep | awk '{print "kill -9 "$2}' | sh
    nohup python3 $(pwd)/zzut_speed_punchcard_start.py >>../log/runtime.log 2>>../log/runtime.log &
    echo "快速打卡模式已开启"
    ;;
2)
    ps -aux | grep "zzut_rd_punchcard_start" | grep -v grep | awk '{print "kill -9 "$2}' | sh
    nohup python3 $(pwd)/zzut_rd_punchcard_start.py >>../log/runtime.log 2>>../log/runtime.log &
    echo "随机分布打卡模式已开启"
    ;;
3)
    ps -aux | grep "zzut_all_punchcard_start" | grep -v grep | awk '{print "kill -9 "$2}' | sh
    nohup python3 $(pwd)/zzut_all_punchcard_start.py >>../log/runtime.log 2>>../log/runtime.log &
    ;;
4)
    ps -aux | grep "zzut_speed_punchcard_start" | grep -v grep | awk '{print "kill -9 "$2}' | sh
    ps -aux | grep "zzut_rd_punchcard_start" | grep -v grep | awk '{print "kill -9 "$2}' | sh
    ps -aux | grep "zzut_all_punchcard_start" | grep -v grep | awk '{print "kill -9 "$2}' | sh
    nohup python3 $(pwd)/zzut_speed_punchcard_start.py >>../log/runtime.log 2>>../log/runtime.log &
    nohup python3 $(pwd)/zzut_rd_punchcard_start.py >>../log/runtime.log 2>>../log/runtime.log &
    nohup python3 $(pwd)/zzut_all_punchcard_start.py >>../log/runtime.log 2>>../log/runtime.log &
    echo "所有模式已全部开启"
    ;;
5)
    echo "开始打卡"
    nohup python3 $(pwd)/now_auto_punchcard.py >>../log/runtime.log 2>>../log/runtime.log &
    ;;
6)
    echo "开始发送"
    nohup python3 $(pwd)/now_report_mail.py >>../log/runtime.log 2>>../log/runtime.log &
    ;;
esac
