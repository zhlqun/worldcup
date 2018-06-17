#!/usr/bin/env python
# -*- coding: utf-8 -*-
##########################################################
# File Name: parse_page.py
# Author: laijiawei, Baidu Inc.
# Mail: laijiawei@baidu.com
# Created Time: 2018-06-15 17:00:02
################################################
#================================================
import os
import sys
import json
from io import open
import util
import time
import urllib2

fp = open("log", "a")

def get_json_data_from_sina(room_id):
    """  从网页爬取最新20条直播记录 """
    page_info = {}
    url = 'http://rapid.sports.sina.com.cn/live/api/msg/index?room_id=' + room_id + '&count=100&msg_id=&direct=-1'
    #url = 'http://rapid.sports.sina.com.cn/live/api/msg/index?room_id=sports%3A201805082&count=10&msg_id=&direct=-1&dpc=1'
    for i in range(20):
        page_data = urllib2.urlopen(url).read()
        page_data = json.loads(page_data, encoding="utf-8")
        result = page_data.get('result', {})
        status = result.get('status', {})
        datas = result.get('data', [])
        idx = ''
        #print room_id, len(datas), status, len(datas)
        if len(datas) > 1:
            idx = datas[-1].get("id", '')
        else:
            break
        detele_vals = ['type', 'liver', 'liver_id', 'ctime']
        fp.write(room_id + '  msg:' + status.get('msg') + str(len(datas)) + "\n")
        fp.flush()
        live_info = result.get('data', [])
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
        url = 'http://rapid.sports.sina.com.cn/live/api/msg/index?room_id=' + room_id + '&count=100&msg_id=' + idx + '&direct=-1'
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


def loads_pasted_info(filename):
    """ 导入旧数据 """
    pasted_info = {}
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                info = json.loads(line.strip())
                pub_time = info['pub_time']
                pasted_info[pub_time] = info
    return pasted_info

def displayer_info(page_info_list, displayer_filename, save_filename, key_dic):
    with open(displayer_filename, 'w', encoding='utf-8') as f:
        for info in page_info_list:
            pub_time = info.get('pub_time')
            pub_time = util.timestamp2string(float(pub_time))
            score = info.get('match', {}).get('score1', '') + u'-' + info.get('match', {}).get('score2', '')
            room_id = info.get('room_id', 0)
            time_now = info.get('mtime', 0)
            key = ""
            for item in key_dic:
                if int(time_now) > key_dic[item][0] - 600 and int(time_now) < key_dic[item][0] + 3600 * 2.5:
                    key = key_dic[item][1].split("#")[2]
                    #if room_id in key_dic:
                    #    key = key_dic[room_id][1].split("#")[2]
                    if 'text' in info:
                        text = 'text\001' + info.get('text', '')
                        if u'权威' not in text \
                            and u'足彩' not in text \
                            and u'小炮' not in text:
                            f.write(pub_time + '\t' + text + '\t' + score + '\t' + key + '\n')
                    if 'gif' in info:
                        gif = 'url\001' + info.get('gif')
                        f.write(pub_time + '\t' + gif + '\t' + score + '\t' + key + '\n')
                    if 'pic' in info:
                        pic = 'url\001' + info.get('pic')
                        f.write(pub_time + '\t' + pic + '\t' + score + '\t' + key + '\n')
    # 存储数据
    with open(save_filename, 'w', encoding='utf-8') as f:
        for info in page_info_list:
            f.write(json.dumps(info, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    key_dic = dict()
    idx = 82
    with open('schedule', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip().split("\t")
            timestamp = line[1]
            key = line[2]
            room_id = 'sports:2018050' + str(idx)
            idx += 1
            key_dic[room_id] = (int(timestamp), key)
     
    displayer_filename = 'data/worldcupDetail'
    idx = 88
    time_cur = time.time()
    idx +=  (int(time_cur) - 1529078400) / (3600 * 24)
    while True:
        time_now = time.time()
        for i in range(idx, idx + 5):
            room_id = "sports:2018050" + str(i)
            date = util.timestamp2string(time_now)
            save_filename = 'data/update_content.txt'
            if True:#(time_now > key_dic[room_id][0] - 600 and time_now < key_dic[room_id][0] + 2.5 * 3600):
                # 1, 导入旧数据
                pasted_info = loads_pasted_info(save_filename)
                # 2, 请求新浪新数据
                page_info = get_json_data_from_sina(str(room_id))
                # 3, 合并新旧数据
                merge_info_list = merge_info(page_info, pasted_info)
                # 4, 展示数据
                displayer_info(merge_info_list, displayer_filename, save_filename, key_dic)
        time.sleep(1)
        #break
