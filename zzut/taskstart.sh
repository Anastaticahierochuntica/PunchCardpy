# !/bin/bash

ps -aux | grep "zzut_punchcard_start" | grep -v grep | awk '{print "kill -9 "$2}' | sh

if [ ! -d $(pwd)/log ]; then
    mkdir log
fi

nohup python3 $(pwd)/bin/zzut_punchcard_start.py >>$(pwd)/log/runtime.log 2>>$(pwd)/log/runtime.log &
