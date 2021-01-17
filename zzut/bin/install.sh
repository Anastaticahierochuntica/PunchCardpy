# !/bin/bash

echo "安装火狐浏览器"
# 安装火狐浏览器
sudo yum install firefox -y

echo "安装python3运行环境"
# 安装python3环境
sudo yum install python3 -y

echo "安装python3依赖库"
# 安装python3依赖库
pip3 install pyvirtualdisplay
pip3 install fake_useragent
pip3 install selenium
pip3 install apscheduler
pip3 install email
pip install mysql-connector

echo "安装运行时依赖"
# 安装运行依赖
sudo yum install gtk3 gtk3-devel -y
sudo yum install Xvfb libXfont xorg-x11-fonts* -y
sudo yum install xdpyinfo -y

echo "下载火狐驱动"
# 下载firefox驱动：
wget https://github.com/mozilla/geckodriver/releases/download/v0.28.0/geckodriver-v0.28.0-linux64.tar.gz

echo "布置驱动"
# 解压缩：
tar -zxvf ./geckodriver-v0.28.0-linux64.tar.gz

# 软链接：
ln -s $(pwd)/geckodriver /usr/bin/geckodriver

rm -f ./geckodriver-v0.28.0-linux64.tar.gz

echo "安装结束"
