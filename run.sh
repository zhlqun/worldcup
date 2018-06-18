#!/usr/bin/env bash
#encoding=utf8

ps -ef|grep "server.py" | grep -v grep|cut -c 9-15|xargs kill -9
ps -ef|grep "parse_page.py" | grep -v grep|cut -c 9-15|xargs kill -9
cd sina_dynamic/
nohup python parse_page.py > log 2>&1 &
cd ../
nohup python server.py > log 2>&1 &
