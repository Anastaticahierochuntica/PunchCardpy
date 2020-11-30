# !/bin/bash

ps -aux | grep "zzut_punchcard_start" | grep -v grep | awk '{print "kill -9 "$2}' | sh

echo "服务关闭"