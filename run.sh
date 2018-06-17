#!/usr/bin/env bash
#encoding=utf8

cd sina_dynamic/
nohup python parse_page.py &
nohup python server.py > log 2>&1 &
