# -*- coding: utf-8 -*-
import csv
import os
import sys
import requests
from fake_useragent import UserAgent
from lxml import html

ua = UserAgent(verify_ssl=False)

etree = html.etree

web_header = {
    'origin': 'https://ncov.dxy.cn',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive'
}


def spider():
    ret = requests.get(url='https://file1.dxycdn.com/2020/0130/454/3393874921745912507-115.json?t=26389890', headers=web_header).json()
    print(ret)
    need_list = []
    data_list = ret['data']
    for data in data_list:
        body = data['body']
        id = data['id']
        mainSummary = data['mainSummary']
        rumorType = data['rumorType']
        score = data['score']
        sourceUrl = data['sourceUrl']
        summary = data['summary']
        title = data['title']

        need = [id, title, body, rumorType, score, sourceUrl, summary, mainSummary]
        need_list.append(need)
    return need_list


def get_path(file_name):
    path = os.path.join(os.path.dirname(sys.argv[0]), file_name)
    return path


def save_data(filename, data):
    # now = datetime.datetime.now().replace()
    # now = str(now)[0:10].replace('-', '').replace(' ', '').replace(':', '')
    path = get_path(filename + '.csv')
    if os.path.isfile(path):
        is_exist = True
    else:
        is_exist = False
    with open(path, "a", newline="", encoding="utf_8_sig") as f:
        c = csv.writer(f)
        if not is_exist:
            c.writerow(['id', 'title', 'body', 'rumorType', 'score', 'sourceUrl', 'summary', 'mainSummary'])
        for line in data:
            c.writerow(line)



if __name__ == '__main__':
    data = spider()
    save_data(filename='丁香谣言', data=data)

