#!/usr/bin/env python
# -*- coding: utf-8 -*-
##########################################################
# File Name: parse_page.py
# Author: laijiawei, Baidu Inc.
# Mail: laijiawei@baidu.com
# Created Time: 2018-06-15 17:00:02
################################################
#================================================
import sys
import json
from io import open
import util
import time
import urllib2


def get_json_data_from_sina(room_id):
    """  从网页爬取最新20条直播记录 """
    page_info = {}
    url = 'http://rapid.sports.sina.com.cn/live/api/msg/index?room_id=sports%3A201805083&count=20&msg_id=192382450157741800&direct=-1&dpc=1'
    #url = 'http://rapid.sports.sina.com.cn/live/api/msg/index?room_id=sports%' + room_id + '&count=100&msg_id=192382405160552166&direct=-1'
    #url = 'http://rapid.sports.sina.com.cn/live/api/msg/index?room_id=sports%3A201805082&count=10&msg_id=192076087950472934&direct=-1&dpc=1'
    page_data = urllib2.urlopen(url).read()
    page_data = json.loads(page_data, encoding="utf-8")
    datas = page_data.get('result', {})
    status = datas.get('status', {})
    detele_vals = ['type', 'liver', 'room_id', 'liver_id', 'ctime']
    if status.get('msg') == 'succ db':
        live_info = datas.get('data', [])
        for info in live_info:
            # 1, 去掉非文字信息
            #if 'text' not in info:
                #print json.dumps(info, encure_ascii=False).encode('utf-8')
            #    continue
            #if 'link' in info:
                #print info['text'].encode('utf-8')
            #    continue
            # 2，去掉不用字段
            for val in detele_vals:
                if val in info:
                    del info[val]
            info['timestamp'] = info.get('mtime', int(time.time()))
            pub_time = info['pub_time']
            page_info[pub_time] = info
    return page_info


def merge_info(page_info, pasted_info):
    """ 合并新旧数据 """
    for pub_time, info in page_info.items():
        pasted_info[pub_time] = info
    page_info_list = sorted(pasted_info.items(), key = lambda x: x[0], reverse=True)
    result_info = []
    for info in page_info_list:
        result_info.append(info[1])
    return result_info


#def loads_pasted_info(matchkey):

def loads_pasted_info(filename):
    """ 导入旧数据 """
    pasted_info = {}
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            info = json.loads(line.strip())
            pub_time = info['pub_time']
            pasted_info[pub_time] = info
    return pasted_info


def displayer_info(page_info_list, displayer_filename, save_filename):
    with open(displayer_filename, 'w', encoding='utf-8') as f:
        for info in page_info_list:
            time = info.get('pub_time')
            time = util.timestamp2string(float(time))
            score = info.get('match', {}).get('score1', '') + u'-' + info.get('match', {}).get('score2', '')
            if 'text' in info:
                text = 'text\001' + info.get('text', '')
                f.write(time + '\t' + text + '\t' + score + '\n')
            if 'gif' in info:
                gif = 'url\001' + info.get('gif')
                f.write(time + '\t' + gif + '\t' + score + '\n')
            if 'pic' in info:
                pic = 'url\001' + info.get('pic')
                f.write(time + '\t' + pic + '\t' + score + '\n')
    # 存储数据
    with open(save_filename, 'w', encoding='utf-8') as f:
        for info in page_info_list:
            print json.dumps(info, ensure_ascii=False).encode('utf-8')
            f.write(json.dumps(info, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    room_id = '3A201805083'
    save_filename = 'data/update_content.txt'
    displayer_filename = 'data/worldcupDetail'
    # 1, 导入旧数据
    pasted_info = loads_pasted_info(save_filename)
    # 2, 请求新浪新数据
    page_info = get_json_data_from_sina(room_id)
    # 3, 合并新旧数据
    merge_info_list = merge_info(page_info, pasted_info)
    # 4, 展示数据
    displayer_info(merge_info_list, displayer_filename, save_filename)


