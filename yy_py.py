#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @Time    : 2020-01-28 09:57
#  @Author  : July
from constants import *
import requests
from lxml import html
import os
import sys
import datetime
import csv
import random
import time
from retrying import retry
import re
import ast
import json

etree = html.etree
proxy = {}

# 用的是熊猫代理 http://www.xiongmaodaili.com/ ，按量提取，每次提取1个ip，json格式，买3块钱的就差不多了
proxy_url = 'http://route.xiongmaodaili.com/xiongmao-web/api/glip?secret=2cafe0fa711f5fc243bfe47999e61921&orderNo=GL20200223101445SA8mbNNF&count=1&isTxt=0&proxyType=1'


@retry(stop_max_attempt_number=3, wait_random_min=1000, wait_random_max=5000)
def change_proxy(retry_count):
    if retry_count < 0:
        return

    result = requests.get(proxy_url).json()
    if result['msg'] == 'ok':
        ip = result['obj'][0]['ip']
        port = result['obj'][0]['port']
        proxies = {"http": "http://" + ip + ":" + port, "https": "http://" + ip + ":" + port}
        global proxy
        proxy = proxies
        print(f"代理ip为更改为：{proxies}")
        return proxies
    else:
        time.sleep(1)
        print('切换代理失败，重新尝试。。。')
        change_proxy(retry_count - 1)


header = {
    'User-Agent': ua.random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encodin': 'gzip, deflate',
    'Cookie': 'SERVERID=73cbd63e25a80cc53526e5b6970e3108|1582954566|1582954543',
    'Host': 'qc.wa.news.cn'
}

url = 'http://qc.wa.news.cn/nodeart/list?nid=11215616&pgnum={}&cnt=10&attr=63&tp=1&orderby=1&callback=jQuery1124041623210911370556_1582954546619&_=1582954546623'


def spider(page):
    ret = requests.get(url=url.format(page), headers=header).content.decode()
    p = re.compile(r'\((.*?)\)', re.S)
    dc = p.findall(ret)[0].replace('null', '0')
    print(dc)
    dc = ast.literal_eval(dc)
    print(dc)
    data_list = dc['data']['list']
    print(len(data_list))
    need_list = []
    for d in data_list:
        DocID = d['DocID']
        Title = d['Title']
        PubTime = d['PubTime']
        LinkUrl = d['LinkUrl']
        keyword = d['keyword']
        Editor = d['Editor']
        SourceName = d['SourceName']

        # 详情页数据
        d_header = {
            'User-Agent': ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encodin': 'gzip, deflate',
            'Cookie': 'SERVERID=73cbd63e25a80cc53526e5b6970e3108|1582954566|1582954543',
            'Host': 'www.piyao.org.cn'
        }
        dtl_ret = requests.get(url=LinkUrl, headers=d_header).content.decode()
        root = etree.HTML(dtl_ret)
        content = root.xpath("string(//div[@class='con_txt'])")
        # http://www.piyao.org.cn/2020-02/27/1210491768_15827668876021n.jpg
        # http://www.piyao.org.cn/2020-02/5/1210491912_15827756108181n.jpg
        # http://www.piyao.org.cn/2020-02/28/1210494059_15828785624311n.png
        img_url = 'http://www.piyao.org.cn/' + PubTime[0:7] + '/' + PubTime[8:10] + '/'
        img_urls = img_url + ('\n'+img_url).join(root.xpath("//div[@class='con_txt']//img/@src"))
        print(img_urls)
        need = [DocID, Title, PubTime, LinkUrl, keyword, Editor, SourceName, content, img_urls]

        print(need)
        need_list.append(need)
    return need_list


def get_path(file_name):
    path = os.path.join(os.path.dirname(sys.argv[0]), file_name)
    return path


def save_data(filename, data):
    path = get_path(filename + '.csv')
    if os.path.isfile(path):
        is_exist = True
    else:
        is_exist = False
    with open(path, "a", newline="", encoding="utf_8_sig") as f:
        c = csv.writer(f)
        if not is_exist:
            c.writerow(['DocID', 'Title', 'PubTime', 'LinkUrl', 'keyword', 'Editor', 'SourceName', 'content', 'img_urls'])
        for line in data:
            c.writerow(line)


if __name__ == '__main__':
    # change_proxy(1)
    for page in range(1, 600):
        data = spider(page)
        save_data(filename='wa谣言', data=data)
        print(page)
