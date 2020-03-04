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
    'Cookie': 'SLARDAR_WEB_ID=80211543-16b3-473e-a64f-a943c2b34fbb'
}

url = 'https://i.snssdk.com/rumor-denier/list/?offset=0&count=800'


def spider():
    ret = requests.get(url=url, headers=header).json()
    print(len(ret['data']))
    data = ret['data']
    need_list = []
    for d in data:
        id = d['id']
        status = d['annotation']['status']
        is_hot = d['is_hot']
        title = d['title']
        created_at = str(d['created_at'])
        time_array = time.localtime(int(created_at[0:10]))
        created_at = time.strftime("%Y-%m-%d %H:%M:%S", time_array)

        updated_at = str(d['updated_at'])
        time_array = time.localtime(int(updated_at[0:10]))
        updated_at = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
        read_count = d['read_count']

        # 详情页数据
        dtl_url = 'https://m.toutiao.com/i{}/info/?_signature=wFZ9DhAVnhkojF9zU0sGUsBWfR&i={}'.format(id, id)
        time.sleep(random.uniform(1.2, 3.5))
        def get_dtl_ret(retry_count):
            if retry_count < 0:
                raise 0
            try:
                dtl_ret = requests.get(url=dtl_url, headers=header, proxies=proxy, timeout=6).json()
                return dtl_ret
            except:
                change_proxy(3)
                return get_dtl_ret(retry_count-1)

        dtl_ret = get_dtl_ret(3)
        try:
            auth_info = dtl_ret['data']['media_user']['user_auth_info']['auth_info']
        except:
            auth_info = ''

        d_url = dtl_ret['data']['url']
        impression_count = dtl_ret['data']['impression_count']
        is_original = dtl_ret['data']['is_original']
        is_pgc_article = dtl_ret['data']['is_pgc_article']

        content_html = dtl_ret['data']['content']
        content_root = etree.HTML(content_html)
        content1 = content_root.xpath('string(/)')
        content2 = '\n'.join(content_root.xpath('//text()'))

        strong = content_root.xpath('//p/strong')

        source = ''
        for s in strong:
            if s.xpath("./text()")[0] == '辟谣来源：':
                source = s.xpath('./../text()')[0] if s.xpath('./../text()') else ''
                print(source)

        imgs = content_root.xpath("//img/@src")
        comment_count = dtl_ret['data']['comment_count']

        need = [id, status, is_hot, title, source, created_at, updated_at, read_count, auth_info, d_url, impression_count,
                is_original, is_pgc_article, content1, content2, imgs, comment_count]
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
            c.writerow(
                ['id', 'status', 'is_hot', 'title', 'source', 'created_at', 'updated_at', 'read_count', 'auth_info', 'd_url',
                 'impression_count',
                 'is_original', 'is_pgc_article', 'content1', 'content2', 'imgs', 'comment_count'])
        for line in data:
            c.writerow(line)


if __name__ == '__main__':
    # change_proxy(1)
    data = spider()
    save_data(filename='今日头条谣言', data=data)
