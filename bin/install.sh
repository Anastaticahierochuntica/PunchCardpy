#!/bin/bash
echo "安装python3运行环境"
# 安装python3环境
sudo yum install python3 -y

echo "安装python3依赖库"
# 安装python3依赖库
pip3 install pyvirtualdisplay
pip3 install apscheduler
pip3 install email
pip install mysql-connector

echo "安装运行时依赖"
# 安装运行依赖
sudo yum install gtk3 gtk3-devel -y
sudo yum install Xvfb libXfont xorg-x11-fonts* -y
sudo yum install xdpyinfo -y

echo "安装结束"
