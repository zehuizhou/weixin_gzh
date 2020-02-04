#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-01-28 09:57
# @Author  : July
from constants import *
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


def spider(page, date, pro):
    parm = {
        'q': '肺炎',
        'page': page,
        'types': 'all',
        '10w': 1,
        'post_time': 5,
        'startTime': date,
        'endTime': date,
        'industry': '全省',
        # 'industry': 'all',
        'proName': pro
    }

    def get_res(c):
        try:
            res = requests.get(url=index_url, headers=web_header, params=parm, proxies=proxy, timeout=(3, 7)).json()
            return res
        except:
            change_proxy(3)
            return get_res(c-1)

    res = get_res(3)
    time.sleep(random.uniform(2.1, 4.5))
    if res['error'] == 0 or res['error'] == 2:
        li = res['data']
        root_li = etree.HTML(li)
        root_li_list = root_li.xpath("//li")
        # 日期，标题，公众号，全文，作者，阅读量，在看，链接，图片和视频链接
        need_list = []
        for li in root_li_list:
            article_date = li.xpath(".//div[@class='fl']/span[1]/text()")[0]  # 日期
            article_title = li.xpath(".//div[@class='word']/h2/a/text()")[0]  # 标题
            article_gzh = li.xpath(".//div[@class='fl']/a/text()")[0]  # 公众号
            article_url = li.xpath(".//div[@class='word']/h2/a/@href")[0]  # 文章地址
            article_read = '10W+'  # 阅读量
            article_up = ''

            # 详情页数据
            def get_data(count):
                if count < 0:
                    return
                try:
                    detail_res = requests.get(url=article_url, headers=detail_header, proxies=proxy, timeout=(3, 7)).content.decode()
                except:
                    change_proxy(3)
                    return get_data(count - 1)
                if '访问过于频繁' in detail_res:
                    change_proxy(3)
                    return get_data(count-1)
                return detail_res

            detail_res = get_data(3)
            time.sleep(random.uniform(1.1, 2.1))
            root_detail_res = etree.HTML(detail_res)
            article_author = root_detail_res.xpath("//span[@class='rich_media_meta rich_media_meta_text']/text()")[0] if \
                root_detail_res.xpath("//span[@class='rich_media_meta rich_media_meta_text']/text()") else ''
            article_author = article_author.replace(' ', '').replace('\n', '')  # 作者
            article_content = root_detail_res.xpath("string(//div[@class='rich_media_content '])").replace(' ', '')  # 文章内容
            article_img_url = root_detail_res.xpath("//div[@class='rich_media_content ']//img/@data-src")
            article_img_url = '\n'.join(article_img_url)    # 图片链接
            article_video_url = root_detail_res.xpath("//iframe/@data-src")[0] if\
                root_detail_res.xpath("//iframe/@data-src") else ''  # 视频链接

            need = [article_date, article_title, article_gzh, article_content, article_author, article_read, article_up,
                    article_url, article_img_url, article_video_url]
            print(need)
            need_list.append(need)
        return need_list
    else:
        print('没有数据。。。')


def get_path(file_name):
    path = os.path.join(os.path.dirname(sys.argv[0]), file_name)
    return path


def save_data(filename, data):
    now = datetime.datetime.now().replace()
    now = str(now)[0:10].replace('-', '').replace(' ', '').replace(':', '')
    path = get_path(filename + str(now) + '.csv')
    if os.path.isfile(path):
        is_exist = True
    else:
        is_exist = False
    with open(path, "a", newline="", encoding="utf_8_sig") as f:
        c = csv.writer(f)
        if not is_exist:
            c.writerow(['日期', '标题', '公众号', '全文', '作者', '阅读量', '在看', '链接', '图片链接', '视频链接'])
        for line in data:
            c.writerow(line)


if __name__ == '__main__':
    page_list = [1, 2, 3, 4, 5]
    # change_proxy(3)
    date_list = ['2020-01-27', '2020-01-28']
    a = []
    pro_list = ['北京', '甘肃', '山西', '内蒙古', '陕西', '吉林', '福建', '贵州', '广东', '青海', '西藏', '四川', '宁夏',
                '海南', '台湾', '香港', '广西', '湖北', '天津', '上海', '重庆', '河北', '河南', '云南', '辽宁', '黑龙江', '湖南',
                '安徽', '山东', '新疆', '江苏', '浙江', '江西', '澳门']

    for i in date_list:
        for j in pro_list:
            for page in page_list:
                data = spider(page=page, date=i, pro=j)
                if data is not None:
                    time.sleep(0.5)
                    save_data('武汉', data)
                    print(f'{i}的{j}第{page}页---------保存成功---------')

    # for i in date_list:
    #     data = spider(page=2, date=i, pro='')
    #     if data is not None:
    #         time.sleep(2)
    #         save_data('武汉加油', data)
