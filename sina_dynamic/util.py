import sys
import json
import urllib2
import urllib
import time
from io import open
reload(sys)
sys.setdefaultencoding("utf-8")

def get_sign(url):
    """
    this is url covert to nid function
    """
    u = sign.creat_sign_fs64(url)
    u0 = long(u & 0xFFFFFFFF)
    u1 = long(u >> 32)
    return str((u0 << 32) + u1)


def get_update_time():
    """  get_update_time """
    timestamp = time.localtime(time.time())
    return time.strftime('%Y-%m-%d %H:%M:%S', timestamp)


def string2timestamp(string):
    """ string2timestamp """
    timeArray = time.strptime(string, "%Y-%m-%d %H:%M:%S")
    timestamp = int(time.mktime(timeArray))
    return timestamp


def timestamp2string(timestamp):
    """ timestamp2string """
    timeArray = time.localtime(timestamp)
    #otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    otherStyleTime = time.strftime("%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


if __name__ == '__main__':
    pass
