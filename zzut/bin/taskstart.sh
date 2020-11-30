# !/bin/bash

ps -aux | grep "zzut_punchcard_start" | grep -v grep | awk '{print "kill -9 "$2}' | sh

if [ ! -d ../log ]; then
    mkdir ../log
fi

nohup python3 $(pwd)/zzut_punchcard_start.py >>../log/runtime.log 2>>../log/runtime.log &

echo "服务开启"
