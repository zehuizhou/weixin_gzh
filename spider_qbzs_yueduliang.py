#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @Time    : 2020-01-28 09:57
#  @Author  : July
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


def spider(keyword, page, date):
    parm = {
        'q': keyword,
        'page': page,
        'types': 'all',
        '10w': 1,
        'post_time': 5,
        'startTime': date,
        'endTime': date,
        # 'industry': '全省',
        'industry': 'all',
        'proName': '',
        'sort': 'readnum'
    }

    def get_res(c):
        if c < 0:
            return
        try:
            res = requests.get(url=index_url, headers=web_header, params=parm, proxies=proxy, timeout=(3, 7)).json()
            print(res)
            return res
        except:
            change_proxy(3)
            return get_res(c - 1)

    res = get_res(3)
    time.sleep(random.uniform(2, 2.5))
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

            # article_up = ''

            # 详情页数据
            def get_data(count):
                if count < 0:
                    return
                try:
                    detail_res = requests.get(url=article_url, headers=detail_header, proxies=proxy,
                                              timeout=(3, 7)).content.decode()
                except:
                    change_proxy(3)
                    return get_data(count - 1)
                if '访问过于频繁' in detail_res:
                    change_proxy(3)
                    return get_data(count - 1)
                return detail_res

            detail_res = get_data(3)

            # time.sleep(random.uniform(0, 0.3))

            root_detail_res = etree.HTML(detail_res)
            article_author = root_detail_res.xpath("//span[@class='rich_media_meta rich_media_meta_text']/text()")[0] if \
                root_detail_res.xpath("//span[@class='rich_media_meta rich_media_meta_text']/text()") else ''
            article_author = article_author.replace(' ', '').replace('\n', '')  # 作者
            article_content = root_detail_res.xpath("string(//div[@class='rich_media_content '])").replace('\n', '') \
                .replace('\r', '').replace('\t', '').replace(' ', '')  # 文章内容
            if article_content == '' or article_content is None:
                is_have = 0
            else:
                is_have = 1

            article_img_url = root_detail_res.xpath("//div[@class='rich_media_content ']//img/@data-src")
            article_img_url = '\n'.join(article_img_url)  # 图片链接
            article_video_url = root_detail_res.xpath("//iframe/@data-src")
            article_video_url = '\n'.join(article_video_url)  # 视频链接
            need = [article_date, article_title, article_gzh, article_content, article_author, article_read,
                    article_url, article_img_url, article_video_url, is_have]
            print(need)
            need_list.append(need)
        return need_list
    else:
        print('没有数据。。。')
        return None


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
            c.writerow(['日期', '标题', '公众号', '全文', '作者', '阅读量', '链接', '图片链接', '视频链接', '是否有内容'])
        for line in data:
            c.writerow(line)


if __name__ == '__main__':
    change_proxy(1)

    # keywords = ['病人', '肺炎', '高福', '韩红', '患者', '口罩', '李兰娟', '李文亮', '辟谣', '武汉', '谣言', '医生', '钟南山',
    #             '专家', '张文宏', '记者']
    keywords = ['李兰娟', '李文亮', '辟谣', '武汉', '谣言', '医生', '钟南山', '专家', '张文宏', '记者']

    page_list = [1, 2, 3, 4, 5]

    # date_list = ['2020-01-07', '2020-01-08', '2020-01-09', '2020-01-10', '2020-01-11', '2020-01-12', '2020-01-13',
    #              '2020-01-14', '2020-01-15', '2020-01-16', '2020-01-17', '2020-01-18', '2020-01-19', '2020-01-20',
    #              '2020-01-21', '2020-01-22', '2020-01-23', '2020-01-24', '2020-01-25', '2020-01-26', '2020-01-27',
    #              '2020-01-28', '2020-01-29', '2020-01-30', '2020-01-31', '2020-02-01', '2020-02-02', '2020-02-03',
    #              '2020-02-04', '2020-02-05', '2020-02-06', '2020-02-07', '2020-02-08', '2020-02-09', '2020-02-10',
    #              '2020-02-11', '2020-02-12', '2020-02-13', '2020-02-14', '2020-02-15', '2020-02-16', '2020-02-17',
    #              '2020-02-18', '2020-02-19', '2020-02-20', '2020-02-21', '2020-02-22', '2020-02-23', '2020-02-24',
    #              '2020-02-25', '2020-02-26', '2020-02-27', '2020-02-28', '2020-02-29', '2020-03-01', '2020-03-02',
    #              '2020-03-03', '2020-03-04', '2020-03-05', '2020-03-06', '2020-03-07', '2020-03-08', '2020-03-09',
    #              '2020-03-10', '2020-03-11', '2020-03-12', '2020-03-13', '2020-03-14', '2020-03-15', '2020-03-16',
    #              '2020-03-17', '2020-03-18', '2020-03-19', '2020-03-20', '2020-03-21', '2020-03-22', '2020-03-23',
    #              '2020-03-24', '2020-03-25', '2020-03-26', '2020-03-27', '2020-03-28', '2020-03-29', '2020-03-30',
    #              '2020-03-31', '2020-04-01', '2020-04-02', '2020-04-03', '2020-04-04', '2020-04-05']

    date_list = ['2020-01-07', '2020-01-08', '2020-01-09', '2020-01-10', '2020-01-11', '2020-01-12', '2020-01-13',
                 '2020-01-14', '2020-01-15', '2020-01-16', '2020-01-17', '2020-01-18', '2020-01-19', '2020-01-20',
                 '2020-01-21', '2020-01-22', '2020-01-23', '2020-01-24', '2020-01-25', '2020-01-26', '2020-01-27',
                 '2020-01-28', '2020-01-29', '2020-01-30', '2020-01-31', '2020-02-01', '2020-02-02', '2020-02-03',
                 '2020-02-04', '2020-02-05', '2020-02-06', '2020-02-07', '2020-02-08', '2020-02-09', '2020-02-10',
                 '2020-02-11', '2020-02-12', '2020-02-13', '2020-02-14', '2020-02-15', '2020-02-16', '2020-02-17',
                 '2020-02-18', '2020-02-19', '2020-02-20', '2020-02-21', '2020-02-22', '2020-02-23', '2020-02-24',
                 '2020-02-25', '2020-02-26', '2020-02-27', '2020-02-28', '2020-02-29', '2020-03-01', '2020-03-02',
                 '2020-03-03', '2020-03-04', '2020-03-05', '2020-03-06', '2020-03-07', '2020-03-08', '2020-03-09',
                 '2020-03-10', '2020-03-11', '2020-03-12', '2020-03-13', '2020-03-14', '2020-03-15', '2020-03-16',
                 '2020-03-17', '2020-03-18', '2020-03-19', '2020-03-20', '2020-03-21', '2020-03-22', '2020-03-23',
                 '2020-03-24', '2020-03-25', '2020-03-26', '2020-03-27', '2020-03-28', '2020-03-29', '2020-03-30',
                 '2020-03-31', '2020-04-01', '2020-04-02', '2020-04-03', '2020-04-04', '2020-04-05']

    for k in keywords:
        for d in date_list:
            for page in page_list:
                data = spider(keyword=k, page=page, date=d)
                if data is not None:
                    save_data(k, data)
                    print(f'{k}{d}第{page}页---------保存成功---------')
                else:
                    print("暂无数据，不继续请求下一页")
                    break

    # for i in date_list:
    #     for page in page_list:
    #         data = spider(page=page, date=i, pro='')
    #         if data is not None:
    #             time.sleep(0.1)
    #             save_data(keyword, data)
    #             print(f"{i}的第{page}页存储成功")
    #         else:
    #             print("暂无数据，不继续请求下一页")
    #             break
