# !/bin/bash

echo "1. 关闭快速打卡模式"
echo "2. 关闭随机分布打卡模式"
echo "3. 关闭配合WEB随机分布打卡模式"
echo "4. 全部关闭"

read -p "选择需要关闭的模式：" pattern

case $pattern in
1)
    ps -aux | grep "zzut_speed_punchcard_start" | grep -v grep | awk '{print "kill -9 "$2}' | sh
    echo "快速打卡模式已关闭"
    ;;
2)
    ps -aux | grep "zzut_rd_punchcard_start" | grep -v grep | awk '{print "kill -9 "$2}' | sh
    echo "随机分布打卡模式已关闭"
    ;;
3)
    ps -aux | grep "zzut_rd_web_start.py" | grep -v grep | awk '{print "kill -9 "$2}' | sh
    echo "配合WEB随机分布打卡模式已关闭"
    ;;
4)
    ps -aux | grep "zzut_speed_punchcard_start" | grep -v grep | awk '{print "kill -9 "$2}' | sh
    ps -aux | grep "zzut_rd_punchcard_start" | grep -v grep | awk '{print "kill -9 "$2}' | sh
    ps -aux | grep "zzut_rd_web_start.py" | grep -v grep | awk '{print "kill -9 "$2}' | sh
    echo "所有模式已全部关闭"
    ;;
esac
